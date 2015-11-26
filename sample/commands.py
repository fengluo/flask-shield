from flask.ext.script import Command
from extensions import shield, db

from models import User, Permission


class CreateDBCommand(Command):
    def run(self):
        db.create_all()


class DropDBCommand(Command):
    def run(self):
        db.drop_all()


def _make_context():
    return dict(db=db)


class RegisterPermissionsCommand(Command):
    def run(self):
        shield.register_permissions()


class CreateSampleUser(Command):
    def run(self):
        edit_perm = Permission.query.filter_by(slug='edit').first()
        advance_edit_perm =\
            Permission.query.filter_by(slug='advance_edit').first()
        user_foo = User(name='foo', password='123')
        user_foo.permissions.append(edit_perm)
        db.session.add(user_foo)
        user_boo = User(name='boo', password='123')
        user_boo.permissions.append(edit_perm)
        user_boo.permissions.append(advance_edit_perm)
        db.session.add(user_boo)
        db.session.commit()
