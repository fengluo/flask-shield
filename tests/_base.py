import unittest
from flask import Flask, request, g, jsonify
from flask_shield import Shield, login_user, logout_user


class User(object):
    def __init__(self, id, username):
        self.id = id
        self.username = username

    @property
    def is_active(self):
        return True

    def get_perms(self):
        return ['edit', 'advance_edit']


def get_user_by_id(users, id):
    l = filter(lambda x: x.id == id, users)
    return l[0] if len(l) > 0 else None


class Permission(object):
    def __init__(self, slug):
        self.slug = slug


def get_permission_by_slug(permissions, slug):
    l = filter(lambda x: x.slug == slug, permissions)
    return l[0] if len(l) > 0 else None


class BaseCase(unittest.TestCase):
    config = {
        'TESTING': True,
        'DEBUG': True,
        'SECRET_KEY': 'secret test'
    }

    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client()

    def create_app(self):
        app = Flask(__name__)
        app.config.update(self.config)

        @app.errorhandler(403)
        def forbidden(error):
            return jsonify(error='Sorry, page not allowed'), 403

        permissions = []
        users = [User(1, 'foo'), User(2, 'boo')]
        shield = Shield()

        shield.init_app(app)

        @shield.user_loader
        def load_user(id):
            return get_user_by_id(users, id)

        @shield.permission_loader
        def load_permission(slug):
            return get_permission_by_slug(permissions, slug)

        @shield.permission_saver
        def save_permission(slug):
            permissions.append(Permission(slug=slug))

        @app.route('/', methods=["GET"])
        def index():
            return 'index'

        @app.route('/login', methods=["POST"])
        def login():
            login_user(User(1, 'foo'))
            return str(g.user.id)

        @app.route('/logout', methods=["POST"])
        def logout():
            pass

        @app.route('/edit', methods=["GET"])
        @shield.require_permission(['edit', 'advance_edit'])
        def edit():
            if shield.check_permission('normal_edit'):
                return 'edit'

        shield.register_permissions()

        return app
