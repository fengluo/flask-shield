# -*- coding: utf-8 -*-
from flask import g, session, abort
from flask.signals import Namespace

signals = Namespace()

user_loader = signals.signal('user-loader')
permission_loader = signals.signal('permission-loader')
permission_saver = signals.signal('permission-saver')


class Shield(object):
    def __init__(self, app=None):
        self.permissions = []
        self.user_callback = None
        self.permission_callback = None
        self.permission_send = None

    def init_app(self, app):
        app.before_request(self._get_current_user)
        self.app = app

    def _get_current_user(self):
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            g.user = self.user_callback(user_id)

    def user_loader(self, callback):
        self.user_callback = callback
        return callback

    def permission_loader(self, callback):
        self.permission_callback = callback
        return callback

    def permission_saver(self, send):
        self.permission_send = send
        return send

    def require_permission(self, permissions):
        def decorator(func):
            self.permissions.extend(permissions)

            def wrappers(*args, **kw):
                if not g.user:
                    abort(401)
                if not set(permissions) & set(g.user.get_perms()):
                    abort(403)
                return func(*args, **kw)
            return wrappers
        return decorator

    def register_permissions(self):
        for permission in self.permissions:
            result = self.permission_callback(permission)
            if not result:
                self.permission_send(permission)


def login_user(user, remember=False, force=False):
    if not force and not user.is_active:
        return False
    user_id = getattr(user, 'id')
    session['user_id'] = user_id
    if remember:
        session['remember'] = 'set'
    g.user = user
    return True


def logout_user():
    if 'user_id' in session:
        session.pop('user_id')
    session['remember'] = 'clear'
    g.user = None
    return True
