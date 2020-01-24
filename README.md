# NETCONF-ZTP-config-retieval-and-push
Scripts for CLI-free ZTP provision, golden config read/push/verify

--------

ztp-initial-script.sh

to be pointed to by DHCP service, with http/s pointer. When received by new XR instance/router, an rsa key is generated, ssh and netconf enabled, and an interface configured and unshut. Making the new router ready for NETCONF config.

--------

get-config.py

Use to read running config. It generates:

172.16.7.112-config-full-20200123.xml    full configuration

172.16.7.112-modules-full-20200123.xml    list of configured models

172.16.7.112-modules-config-20200123.xml    list of configured native models, to be used for config push

172.16.7.112-modules-non-config-20200123.xml    list of "other" models

172.16.7.112-config-filter-aaa-20200123.xml    get-config filter used to retrieve each native model configuration

172.16.7.112-config-module-aaa-20200123.xml    retrieved configuration of each native model

--------

edit-config-full.py

Uses the above to push model configuration to router, one by one. Generates response:

response-edit-config-full.xml

--------

Suggest adding a functionality checklist, to be pulled also using NETCONF a few minutes after ok provisioning. To verify that control and forwarding are functional. Such as minimum number of iBGP with RRs, minimum number of prefixes for each address family, interface state, etc.
