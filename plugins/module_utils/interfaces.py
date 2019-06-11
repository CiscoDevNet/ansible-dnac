# -*- coding: utf-8 -*-

# (c) 2019, Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.connection import Connection

from ansible_collections.ciscodevnet.ansible_dnac.plugins.module_utils import objects


API_TO_FACTS_MAP = objects.KeyMap(
    objects.mapped_key('adminstatus', 'enabled', lambda x: x == 'UP'),
    objects.mapped_key('description'),
    objects.mapped_key('duplex'),
    objects.mapped_key('id'),
    objects.mapped_key('ifIndex', 'ifindex', lambda x: int(x) if x else None),
    objects.mapped_key('interfaceType', 'interface_type'),
    objects.mapped_key('ipv4Address', 'ipv4_address'),
    objects.mapped_key('ipv4Mask', 'ipv4_mask'),
    objects.mapped_key('isisSupport', 'isis_supported', lambda x: bool(x)),
    objects.mapped_key('lastUpdated', 'last_updated'),
    objects.mapped_key('macAddress', 'macaddress'),
    objects.mapped_key('mappedPhysicalInterfaceName', 'name'),
    objects.mapped_key('mediaType', 'media_type'),
    objects.mapped_key('nativeVlanid', 'native_vlan_id'),
    objects.mapped_key('ospfSupport', 'ospf_support', lambda x: bool(x)),
    objects.mapped_key('pid'),
    objects.mapped_key('portMode', 'port_mode'),
    objects.mapped_key('portName', 'port_name'),
    objects.mapped_key('portType', 'port_type'),
    objects.mapped_key('serialNo', 'serialnum'),
    objects.mapped_key('series'),
    objects.mapped_key('status', 'oper_status'),
    objects.mapped_key('vlanId', 'vlan_id', lambda x: int(x) if x else None),
    objects.mapped_key('voiceVlan', 'voice_vlan', lambda x: int(x) if x else None)
)


def get(module):
    connection = Connection(module._socket_path)
    resp = connection.get('/dna/intent/api/v1/interface')
    resp = module.from_json(resp)
    resp = resp['response']

    # make sure the api response returned a dict object
    if not isinstance(resp, (dict, list)):
        module.fail_json(
            msg="invalid object type, got {}, expected one of {}".format(type(resp), ','.join((dict, list)))
        )

    return [objects.ApiObject(o) for o in resp]


def get_facts(module):
    collection = get(module)
    return {'devices': objects.serialize(collection, mapping=API_TO_FACTS_MAP)}
