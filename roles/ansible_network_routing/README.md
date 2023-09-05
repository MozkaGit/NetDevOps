[![Push to Galaxy](https://github.com/MozkaGit/Ansible_NetDevOps_role/actions/workflows/push_to_galaxy.yml/badge.svg)](https://github.com/MozkaGit/Ansible_NetDevOps_role/actions/workflows/push_to_galaxy.yml)

Ansible NetDevOps
=========

This Ansible role, `ansible_netdevops_role`, automates the initial configuration and maintenance of Cisco routers in a network. It focuses on configuring WAN and LAN interfaces, setting up IP routes based on the router's hostname, executing commands, and capturing and saving the router's running configuration. This role is designed to simplify network management tasks.

1. Replace Interface Configuration: It replaces the device configuration for specified interfaces, enabling them and setting their descriptions. This is done for both WAN and LAN interfaces.

2. Configure IP Routes: After configuring the interfaces, the playbook configures IP routes on the routers based on the router's hostname

3. Execute Commands: The playbook runs several commands on the routers using the `cisco.ios.ios_command` module. It retrieves the IOS version, displays a brief overview of IP interfaces, and captures the router's running configuration.

4. Print and Save Output: The output of the executed commands is registered, printed for debugging purposes, and saved to a specified destination. This allows for documentation and backup of the router's configuration.

In summary, this role automates the initial configuration and maintenance of Cisco routers in a network, focusing on interfaces and routing, and it collects and saves relevant information for future reference.

Role Variables
--------------

- `first_rtr`: The name of the first router.

- `second_rtr`: The name of the second router.
- `first_wan_interface`: The WAN interface for the first router.
- `first_lan_interface`: The LAN interface for the first router.
- `second_wan_interface`: The WAN interface for the second router.
- `second_lan_interface`: The LAN interface for the second router.
- `first_wan_ip_subnet`: The subnet for the WAN interface of the first router.
- `first_lan_ip_subnet`: The subnet for the LAN interface of the first router.
- `second_wan_ip_subnet`: The subnet for the WAN interface of the second router.
- `second_lan_ip_subnet`: The subnet for the LAN interface of the second router.
- `first_wan_ip_test`: Test IP address for the first WAN interface.
- `first_lan_ip_test`: Test IP address for the first LAN interface.
- `second_wan_ip_test`: Test IP address for the second WAN interface.
- `second_lan_ip_test`: Test IP address for the second LAN interface.
- `first_ip_route`: IP route configuration for the first router.
- `second_ip_route`: IP route configuration for the second router.
- `backups_destination`: Destination path for saving router configuration backups.

Dependencies
----------------

None.

Example Playbook
----------------

    - hosts: all
      roles:
         - mozkagit.ansible_netdevops_role

License
-------

MIT / BSD

Author Information
------------------

This role was created by MozkaGit.
