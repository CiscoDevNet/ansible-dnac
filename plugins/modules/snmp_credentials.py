#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2019, Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible.module_utils.six import iteritems

from ansible_collections.ciscodevnet.ansible_dnac.plugins.module_utils import objects


READ_CONFIG_TO_API_MAP = objects.KeyMap(
    ('name', 'description'),
    ('community', 'readCommunity'),
    ('comments',)
)


WRITE_CONFIG_TO_API_MAP = objects.KeyMap(
    ('name', 'description'),
    ('community', 'writeCommunity'),
    ('comments',)
)


def main():
    """Main entry point for Ansible Module"""

    config_spec = {
        'name': dict(required=True),
        'community': dict(),
        'readwrite': dict(type='bool', default=False),
        'comments': dict()
    }

    argument_spec = {
        'config': dict(type='list', elements='dict', options=config_spec),
        'state': dict(choices=['present', 'absent'], default='present')
    }

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    connection = Connection(module._socket_path)

    state = module.params['state']

    config = {
        'readonly': list(),
        'readwrite': list()
    }

    for item in module.params['config']:
        access_type = 'readwrite' if item['readwrite'] is True else 'readonly'

        if item['community'] is None:
            item['community'] = item['name']

        config[access_type].append(item)

    result = {'changed': False}

    for key, value in iteritems(config):
        if key == 'readonly':
            subtype = 'SNMPV2_READ_COMMUNITY'
            config_map = READ_CONFIG_TO_API_MAP
        elif key == 'readwrite':
            subtype = 'SNMPV2_WRITE_COMMUNITY'
            config_map = WRITE_CONFIG_TO_API_MAP

        resp = connection.get('/api/v1/global-credential?credentialSubType={}'.format(subtype))
        resp = module.from_json(resp)

        # make sure the api response returned a dict object
        if not isinstance(resp, (dict, list)):
            module.fail_json(
                msg="invalid object type, got {}, expected one of {}".format(type(resp), ','.join((dict, list)))
            )

        # convert each object in the response to a typed object
        api_objects = [objects.ApiObject(o) for o in resp['response']]

        operations = objects.Operations(list(), list(), list())

        # If state is set to 'absent' and there is no configuration, just
        # simply remove all of the existing objects from the
        # server
        if not module.params['config']:
            operations.delete.extend(api_objects)

        else:
            for entry in value:
                config_spec.pop('readwrite', None)
                config_object = objects.ConfigObject(config_spec, entry)

                # Iterate over all of the `api_objects` and try to find a match
                # to the config_object.  If a match is found it will be set to
                # matched_object otherwise matched_object will be None
                match_rule = objects.matchattr('name', 'description')
                matched_object = objects.match(config_object, api_objects, (match_rule,))

                # If matched_object is None, there was no matching api_object found
                # in the list.  If the state param is set to present, flag the
                # config_object for creation
                if matched_object is None and state == 'present':
                    operations.post.append(config_object)

                # If a matched_object is found and state is set to absent, then the
                # matched_object needs to be deleted from the server
                elif matched_object and state == 'absent':
                    operations.delete.append(matched_object)

                # Finally if a matched_object is found and the state param is set
                # to "present" (default), check the fields for any changes and
                # add config_object to the edit change set
                elif matched_object:
                    module.warn("cannot update snmp credentials")
                    #obj = {
                    #    'id': matched_object.id,
                    #    'instanceUuid': matched_object.instanceUuid,
                    #    'instanceTenantId': matched_object.instanceTenantId,
                    #    'credentialType': matched_object.credentialType,
                    #    'description': config_object.name
                    #}

                    #if key == 'readonly':
                    #    obj['readCommunity'] = config_object.community
                    #elif key == 'readwrite':
                    #    obj['writeCommunity'] = config_object.community

                    #if config_object.comments is not None:
                    #    obj['comments'] = config_object.comments

                    #operations.put.append(objects.ConfigObject(obj, obj))

            # The url for is different depending on the access type
            base_url = '/dna/intent/api/v1/global-credential'

            if key == 'readonly':
                url = base_url + '/snmpv2-read-community'
            elif key == 'readwrite':
                url = base_url + '/snmpv2-write-community'

            result.update({'operation': dict(added=[], removed=[], modified=[])})

            for method in ('post', 'put', 'delete'):
                items = getattr(operations, method)
                if items:
                    if method == 'post':
                        if not module.check_mode:
                            data = objects.serialize(items, config_map)
                            connection.post(url, data=data)
                        result['changed'] = True
                        result['operation']['added'].extend([item.name for item in items])

                    elif method == 'put':
                        if not module.check_mode:
                            data = objects.serialize(items, config_map)
                            connection.put(url, data=data)
                        result['changed'] = True
                        result['operation']['modified'].extend([item.description for item in items])

                    elif method == 'delete':
                        for item in items:
                            if not module.check_mode:
                                connection.delete('/dna/intent/api/v1/global-credential/{}'.format(item.id))
                            result['changed'] = True
                            result['operation']['removed'].append(item.description)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
