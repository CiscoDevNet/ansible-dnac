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


CONFIG_TO_API_MAP = objects.KeyMap(
    ('name', 'description'),
    ('username',),
    ('password',),
    ('port',),
    ('secure',),
    ('comments',),
    ('credential_type', 'credentialType', lambda x: 'GLOBAL')
)


def main():
    """Main entry point for Ansible Module"""

    config_spec = {
        'name': dict(required=True),

        'username': dict(required=True),
        'password': dict(no_log=True, required=True),

        'port': dict(type='int', required=True),
        'secure': dict(type='bool'),

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
        config[access_type].append(item)

    result = {'changed': False}

    for key, value in iteritems(config):
        if key == 'readonly':
            subtype = 'HTTP_READ'
        elif key == 'readwrite':
            subtype = 'HTTP_WRITE'

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
                    module.warn("cannot update http credentials")

            # The url for is different depending on the access type
            base_url = '/dna/intent/api/v1/global-credential'

            if key == 'readonly':
                url = base_url + '/http-read'
            elif key == 'readwrite':
                url = base_url + '/http-write'

            result.update({'operation': dict(added=[], removed=[], modified=[])})

            for method in ('post', 'put', 'delete'):
                items = getattr(operations, method)
                if items:
                    if method == 'post':
                        if not module.check_mode:
                            data = objects.serialize(items, CONFIG_TO_API_MAP)
                            connection.post(url, data=data)
                        result['changed'] = True
                        result['operation']['added'].extend([item.name for item in items])

                    elif method == 'put':
                        if not module.check_mode:
                            data = objects.serialize(items, CONFIG_TO_API_MAP)
                            connection.put(url, data=data)
                        result['changed'] = True
                        result['operation']['modified'].extend([item.name for item in items])

                    elif method == 'delete':
                        for item in items:
                            if not module.check_mode:
                                connection.delete('/dna/intent/api/v1/global-credential/{}'.format(item.id))
                            result['changed'] = True
                            result['operation']['removed'].append(item.description)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
