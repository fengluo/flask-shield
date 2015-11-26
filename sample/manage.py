from flask.ext.script import Manager, Shell
from app import create_app
from commands import CreateDBCommand, DropDBCommand,\
    _make_context, RegisterPermissionsCommand, CreateSampleUser


app = create_app()
manager = Manager(app)
manager.add_command('createdb', CreateDBCommand())
manager.add_command('dropdb', DropDBCommand())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('register_permissions', RegisterPermissionsCommand())
manager.add_command('create_sample_user', CreateSampleUser())

if __name__ == '__main__':
    manager.run()
