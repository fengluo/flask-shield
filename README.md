# Flask-Shield

Flask-Shield is an extension of Flask for permission management based on RBAC.

Example:

See **sample** in repository

```
# install dependencies
pip install -r requirements.txt

# create sqlite db
python manage.py createdb

# create permissions
python manage.py register_permissions

# create sample users
# name: foo password: 123 permissions: edit
# name: boo password: 123 permissions: edit, advance_edit
python manage.py create_sample_user

# run server
# URL: http://127.0.0.1:5000/login
python manage.py runserver

# You can find different users have different permissions on the path of edit.
```