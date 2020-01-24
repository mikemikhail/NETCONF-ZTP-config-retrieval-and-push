#! /usr/bin/env python
# Reads XR device configuration to a file
# mamikhai@cisco.com

import sys, os, warnings, re
warnings.simplefilter("ignore", DeprecationWarning)
from ncclient import manager
import time
from datetime import datetime

# target NETCONF server
server = '172.16.7.112'

logfile = 'get_config.log'
tracefile = 'get_config.trace.log'

cap_cnf_file = server + '-cap-cnf-' + str(datetime.now().strftime('%Y%m%d')) + '.xml'

user ='cisco'
password ='cisco'

def my_unknown_host_cb(host, fingerprint):
    return True

if __name__ == '__main__':
    with manager.connect(host=server, port=830, username=user, password=password, look_for_keys=False, \
            hostkey_verify=False, unknown_host_cb=my_unknown_host_cb) as m:

        config_full_file = server + '-config-full-' + str(datetime.now().strftime('%Y%m%d')) + '.xml'
        config = m.get_config(source='running').data_xml
        with open(config_full_file, 'w') as f:
            f.write(config)
        f.close()

        modules_full_file = server + '-modules-full-' + str(datetime.now().strftime('%Y%m%d')) + '.xml'
        modules_config_file = server + '-modules-config-' + str(datetime.now().strftime('%Y%m%d')) + '.xml'
        modules_non_config_file = server + '-modules-non-config-' + str(datetime.now().strftime('%Y%m%d')) + '.xml'

        with open(modules_full_file, 'w') as modules_full, open(modules_config_file, 'w') as modules_config, \
             open(modules_non_config_file, 'w') as modules_non_config, open(config_full_file, 'r') as config_full:
            for line in config_full:
                if re.match(r'^  <[^/]', line):
                    modules_full.write(line)
                    if re.match(r'^  <[^/].*cisco\.com.*cfg', line):
                        modules_config.write(re.sub('>', ' />', line))
                    else:
                        modules_non_config.write(line)
        config_list_file = server + '-config-module-list-' + str(datetime.now().strftime('%Y%m%d')) + '.txt'

        with open(modules_config_file, 'r') as modules, open(config_list_file, 'w')  as config_list:
            module = modules.readline()
            while module:
                filter_file = server + '-config-filter-' + (module.partition('<')[2]).partition(' xmlns')[0] + '-' + str(datetime.now().strftime('%Y%m%d')) + '.xml'
                with open(filter_file, 'w') as f:
                    f.write('<filter>\n')
                    f.write(module)
                    f.write('</filter>')

                config_module_file = server + '-config-module-' + (module.partition('<')[2]).partition(' xmlns')[0] + '-' + str(datetime.now().strftime('%Y%m%d')) + '.xml'
                config_list.write(config_module_file + '\n')
                with open(config_module_file, 'w') as f:
#                    f.write('<config>\n')
                    c = m.get_config(source='running', filter=open(filter_file, 'r').read()).data_xml
                    c = re.sub(r'<\?xml.*>', '<config>', c)
                    c = re.sub(' </data>', '</config', c)
                    f.write(c)
#                    f.write('</config>')
                    module = modules.readline()
