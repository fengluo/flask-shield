class PermMetaClass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Perm':
            return type.__new__(cls, name, bases, attrs)
        attrs['namespace'] = attrs.get(
            'namespace', attrs['__module__']).lower()
        attrs['slug'] = '.'.join([attrs['namespace'], name.lower()])
        attrs['name'] = attrs.get('name', None)
        return type.__new__(cls, name, bases, attrs)


class Perm(object):
    __metaclass__ = PermMetaClass

    def __init__(self, **kw):
        super(Perm, self).__init__(**kw)

    def __hash__(self):
        return hash(self.slug)


class BasePerm(Perm):
    title = 'hre'


class AccountPerm(BasePerm):
    namespace = 'Account'


class NewPerm(AccountPerm):
    name = 'NewAccount'


class EditPerm(AccountPerm):
    name = 'EditAccount'


def get_all_subclasses(cls):
        all_subclasses = []

        for subclass in cls.__subclasses__():
            print subclass().name
            all_subclasses.append(subclass)
            tmp = get_all_subclasses(subclass)
            all_subclasses.extend(tmp)

        return all_subclasses

get_all_subclasses(Perm)
