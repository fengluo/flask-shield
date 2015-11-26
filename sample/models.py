from flask.ext.shield import PermissionMixin, UserMixin
from extensions import db

permissions = db.Table(
    'user_permission',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id')))


class Permission(db.Model, PermissionMixin):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100))
    name = db.Column(db.String(100))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(255))

    permissions = db.relationship(
        'Permission',
        secondary=permissions,
        backref=db.backref('users', lazy='dynamic'))
