#! /usr/bin/env python2.7
#
# Retrieve the running config from the NETCONF server passed on the
# command line using get-config and write the XML configs to files.
#

import sys, os, warnings, time
warnings.simplefilter("ignore", DeprecationWarning)
from ncclient import manager

response = 'response-edit-config-full.xml'

def demo(host, user):
    with manager.connect(host=host, port=830, username='cisco', password='cisco', hostkey_verify=False, timeout=120) as m, \
         open('192.168.30.125-config-module-list-20181018.txt', 'r') as config_list:
         config_module = config_list.readline().split('\n')[0]
         while config_module:
             print config_module
             c = m.edit_config(open(config_module, 'r').read(), format='xml', target='candidate', default_operation='merge')
             print c
             with open(response, 'w') as f:
                 f.write(str(c))

             c = m.commit()
             print c
             with open(response, 'a') as f:
                 f.write(str(c))

             config_module = config_list.readline().split('\n')[0]

if __name__ == '__main__':
    demo(sys.argv[1], os.getenv("USER"))
