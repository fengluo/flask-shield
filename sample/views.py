from flask import Blueprint, request, abort, render_template, g
from flask.ext.shield import login_user

from extensions import shield
from permissions import edit_perm, advance_edit_perm
from models import User

post = Blueprint('post', __name__)


@post.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    name = request.values.get('name')
    password = request.values.get('password')
    user = User.query.filter_by(name=name, password=password).first()
    if user:
        login_user(user)
        return render_template('result.html', user=g.user)
    else:
        abort(403)


@post.route('/edit', methods=["GET"])
@shield.require_permission(edit_perm, advance_edit_perm)
def edit():
    if shield.check_permission(advance_edit_perm):
        return 'advance_edit'
    return 'edit'
