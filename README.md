# Flask-Shield

Flask-Shield is an extension of Flask for permission management based on RBAC.

extensions.py

```
from flask.ext.shield import Shield
shield = Shield()
```

__init__.py

```
    shield.init_app(app)

    @shield.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @shield.permission_loader
    def load_permission(slug):
        return Permission.query.filter_by(slug=slug).first()

    @shield.permission_saver
    def save_permission(slug):
        db.session.add(Permission(slug=slug))
        db.session.commit()
```

views.py

```
@api.route('/posts/<id>/edit', methods=["POST"])
@shield.require_permission(['edit', 'advance_edit'])
def edit(id):
    if shield.check_permission('advance_edit'):
        return 'advance_edit'
```
