# ansible-dnac

The `ansible-dnac` project provides an Ansible collection for automating tasks
of the Cisco DNA Center server.  It provides a set of plugins and roles for
perfoming tasks against the DNA Center server.

Note: This is a collection and therefore it requires Ansible 2.8 or later in 
order to work properly.


## Example Playbook

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


## Running from source

This collection provides a basic installer for setting up the collection to run
in your local development environment.  Please note this installer should be 
used in local development environments and is not designed to replace the 
offical Ansible installer.   

To install the collection issue the following command:

```make install```

This command will install the collection to the local users Ansible collections
path at ```~/.ansible/collections/ansible_collections/ciscodevnet/ansible_dnac```

To uninstall the collection issue the command:

```make uninstall```


## License

GPLv3

## Contributors

* Peter Sprygada (privateip) <psprygad@redhat.com>
