# ansible-dnac

The `ansible-dnac` project provides an Ansible collection for automating tasks
of the Cisco DNA Center server.  It provides a set of plugins and roles for
perfoming tasks against the DNA Center server.

Note: This collection is not compatible with versions of Ansible before 2.8


## Requirements

* Ansible 2.8 or later
* Cisco Intent API 1.2 or later


## Contributing

Contributions are strongly encourged from the Cisco DevNet community.  To 
contribute to this collection simply fork the project in Github, create a new
feature and/or bugfix branch, make your changes and submit a pull request.


## Running from source

This collection can be run from the source checkout.  To install the 
collection issue the following command:

```make install```

This command will install the collection to the local users Ansible collections
path at ```~/.ansible/collections/ansible_collections/ciscodevnet/ansible_dnac```

To uninstall the collection issue the command:

```make uninstall```

Once the collection is installed, you can use it in a playbook by specifying 
the full namespace path to the module, plugin and/or role. 

```
---
- hosts: dnac
  gather_facts: no

  tasks:
    - name: add devices to inventory
      ciscodevnet.ansible_dnac.devices:
        config:
          - address: 1.2.3.4
            username: ansible
            password: ansible
            snmp_ro_community: public
            snmp_rw_community: private
          - address: 5.6.7.8
            username: ansible
            password: ansible
            snmp_ro_community: public
            snmp_rw_communit
      state: present
```


## License

GPLv3


## Contributors

* Peter Sprygada (privateip) <psprygad@redhat.com>
