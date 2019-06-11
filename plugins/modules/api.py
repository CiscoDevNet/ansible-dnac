#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2019, Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection


def main():
    """Main entry point for Ansible Module"""

    argument_spec = {
        'url': dict(required=True)
    }

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    connection = Connection(module._socket_path)

    result = {'changed': False}

    resp = connection.get(module.params['url'])
    result.update({'output': module.from_json(resp)})

    module.exit_json(**result)

if __name__ == '__main__':
    main()
