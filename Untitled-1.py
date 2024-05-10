from pysnmp.hlapi import *

def get_snmp_data(oid, target_ip, community='public', port=161):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=0),
        UdpTransportTarget((target_ip, port)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )
    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print(f"{errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or '?'}")
    else:
        for varBind in varBinds:
            return varBind[1]

def discover_network_topology(device_ip_list):
    # OID for device ID and to get connected device details
    sysDescr = '1.3.6.1.2.1.1.1.0'  # System Description
    sysName = '1.3.6.1.2.1.1.5.0'  # System Name

    network_topology = {}

    for ip in device_ip_list:
        device_info = {}
        device_info['sysDescr'] = str(get_snmp_data(sysDescr, ip))
        device_info['sysName'] = str(get_snmp_data(sysName, ip))
        network_topology[ip] = device_info

    return network_topology
device_ips = ['192.168.1.1', '192.168.1.2']  # List of device IPs in your network
topology = discover_network_topology(device_ips)
print("Network Topology:", topology)
