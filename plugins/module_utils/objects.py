# -*- coding: utf-8 -*-

# (c) 2019, Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from collections import namedtuple
from collections import MutableMapping

from ansible.module_utils.six import iteritems, iterkeys

from ansible_collections.ciscodevnet.ansible_dnac.plugins.module_utils.helpers import first

ApiObject = lambda o: namedtuple('ApiObject', o.keys())(**o)
ConfigObject = lambda o, item: namedtuple('ConfigObject', iterkeys(o))(**dict([(k, item[k]) for k in iterkeys(o)]))

Operations = namedtuple('Operations', ('post', 'put', 'delete'))
Updates = namedtuple('Updates', ('post', 'put', 'delete'))

MappedKey = namedtuple('Map', ('key', 'mapped_key', 'transform'))
MatchAttr = namedtuple('MatchAttr', ('configattr', 'apiattr'))


class KeyMap(MutableMapping):

    def __init__(self, *args):
        self._objects = {}
        for arg in args:
            self.add(*arg)

    def __getitem__(self, key):
        return self._objects[key]

    def __setitem__(self, key, value):
        assert isinstance(value, MappedKey)
        self._objects[key] = value

    def __delitem__(self, key, value):
        del self._objects[key]

    def __len__(self):
        return len(self._objects)

    def __iter__(self):
        return iter(self._objects)

    def add(self, key, mapped_key=None, transform=None):
        mapped_key = mapped_key or key
        if transform:
            assert callable(transform)
        self._objects[key] = MappedKey(key, mapped_key, transform)


def create(obj, item, mapping=None):
    kwargs = {}
    mapping = mapping or {}
    for f in obj._fields:
        key = mapping.get(f, f)
        kwargs[key] = item[key]
    return obj(**kwargs)


def match(obj, collection, fields):
    objects = list(collection)

    for key in fields:
        if isinstance(key, MatchAttr):
            configattr = key.configattr
            apiattr = key.apiattr
            tmpobj = [item for item in objects if getattr(obj, configattr) == getattr(item, apiattr)]
        else:
            tmpobj = [item for item in objects if getattr(obj, key) == getattr(item, key)]

        if not tmpobj:
            return None
        else:
            objects = tmpobj

    return first(objects)


def serialize(o, mapping=None):
    if mapping and not isinstance(mapping, KeyMap):
        raise Exception("Mapping must be of type {}".format(type(KeyMap)))

    if isinstance(o, list):
        return [serialize(obj, mapping) for obj in o]

    else:
        obj = {}
        mapping = mapping or {}

        if hasattr(o, '_asdict'):
            o = dict(o._asdict())

        if mapping:
            for key, mapped_key in iteritems(mapping):
                value = o.get(key)
                key = getattr(mapped_key, 'mapped_key', key)
                if mapped_key.transform:
                    value = mapped_key.transform(value)
                if value is not None:
                    obj[key] = value

        return obj or o


def mapped_key(key, mapped_key=None, transform=None):
    mapped_key = mapped_key or key
    return MappedKey(key, mapped_key, transform)


def matchattr(configattr, apiattr=None):
    return MatchAttr(configattr, (apiattr or configattr))
