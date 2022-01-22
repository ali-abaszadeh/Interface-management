# Get and set interface
interface_name='enp4s0'
new_ip='192.168.40.135'
new_gateway='192.168.40.1'
#new_gateway=''

# Get all interfaces and IPv4 addresses.
def get_interface1():
    try:
        # interface method return interface names, ifaddresses method return ip address info
        # and AF_INET method return key,values for (addr,netmask,peer,port) and AF_LINK method return key,value for(addr,MAC)
        from netifaces import interfaces, ifaddresses, AF_INET, AF_LINK
        # to not take into account loopback addresses (no interest here)
        interface_info = []
        for interface in interfaces():
            config = ifaddresses(interface)
            # AF_INET is not always present
            if AF_INET in config.keys():
                for link in config[AF_INET]:
                    for link1 in config[AF_LINK]:
                    # loopback holds a 'peer' instead of a 'broadcast' address
                    #if 'addr' in link.keys() and 'peer' not in link.keys():
                        interface_info.append(interface)
                        interface_info.append(link['addr'])
                        interface_info.append(link['netmask'])
                        # Return MAC Address
                        interface_info.append(link1['addr'])
        return '  '.join(interface_info)
    except ImportError:
        print("Unable to get IPV4")
        return []


# This function get interface, IPv4, IPv6, netmask and brodcast for each eth.
def get_interface2():
    import ifcfg
    for name, interface in ifcfg.interfaces().items():
        # do something with interface
        print(interface['device'])
        print(interface['inet'])  # First IPv4 found
        print(interface['inet4'])  # List of ips
        print(interface['inet6'])
        print(interface['netmask'])
        print(interface['broadcast'])


# This function set IP and Gateway in Netplan configuration file.
# pip install pyyaml needed
def set_interface(interface_name,new_ip,new_gateway):
    import os
    import yaml

    new_ip1 = [f'{new_ip}/24']
    dhcp_value = 'no'
    netplan_path = '/etc/netplan/'
    netplan_path1 = ''
    files = []

    # Find .yaml files
    # r=root, d=directories, f = files
    for r, d, f in os.walk(netplan_path):
        for file in f:
            if '.yaml' in file:
                files.append(os.path.join(r, file))
    # Find Netplan configuration path
    for item in files:
        netplan_path1 = item
        print(netplan_path1)
    # Backup from Netplan configuration file in /etc/netplan/ with netplan.bak name before changing it
    os.system('sudo -i cp ' + netplan_path1 + ' /etc/netplan/netplan.bak')
    # Read and set changes in Netplan file
    # Load YAML file in dictionary format
    with open(netplan_path1, 'r') as file:
        documents = yaml.full_load(file)
        #print(documents)
        del documents['network']['ethernets']['enp4s0']['addresses']
        #default_gateway = documents['network']['ethernets']['enp4s0']['gateway4']
        documents['network']['ethernets']['enp4s0']['dhcp4']=dhcp_value
        documents['network']['ethernets']['enp4s0']['dhcp6']=dhcp_value
        documents['network']['ethernets']['enp4s0']['addresses']=new_ip1
        if new_gateway != '':
            del documents['network']['ethernets']['enp4s0']['gateway4']
            documents['network']['ethernets']['enp4s0']['gateway4']=new_gateway
        print(documents['network']['ethernets']['enp4s0']['gateway4'])
        print(documents['network']['ethernets']['enp4s0']['addresses'])
    # Come back dictionary to YAML
    with open(netplan_path1, 'w') as file:
         documents = yaml.dump(documents, file)
    # Run "netplan apply" command for finalizing task.
    os.system('sudo -i netplan generate')
    os.system('sudo -i netplan apply')
 



def main():
    #get_interface1()
    set_interface(interface_name,new_ip,new_gateway)
    #get_interface2()


if __name__ == '__main__':
    main()
