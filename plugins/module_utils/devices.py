# -*- coding: utf-8 -*-

# (c) 2019, Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.connection import Connection

from ansible_collections.ciscodevnet.ansible_dnac.plugins.module_utils import objects


DEVICE_TYPE = {
    'network': 'NETWORK_DEVICE'
}


CONFIG_TO_API_MAP = objects.KeyMap(
    ('address', 'ipAddress', lambda x: [x]),
    ('enable_password', 'enablePassword'),
    ('transport', 'cliTransport'),
    ('snmp_ro_community', 'snmpROCommunity'),
    ('snmp_rw_community', 'snmpRWCommunity'),
    ('snmp_retries', 'snmpRetries'),
    ('snmp_timeout', 'snmpTimeout'),
    ('snmp_version', 'snmpVersion'),
    ('username', 'userName'),
    ('type', 'type', lambda x: DEVICE_TYPE[x])
)


API_TO_FACTS_MAP = objects.KeyMap(
    objects.mapped_key('hostname'),
    objects.mapped_key('id'),
    objects.mapped_key('interfaceCount', 'interface_count'),
    objects.mapped_key('lineCardCount', 'linecard_count'),
    objects.mapped_key('location'),
    objects.mapped_key('macAddress', 'macaddress'),
    objects.mapped_key('managementIpAddress', 'address'),
    objects.mapped_key('memorySize', 'memory'),
    objects.mapped_key('platformId', 'platform'),
    objects.mapped_key('role', transform=lambda x: x.lower()),
    objects.mapped_key('serialNumber', 'serialnum'),
    objects.mapped_key('series'),
    objects.mapped_key('snmpContact', 'snmp_contact'),
    objects.mapped_key('snmpLocation', 'snmp_location'),
    objects.mapped_key('softwareType', 'software_type'),
    objects.mapped_key('softwareVersion', 'software_version'),
    objects.mapped_key('type'),
    objects.mapped_key('upTime', 'uptime')
)


def get(module):
    connection = Connection(module._socket_path)
    resp = connection.get('/dna/intent/api/v1/network-device')
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
