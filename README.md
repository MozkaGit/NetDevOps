# Automated Configuration of Ethernet Interfaces and Default Routes using Ansible

The goal of this project is to automate the configuration of Ethernet interfaces for the Paris and Berlin headquarters routers, along with setting up default routes to enable seamless communication between the two sites. This automation is achieved using Ansible, a powerful configuration management and automation tool.

## Prerequisites

- Ansible server (mine is running on CentOS 7).
- Network lab set up in Eve-NG (Mine is hosted on a Google Cloud Platform (GCP) instance).
- Basic understanding of Ansible and networking concepts is recommended.

## Automated Configuration

To accomplish automated configuration, I created a dedicated Ansible role. This role contains tasks and templates to configure Ethernet interfaces and default routes on the Paris and Berlin headquarters routers.

## Project Files and Directory Structure

```
.
├── ansible.cfg # Config file for ansible
├── group_vars # Directory containing connection variables for the routers.
├── inventory.yml # File containing IP addresses of the routers.
├── network-management.yml # Main Ansible playbook that calls the role.
├── roles
└────└── ansible-network-routing-role
        ├── defaults # Directory containing defaults variables used by the role.
        ├── files # Directory containing vault encrypted password.
        ├── meta
        ├── tasks # Directory containing role-specific tasks.
        ├── tests
        └── vars
```

For a detailed look at directory structure, task definitions, and further technical details, refer to the actual files in the project repository.

## Lab topology

<img width="1066" alt="SCR-20230813-cagf" src="https://github.com/MozkaGit/ansible-network-routing/assets/43102748/f6f33f87-72a5-4ff1-ad8d-cc8f23fce1bc">

The network architecture comprises two routers, the Paris and Berlin headquarters routers, connected to each other via their eth0/1 interfaces. The eth0/2 interfaces are designated for their respective LANs. A Virtual PC Simulator (VPCS) is set up behind each router for ping tests post-configuration. The WAN network is 172.16.1.0/24, while Berlin's LAN is 192.168.1.0/24, and Paris's LAN is 192.168.2.0/24.

## Configuration Process

1. Minimal manual configuration: Initially, a minimal manual configuration must be applied to allow Ansible to use SSH on the router (in my case I use eth0/0 interfaces on each routers). You can use my start-up config files as inspiration for your initial configuration.
2. Ansible Automation: Ansible is used to automate the ip configuration of the routers interfaces (eth0/1 and eth0/2 in my case, as these are the interfaces through which communication occurs).
3. Berlin Router: The route configuration for Berlin involves adding the route "ip route 192.168.2.0 255.255.255.0 172.16.1.200".
4. Paris Router: The route configuration for Paris includes "ip route 192.168.1.0 255.255.255.0 172.16.1.100".

## Ansible Roles and Playbooks

- `routers-config.yml`: This task file handles the configuration of interfaces and routes for both routers.
- `backup-config.yml`: This task file performs show run commands and saves the output locally for backup purposes.
- `get-config.yml`: This task file retrieves the IOS version and shows IP interface brief.
- `main.yml`: This task file orchestrates the execution of the above playbooks using `include_tasks`.

## Execution

1. Clone this repository.
2. Customize files inside `hosts_vars` directory with the correct router IP addresses.
3. Customize `group_vars/routers.yml` with authentication details.
4. Customize the role according to your requirements by modifying the variables in `roles/defaults/main.yml/` to match the desired interface, ip address, route configuration or hosts etc.
5. Run the `network-management.yml` playbook to apply the role:
    ```
    ansible-playbook network-management.yml
    ```
    This playbook orchestrates the configuration role, applying the interface and route settings to the Paris and Berlin routers.
6. After the playbook execution, check the backup-config.yml playbook's output to ensure that configurations were successfully saved:
    ```
    ls roles/ansible-network-routing-role/files/backups/
    ```
    Additionally, you can verify if the content of backups files inside `backups` directory match your configurations files with `cat` command.
7. To test connectivity, connect directly to the VPCS via Eve-NG and perform a ping test. If you don't own a DHCP server you'll have to manually configure IP address and gateway on each VPCS : `VPCS> ip <ip_address/cidr> <gateway>` and then run the ping command.

    We can now confirm if the communication is set between the two sites:

The successful execution of the playbooks and the verification of the configurations will demonstrate the functionality of my Ansible role for automating the interface and route configurations.