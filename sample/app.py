from flask import Flask
from extensions import db, shield

from models import User, Permission
from views import post


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.conf')

    db.init_app(app)
    app.db = db
    shield.init_app(app)

    @shield.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # add the part below if use jwt
    #
    # import jwt
    # @shield.header_loader
    # def load_user_from_header(header):
    #    token = header.replace('Bearer ', '', 1)
    #    try:
    #        token_dict = jwt.decode(token, app.config['SECRET_KEY'])
    #    except Exception:
    #        abort(401)
    #    user_id = token_dict['id']
    #    return User.query.get(int(user_id))

    @shield.permission_loader
    def load_permission(slug):
        return Permission.query.filter_by(slug=slug).first()

    @shield.permission_saver
    def save_permission(perm):
        permission = Permission(name=perm.name, slug=perm.slug)
        db.session.add(permission)
        db.session.commit()

    app.register_blueprint(post)

    return app
