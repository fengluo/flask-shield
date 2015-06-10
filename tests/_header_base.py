# -*- coding: utf-8 -*-

import jwt
import unittest
from flask import Flask, request, g, jsonify, abort
from flask_shield import Shield, login_user, logout_user, UserMixin
from ._base import Permission, get_permission_by_slug
from ._base import User, get_user_by_id, get_user_by_name


class HeaderCase(unittest.TestCase):
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

        @app.errorhandler(401)
        def forbidden(error):
            return jsonify(error='Sorry, page not allowed'), 401

        index_perm = Permission(slug='index', name=u'首页', category=u'全局')
        edit_perm = Permission(slug='edit', name=u'编辑', category=u'文章')
        advance_edit_perm = Permission(
            slug='advance_edit', name=u'高级编辑', category=u'文章')

        permissions = [index_perm, edit_perm, advance_edit_perm]
        foo = User(1, 'foo', [index_perm, edit_perm])
        boo = User(2, 'boo', [index_perm, edit_perm, advance_edit_perm])
        users = [foo, boo]
        shield = Shield()

        shield.init_app(app)

        @shield.user_loader
        def load_user(id):
            return get_user_by_id(users, id)

        @shield.header_loader
        def load_user_from_header(header):
            token = header.replace('Bearer ', '', 1)
            try:
                token_dict = jwt.decode(token, app.config['SECRET_KEY'])
            except Exception:
                abort(401)
            user_id = token_dict['id']
            return get_user_by_id(users, user_id)

        @shield.permission_loader
        def load_permission(slug):
            return get_permission_by_slug(permissions, slug)

        @shield.permission_saver
        def save_permission(permission):
            permissions.append(permission)

        @app.route('/', methods=["GET"])
        @shield.require_permission(index_perm)
        def index():
            return 'index'

        @app.route('/login', methods=["POST"])
        def login():
            name = request.values.get('name')
            user = get_user_by_name(users, name)
            if user:
                login_user(user)
                return str(g.user.id)
            else:
                abort(403)

        @app.route('/logout', methods=["POST"])
        def logout():
            pass

        @app.route('/edit', methods=["GET"])
        @shield.require_permission(edit_perm, advance_edit_perm)
        def edit():
            # if shield.check_permission('normal_edit'):
            return 'edit'

        shield.register_permissions()

        return app
