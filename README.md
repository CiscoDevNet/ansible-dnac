# ansible-dnac

The `ansible-dnac` project provides an Ansible collection for automating tasks
of the Cisco DNA Center server.  It provides a set of plugins and roles for
perfoming tasks against the DNA Center server.

Note: Please be sure to review the section on Running from source for 
instructions on how to install this role for development purposes

## Contributing

Contributions are strongly encourged from the Cisco DevNet community.  To 
contribute to this collection simply fork the project in Github, create a new
feature and/or bugfix branch, make your changes and submit a pull request.


## Running from source

This collection can be run from the source checkout.  Installing the collection
depends on what version of Ansible you are currenlty running.  Please note this 
installer should be used in local development environments and is not designed 
to replace the offical Ansible installer.   


### Ansible 2.8 or later

To install the collection issue the following command:

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



### Ansible 2.7 or earlier

For Ansible versions prior to 2.8, you need to build the collection into a 
role first.   To build the role, use the provided installer playbook by issuing 
the following command on your local system.

```make build-role```

This command will create an installable tarball that can be used to install the
collection as a role into your device roles path.  

Once the role has been successfully built, install the role with the following
command on your local system.

```make install-role```

Note: When building the collection as a role removes the namespace support so 
modules will be referenced with `dnac_`.  For instance instead of calling 
`ciscodevnet.ansible_dnac.devices` it will now be `dnac_devices`.  You will also
need to import the role using the playbooks import directive.

```
---
- hosts: dnac
  gather_facts: no

  roles:
    - ciscodevnet.dnac

  tasks:
    - name: add devices to inventory
      dnac_devices:
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
