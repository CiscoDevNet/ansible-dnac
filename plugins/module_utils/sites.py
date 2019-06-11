# -*- coding: utf-8 -*-

# (c) 2019, Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.connection import Connection

from ansible_collections.ciscodevnet.ansible_dnac.plugins.module_utils import objects


API_TO_FACTS_MAP = objects.KeyMap(
    objects.mapped_key('groupNameHierarchy', 'path'),
    objects.mapped_key('locationAddress', 'address'),
    objects.mapped_key('locationCountry', 'country'),
    objects.mapped_key('name'),
    objects.mapped_key('latitude'),
    objects.mapped_key('longitude')
)

def get(module):
    connection = Connection(module._socket_path)
    resp = connection.get('/dna/intent/api/v1/topology/site-topology')
    resp = module.from_json(resp)
    resp = resp['response']['sites']

    # make sure the api response returned a dict object
    if not isinstance(resp, (dict, list)):
        module.fail_json(
            msg="invalid object type, got {}, expected one of {}".format(type(resp), ','.join((dict, list)))
        )

    return [objects.ApiObject(o) for o in resp]


def get_facts(module):
    collection = get(module)
    return {'topology': {
        'sites': objects.serialize(collection, mapping=API_TO_FACTS_MAP)}
    }

