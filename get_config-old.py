#! /usr/bin/env python
# Reads XR device configuration to a file
# mamikhai@cisco.com

import sys, os, warnings
warnings.simplefilter("ignore", DeprecationWarning)
from ncclient import manager
import time
from datetime import datetime

# target NETCONF server
server = '10.101.125.1'

logfile = 'get_config.log'
tracefile = 'get_config.trace.log'

user ='cisco'
password ='cisco'

ns_filter = '''
            <filter>
              <router-static xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ip-static-cfg" />
              <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg" />
            </filter>
            '''

def check_oper(subtree_filter, response, trace_string, count_string):
    count = 0
    trace = open(tracefile,'a')
    op_time = str(datetime.now())
    trace.write(op_time + ' ' + str(trace_string) + ' ' + str(count_string) + '\n')
    
    # Get data, record
    c = m.get(filter = ('subtree', open(subtree_filter, 'r').read()))
    with open(response, 'w') as f:
        f.write(str(c))
    # Check for target data, record, count
    with open(response, 'r') as f:
        for line in f:
            if trace_string and (trace_string in line):
                trace.write(line)
            if count_string in line:
                count +=1
    trace.close()
    return count

if __name__ == '__main__':
    with manager.connect(host=server, port=830, username=user, password=password, hostkey_verify=False) as m:
        c = m.get_config(source='running', filter=ns_filter).data_xml
        with open(server+'-config-'+str(datetime.now().strftime('%Y%m%d%H%M%S'))+'.xml', 'w') as f:
            f.write(c)
        f.close()

