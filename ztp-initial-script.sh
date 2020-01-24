#!/bin/bash

source ztp_helper.sh
config_file='/disk0:/ztp/tmp/config.txt'
config_log='/disk0:/ztp/customer/config-log.txt'

/bin/touch $config_log

if [ -f $config_file ]; then
  /bin/rm -f $config_file
else
  /bin/touch $config_file
fi

echo 'username cisco' >> $config_file
echo ' group root-lr' >> $config_file
echo ' group cisco-support' >> $config_file
echo ' secret cisco' >> $config_file
echo 'interface MgmtEth0/RP0/CPU0/0' >> $config_file
echo ' ipv4 address 192.168.30.125 255.255.255.0' >> $config_file
echo ' no shutdown' >> $config_file
echo 'netconf-yang agent' >> $config_file
echo ' ssh' >> $config_file
echo 'ssh server v2' >> $config_file
echo 'ssh server netconf vrf default' >> $config_file
xrapply_with_reason 'Initial ZTP config' $config_file

if [[ -z $(xrcmd "show crypto key mypubkey rsa") ]]; then
    echo "1024" | xrcmd "crypto key generate rsa"
else
    echo -ne "yes\n 2048\n" | xrcmd "crypto key generate rsa"
fi

xrcmd 'show running-config' >> $config_log
xrcmd 'show configuration failed' >> $config_log
xrcmd 'show crypto key mypubkey rsa' >> $config_log
