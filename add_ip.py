#!/usr/local/bin/python3

import sys
import sippyapi.db
import ipaddress
import subprocess
from sippyapi.log.StderrLogger import StderrLogger
from sippyapi.misc.ClusterConf import ClusterConf


def get_ip_and_mask():
    sys.stdout.write("Please enter a new IP address:")
    sys.stdout.flush()
    try:
        ip = ipaddress.ip_address(sys.stdin.readline().strip())
    except ValueError:
        print("ERROR: IP address is not valid! ")
        sys.exit()
    sys.stdout.write("Please enter a NETWORK MASK:")
    sys.stdout.flush()
    mask =  sys.stdin.readline().strip()
    try:
        ipaddress.ip_network('%s/%s' % (ip, mask), False)

    except ValueError:
        print("ERROR: NETWORK MASK is not valid! ")
        sys.exit()
    return ip, mask

def get_iface():
    sys.stdout.write("Please enter a NETWORK INTERFACE:")
    sys.stdout.flush()
    val = sys.stdin.readline().strip()
    try:
        subprocess.check_output(["ifconfig %s" % val], shell=True)
    except:
        print("ERROR: No such interface ")
        sys.exit()
    return val

def main():

    ip_and_mask = get_ip_and_mask()
    ip, mask = ip_and_mask[0], ip_and_mask[1]
    iface = get_iface()

    with open('/SSP_ID') as f:
         node = f.readline().strip()
    f.close()

    root_cl_conf = ClusterConf(1)
    logger = StderrLogger()
    root_dbconf = sippyapi.db.Config(logger, i_environment = 1, autocommit = True)
    root_dbconf.user = root_cl_conf.pgsql_user # Connect as superuser
    root_db = sippyapi.db.ConnectionWrapper(root_dbconf, autoreconnect = False)

    root_db.execute("insert into net_addresses (name, description, i_environment, node, "
                    "iface, ip, netmask, i_net, active) values ('new', 'new', '1', '%s' "
                    ", '%s', '%s', '%s', '1', 't');" %(node, iface, ip, mask))

if __name__ == '__main__':
    main()
