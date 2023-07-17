#!/usr/local/bin/python3

import sys
import os
import re
import sippyapi.db
from sippyapi.log.StderrLogger import StderrLogger
from sippyapi.misc.ClusterConf import ClusterConf


def insert_ip():
    sys.stdout.write("Please enter a new IP address:")
    sys.stdout.flush()
    val = sys.stdin.readline().strip()
    if val == "":
        print("ERROR: empty IP")
        insert_ip()
    is_correct = bool(re.match('[0-9.]+$'  , val))
    if not is_correct:
        sys.stdout.write("ERROR: Not a valid IP ADDRESS! Check your input. ")
        sys.stdout.flush()
        val = insert_ip()
    return val

def insert_mask():
    sys.stdout.write("Please enter a NETWORK MASK:")
    sys.stdout.flush()
    val = sys.stdin.readline().strip()
    if val == "":
        print("ERROR: empty MASK")
        insert_mask()
    is_correct = bool(re.match('[0-9.]+$'  , val))
    if not is_correct:
        sys.stdout.write("ERROR: Not a valid MASK! Check your input. ")
        sys.stdout.flush()
        val = insert_mask()
    return val

def insert_iface():
    sys.stdout.write("Please enter a NETWORK INTERFACE:")
    sys.stdout.flush()
    val = sys.stdin.readline().strip()
    if val == "":
        print("ERROR: empty MASK")
        insert_iface()
    is_correct = bool(re.match('[a-zA-Z0-9]+$'  , val))
    if not is_correct:
        sys.stdout.write("ERROR: Not a valid INTERFACE! Check your input. ")
        sys.stdout.flush()
        val = insert_iface()
    return val

def main():

    ip = insert_ip()

    mask = insert_mask()

    iface = insert_iface()

    with open('/SSP_ID') as f:
         node = f.readline().strip()
    f.close()

    root_cl_conf = ClusterConf(1)
    logger = StderrLogger()
    root_dbconf = sippyapi.db.Config(logger, i_environment = 1, autocommit = True)
    root_dbconf.user = root_cl_conf.pgsql_user # Connect as superuser
    root_db = sippyapi.db.ConnectionWrapper(root_dbconf, autoreconnect = False)

    root_db.execute("insert into net_addresses (name, description, i_environment, node, iface, ip, netmask, i_net, active) values ('new', 'new', '1', '%s' , '%s', '%s', '%s', '1', 't');" %(node, iface, ip, mask))

if __name__ == '__main__':
    main()

