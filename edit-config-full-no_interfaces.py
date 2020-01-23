#! /usr/bin/env python2.6
#
# Retrieve the running config from the NETCONF server passed on the
# command line using get-config and write the XML configs to files.
#
# $ ./nc02.py broccoli

import sys, os, warnings
warnings.simplefilter("ignore", DeprecationWarning)
from ncclient import manager

response = 'response-edit-config-full-no_interfaces.xml'

def demo(host, user):
    with manager.connect(host=host, port=22, username='cisco', password='cisco', hostkey_verify=False) as m:
                    c = m.edit_config(open('config-10.101.125.1-no_interfaces.xml', 'r').read(), format='xml', target='candidate', default_operation='merge')
                    with open(response, 'w') as f:
                        f.write(str(c)) 
                    c = m.commit()
                    with open(response, 'a') as f:
                        f.write(str(c))

if __name__ == '__main__':
    demo(sys.argv[1], os.getenv("USER"))
