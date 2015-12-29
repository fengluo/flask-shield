# from models import Permission

# edit_perm = Permission(slug='edit', name='Edit')
# advance_edit_perm = Permission(slug='advance_edit', name='Advance Edit')

from flask_shield import Perm


class EditPerm(Perm):
    namespace = 'post'
    name = 'Edit'


class AdvanceEditPerm(Perm):
    namespace = 'post'
    name = 'Advance Edit'
