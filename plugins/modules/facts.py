# -*- coding: utf-8 -*-

# (c) 2019, Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.common.utils import dict_merge

from ansible_collections.ciscodevnet.ansible_dnac.plugins.module_utils import collectors

COLLECTORS = frozenset([
    'sites',
    'devices',
    'interfaces'
])


def main():
    """Main entry point for Ansible Module"""

    argument_spec = {
        'gather_subset': dict()
    }

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    result = {'changed': False}

    facts = {}

    for name in COLLECTORS:
        loader = getattr(collectors, name)
        facts = dict_merge(facts, loader.get_facts(module))

    result['ansible_facts'] = facts

    module.exit_json(**result)


if __name__ == '__main__':
    main()
