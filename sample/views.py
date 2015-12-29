from flask import Blueprint, request, abort, render_template, g
from flask.ext.shield import login_user

from extensions import shield
from permissions import EditPerm, AdvanceEditPerm
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
@shield.require_permission(EditPerm, AdvanceEditPerm)
def edit():
    print g.user.get_perms()
    if shield.check_permission(AdvanceEditPerm):
        return 'advance_edit'
    return 'edit'
