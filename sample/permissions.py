# from models import Permission

# edit_perm = Permission(slug='edit', name='Edit')
# advance_edit_perm = Permission(slug='advance_edit', name='Advance Edit')

from flask_shield import Perm


class PostPerm(Perm):
    name = 'Post'
    slug = 'post'
    namespace = 'post'


class EditPerm(PostPerm):
    name = 'Edit'
    slug = 'edit'


class AdvanceEditPerm(PostPerm):
    name = 'Advance Edit'
    slug = 'advance_edit'
