#! /usr/bin/env python2.7
#
# Retrieve the running config from the NETCONF server passed on the
# command line using get-config and write the XML configs to files.
#

import sys, os, warnings, time
warnings.simplefilter("ignore", DeprecationWarning)
from ncclient import manager

response = '172.16.7.112-response-edit-config-full.xml'

def my_unknown_host_cb(host, fingerprint):
    return True

def conf(host, user):
    with manager.connect(host=host, port=830, username='cisco', password='cisco', look_for_keys=False, unknown_host_cb=my_unknown_host_cb, hostkey_verify=False, timeout=120) as m, \
         open('172.16.7.112-config-module-list-20210308.txt', 'r') as config_list:
         config_module = config_list.readline().split('\n')[0]
         while config_module:
             print config_module
             c = m.edit_config(open(config_module, 'r').read(), format='xml', target='candidate', default_operation='merge')
             print c
             with open(response, 'a') as f:
                 f.write(config_module)
                 f.write(str(c))

             c = m.commit()
             print c
             with open(response, 'a') as f:
                 f.write(str(c))

             config_module = config_list.readline().split('\n')[0]

if __name__ == '__main__':
    conf(sys.argv[1], os.getenv("USER"))
