# -*- coding: utf-8 -*-
from functools import wraps
from flask import g, abort, request, session, current_app

from datetime import timedelta
from werkzeug.security import safe_str_cmp
from hashlib import sha512
import hmac

COOKIE_NAME = 'remember_token'
COOKIE_DURATION = timedelta(days=365)
AUTH_HEADER_NAME = 'Authorization'
ID_ATTRIBUTE = 'get_id'
PERMS_ATTRIBUTE = 'get_perms'


class PermissionDecorator(object):
    def __init__(self, permissions):
        self.permissions = permissions

    def __call__(self, f):
        @wraps(f)
        def _decorated(*args, **kw):
            if getattr(g, 'user') and not getattr(g.user, 'is_authenticated'):
                abort(401)
            if (self.permissions
                    and not
                    set(self.permissions)
                    & set(getattr(g.user, PERMS_ATTRIBUTE)())):
                abort(403)
            return f(*args, **kw)
        return _decorated


class Shield(object):
    def __init__(self, app=None):
        self.anonymous_user = AnonymousUserMixin
        self.permissions = []

        self.user_callback = None
        self.header_callback = None
        self.token_callback = None
        self.header_send = None
        self.permission_callback = None
        self.permission_send = None

        if app:
            self.init_app(app)

    def init_app(self, app):
        app.before_request(self._load_user)
        self.app = app

    def reload_user(self, user=None):
        if user is not None:
            g.user = user
            return

        user_id = session.get('user_id')
        if user_id is None:
            g.user = self.anonymous_user()
            return

        if self.user_callback is None:
            raise Exception(
                "No user_loader has been installed")

        user = self.user_callback(user_id)
        g.user = user if user else self.anonymous_user()

    def _load_user(self):
        config = current_app.config
        if 'user_id' not in session:
            cookie_name = config.get('REMEMBER_COOKIE_NAME', COOKIE_NAME)
            header_name = config.get('AUTH_HEADER_NAME', AUTH_HEADER_NAME)
            has_cookie = (cookie_name in request.cookies and
                          session.get('remember') != 'clear')
            if has_cookie:
                return self._load_from_cookie(request.cookies[cookie_name])
            elif header_name in request.headers:
                return self._load_from_header(request.headers[header_name])
        return self.reload_user()

    def _load_from_cookie(self, cookie):
        if self.token_callback:
            user = self.token_callback(cookie)
            if user is not None:
                session['user_id'] = getattr(user, ID_ATTRIBUTE)()
                session['_fresh'] = False
            self.reload_user()
        else:
            user_id = decode_cookie(cookie)
            if user_id is not None:
                session['user_id'] = user_id
                session['_fresh'] = False
            self.reload_user()

    def _load_from_header(self, header):
        user = None
        if self.header_callback:
            user = self.header_callback(header)
        self.reload_user(user=user)

    def token_loader(self, callback):
        self.token_callback = callback
        return callback

    def user_loader(self, callback):
        self.user_callback = callback
        return callback

    def header_loader(self, callback):
        self.header_callback = callback
        return callback

    def header_saver(self, send):
        self.header_send = send
        return send

    def permission_loader(self, callback):
        self.permission_callback = callback
        return callback

    def permission_saver(self, send):
        self.permission_send = send
        return send

    def require_permission(self, *permissions):
        self.permissions.extend(permissions)
        return PermissionDecorator(permissions)

    def check_permission(self, permission):
        if not g.user:
            return False  # 401
        if permission not in getattr(g.user, PERMS_ATTRIBUTE)():
            return False  # 403
        return True

    def register_permissions(self):
        for permission in self.permissions:
            # Todo
            result = self.permission_callback(permission.get_slug())
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


class PermissionMixin(object):
    def get_slug(self):
        try:
            return unicode(self.slug)
        except AttributeError:
            raise NotImplementedError(
                'No `slug` attribute - override `get_slug`')

    def __eq__(self, other):
        '''
        Check the equality of two `PermissionMixin` objects using `get_slug`.
        '''
        if isinstance(other, PermissionMixin):
            return self.get_slug() == other.get_slug()
        return NotImplemented

    def __ne__(self, other):
        '''
        Check the inequality of two `PermissionMixin` objects using `get_slug`.
        '''
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal

    def __hash__(self):
        return hash(self.get_slug())


class UserMixin(object):
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    def get_id(self):
        try:
            return unicode(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def get_perms(self):
        try:
            return self.permissions
        except AttributeError:
            raise NotImplementedError(
                'No `permissions` attribute - override `get_perms`')

    def __eq__(self, other):
        '''
        Checks the equality of two `UserMixin` objects using `get_id`.
        '''
        if isinstance(other, UserMixin):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __ne__(self, other):
        '''
        Checks the inequality of two `UserMixin` objects using `get_id`.
        '''
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal


class AnonymousUserMixin(object):
    '''
    This is the default object for representing an anonymous user.
    '''
    @property
    def is_authenticated(self):
        return False

    @property
    def is_active(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return


def encode_cookie(payload):
    '''
    This will encode a ``unicode`` value into a cookie, and sign that cookie
    with the app's secret key.
    :param payload: The value to encode, as `unicode`.
    :type payload: unicode
    '''
    return u'{0}|{1}'.format(payload, _cookie_digest(payload))


def decode_cookie(cookie):
    '''
    This decodes a cookie given by `encode_cookie`. If verification of the
    cookie fails, ``None`` will be implicitly returned.
    :param cookie: An encoded cookie.
    :type cookie: str
    '''
    try:
        payload, digest = cookie.rsplit(u'|', 1)
        if hasattr(digest, 'decode'):
            digest = digest.decode('ascii')  # pragma: no cover
    except ValueError:
        return

    if safe_str_cmp(_cookie_digest(payload), digest):
        return payload


def _cookie_digest(payload, key=None):
    key = _secret_key(key)

    return hmac.new(key, payload.encode('utf-8'), sha512).hexdigest()


def _secret_key(key=None):
    if key is None:
        key = current_app.config['SECRET_KEY']

    if isinstance(key, unicode):  # pragma: no cover
        key = key.encode('latin1')  # ensure bytes

    return key
