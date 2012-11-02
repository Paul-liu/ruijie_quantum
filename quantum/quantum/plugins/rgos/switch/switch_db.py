#
#/*
# * db.py
# * Original Author:  liupu@ruijie.com.cn, 2012-7-30
# *
# *
# * History
# */

import logging
import quantum.plugins.rgos.switch 
from quantum.plugins.rgos.db import rgos_db

LOG = logging.getLogger(__name__)

def mac_converter(mac):
    '''
    Conversion MAC, for example:
    mac: '1234.5678.9abc'
    return 12:34:56:78:9a:bc
    '''
    tmp = []
    tmp.append(mac[0:2])
    tmp.append(mac[2:4])
    tmp.append(mac[5:7])
    tmp.append(mac[7:9])
    tmp.append(mac[10:12])
    tmp.append(mac[12:14])
    sign = ':'
    return sign.join(tmp)

def get_all_port_neighbors():
    """Lists all the switch:port and neighbors data """
    pass



def get_port_neighbors(svi, ifx):
    """Lists a switch:port and neighbors data """
    pass



def add_port_neighbors(svi, neighbor_list):
    """Adds a switch:port and neighbors data"""
    print 'add_port_neighbors start! \r\n'
    mac = ''
    # set the rgos switch ip by svi
    ip = svi
    print 'add_port_neighbors ip = %s \r\n' % ip,
    
    # set the port and mac  
    for i in neighbor_list:
        neighbor_tuple = i
        port = neighbor_tuple[0]
        print 'add_port_neighbors port = %s \r\n' % port,
        
        if neighbor_tuple[2] != 'MAC address':
            print 'add_port_neighbors not mac = %s \r\n' % neighbor_tuple[2],
            continue
        else:
            mac = neighbor_tuple[3]
            print 'add_port_neighbors mac = %s \r\n' % mac,
            # set switch port neighbors info to local db
            mac_tmp = mac_converter(mac)
            print ('=============> add sw eth bind: %s %s %s' % (ip, mac_tmp, port))
            rgos_db.add_ruijie_switch_eth_binding(ip, mac_tmp, port)
    print 'add_port_neighbors end! \r\n'

def remove_port_neighbors(svi, ifx):
    """Removes a switch:port and neighbors data"""
    pass


def update_port_neighbors(svi, neighbor_list):
    """Updates switch:port and neighbors data"""
    pass


def add_hostinfo(index, sshhost, sshport, retry, reconnect):
    """Add a switch:port cfg"""
    idx = index
    ip = sshhost
    port = sshport
    rgos_db.set_ruijie_switch_host_cfg( idx, ip, port, retry, reconnect)
    pass

def update_hostinfo(index, sshhost, sshport, retry, reconnect):
    """Updates switch:port cfg"""
    idx = index
    ip = sshhost
    port = sshport
    rgos_db.set_ruijie_switch_host_cfg( idx, ip, port, retry, reconnect )
    pass

def remove_hostinfo(index):
    """Removes a switch info """
    idx = index
    rgos_db.remove_ruijie_switch_host_cfg( idx )
    pass

def get_hostinfo( ):
    """Gets a all host cfg info"""
    switch_server_hostcfg = rgos_db.get_ruijie_switch_allhost_cfg( )
    if switch_server_hostcfg == []:
        print '##########get_hostinfo is null !\r\n'
    else:
        print '##########get_hostinfo is %s \r\n' % switch_server_hostcfg,
    return switch_server_hostcfg

def get_hostinfo_byhost(sshhost):
    """Gets a user info"""
    host = sshhost
    switch_server_hostcfg = rgos_db.get_ruijie_switch_host_cfg( host )
    if switch_server_hostcfg == []:
        print '##########get_hostinfo_byhost is null with host %s \r\n' % host,
    else:
        print '##########get_hostinfo_byhost is %s \r\n' % switch_server_hostcfg,
    return switch_server_hostcfg

def get_sshserver_id(sshhost):
    print '##########get_sshserver_id sshhost = %s \r\n' % sshhost,
    switch_server_hostcfg = get_hostinfo_byhost(sshhost)
    host_id = switch_server_hostcfg[0].host_id
    print '##########get_sshserver_id id = %s \r\n' % host_id,

    return host_id

def add_userinfo(index, username, password):
    """Add a user auth cfg"""

    idx = index
    user = username
    passwd = password
    rgos_db.set_ruijie_switch_user_cfg( idx, user, passwd )
    pass

def update_userinfo(index, username, password):
    """Updates sser auth cfg"""
    idx = index
    user = username
    passwd = password
    rgos_db.set_ruijie_switch_user_cfg( idx, user, passwd)
    pass

def remove_userinfo(index):
    """Removes a user info"""
    idx = index
    rgos_db.remove_ruijie_switch_user_cfg( idx )
    pass

def get_userinfo(index):
    """Gets a user info"""
    idx = index
    switch_server_usercfg = rgos_db.get_ruijie_switch_user_cfg( idx )
    if switch_server_usercfg == []:
        print '##########get_userinfo is null with id %s! \r\n' % idx,
    else:
        print '##########get_userinfo is %s! \r\n' % switch_server_usercfg,

    return switch_server_usercfg

