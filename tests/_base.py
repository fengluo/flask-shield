# -*- coding: utf-8 -*-

from flask_shield import UserMixin, PermissionMixin


class Permission(PermissionMixin):
    def __init__(self, slug, name=None, category=None):
        self.slug = slug
        self.name = name
        self.category = category


def get_permission_by_slug(permissions, slug):
    results = filter(lambda x: x.slug == slug, permissions)
    return results[0] if len(results) > 0 else None


class User(UserMixin):
    def __init__(self, id, name, permissions):
        self.id = id
        self.name = name
        self.permissions = permissions

    @property
    def is_active(self):
        return True


def get_user_by_id(users, id):
    l = filter(lambda x: x.id == id, users)
    return l[0] if len(l) > 0 else None


def get_user_by_name(users, name):
    l = filter(lambda x: x.name == name, users)
    return l[0] if len(l) > 0 else None
