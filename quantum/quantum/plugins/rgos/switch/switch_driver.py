import socket
import string
import logging
from quantum.plugins.rgos.ssh import sshclient
from quantum.plugins.rgos.switch import switch_db
from quantum.plugins.rgos.switch import switch_api
from quantum.plugins.rgos.db import rgos_db
from quantum.plugins.rgos.vlan import vlan_mgr

LOG = logging.getLogger(__name__)

def parse_recived_message(recv_str, cli):

    if len(recv_str) == 0:
        print 'parse_recived_message para erro: recv_str !'
        return -1

    if len(cli) == 0:
        print 'parse_recived_message para erro: cli !'
        return -1

    # parse the recive message by cli type
    if cli == 'show lldp neighbors detail \r\n':
        # get the neighor mac & local interface info in recv message
        print 'parse_recived_message get_lldp_neighbor start \r\n'
        ret = get_lldp_neighbor_details(recv_str)
        if ret == -1:
            print 'parse_recived_message get_lldp_neighbor erro end! \r\n'
            
    if cli == 'show lldp neighbors \r\n':
        # get the neighor mac & local interface info in recv message
        print 'parse_recived_message get_lldp_neighbor start \r\n'
        ret = get_lldp_neighbor(recv_str)
        if ret == -1:
            print 'parse_recived_message get_lldp_neighbor erro end! \r\n'
            
    print 'parse_recived_message end! \r\n'
        



def scan_server_lldp(chan):

    print 'scan_server_lldp start !'

    try:
        ret = 0
        chan.settimeout(1.0)
        # get switch cli mode info via ssh
        switch_mode_info = ''
        switch_mode_info = switch_api.get_switchinfo_climode(chan, switch_mode_info)
        # send cli command to switch via ssh
        switch_cli = 'show lldp neighbors detail \r\n'
        print 'scan_server_lldp send start switch_cli = %s \r\n' % switch_cli ,
        switch_api.send_switch_cli(chan, switch_cli)
        # recive the cli return info via ssh
        switch_cli_return = ''
        switch_cli_return = switch_api.get_switchinfo_cliexecut(chan, switch_mode_info)
        print 'scan_server_lldp switch_cli_return =\r\n %s \r\n!' % switch_cli_return,
        # analyse the swirch return message 
        ret = parse_recived_message(switch_cli_return, switch_cli)
        if ret == -1:
            print 'scan_server_lldp parse_recived_message erro! \r\n'
        else:
            print 'scan_server_lldp parse_recived_message success! \r\n'

    finally:
        print 'scan_server_lldp end !'

def get_server_lldpneighbors(chan):

    print 'scan_server_lldp start !'

    try:
        ret = 0
        chan.settimeout(1.0)
        # get switch cli mode info via ssh
        switch_mode_info = ''
        switch_mode_info = switch_api.get_switchinfo_climode(chan, switch_mode_info)
        # send cli command to switch via ssh
        switch_cli = 'show lldp neighbors \r\n'
        print 'scan_server_lldp send start switch_cli = %s \r\n' % switch_cli ,
        switch_api.send_switch_cli(chan, switch_cli)
        # recive the cli return info via ssh
        switch_cli_return = ''
        switch_cli_return = switch_api.get_switchinfo_cliexecut(chan, switch_mode_info)
        print 'scan_server_lldp switch_cli_return =\r\n %s \r\n!' % switch_cli_return,
        # analyse the swirch return message 
        ret = parse_recived_message(switch_cli_return, switch_cli)
        if ret == -1:
            print 'scan_server_lldp parse_recived_message erro! \r\n'
        else:
            print 'scan_server_lldp parse_recived_message success! \r\n'

    finally:
        print 'scan_server_lldp end !'

def set_switch_vlan(ssh_host, ssh_port, ifx, vlan):
    
    # paramater check is here
    
    # create cli command
    sshhost = ssh_host
    sshport = ssh_port
    switch_port_mode = 'access'
    switch_ifx = ifx
    switch_vlan = str(vlan)
    vlanall =  '1-4094'
    vlanlist = vlanall
    access = 'ACCESS'
    trunk = 'TRUNK'
    uplink = 'UPLINK'
    portmode = ''
    return_switchport_info = ''
    
    # first step into vlan mode 
    cli_confmode = 'configure\r\n'
    cli_show_ifx_mode = 'show interfaces ' + switch_ifx + ' switchport\r\n'
    cli_vlanmode = 'vlan ' + switch_vlan + '\r\n'
    #print 'set_switch_vlan cli_vlanmode = %s \r\n' % cli_vlanmode,
    cli_ifx_mode = 'interface ' + switch_ifx +  '\r\n'
    # bug for eth1 native 1 will not get dhcp ip
    portmode = trunk
    cli_ifx_set_trunkmode = 'switchport mode '+ portmode +'\r\n'
    portmode = uplink
    cli_ifx_set_uplinkmode = 'switchport mode '+ portmode +'\r\n'
    cli_ifx_remove_vlan = 'switchport tru allow vlan r '+ vlanlist + '\r\n'
    vlanlist = switch_vlan
    cli_ifx_add_vlan = 'switchport tru allow vlan add ' + vlanlist + '\r\n'
    
    #print 'set_switch_vlan cli_vlan_addifx = %s \r\n' % cli_vlan_addifx,
    
    cli_exit = 'exit\r\n'
    cli_conf_exit = 'exit\r\n'
    
    # create ssh connect by host
    user = get_sshserver_username(sshhost)
    password = get_sshserver_password(sshhost)
    
    t= sshclient.ssh_connect(user, password, sshhost, sshport)
    if t == -1:
        print 'set_switch_vlan ssh connect failed t == -1\r\n'
        return -1
    
    chan = sshclient.ssh_channel(t)
    if chan == -1:
        print 'set_switch_vlan ssh channel create failed chan == -1 \r\n'
        return -1
    
    # send the cli to switch
    
    try:
        chan.settimeout(5.0)
        # get switch cli mode info via ssh
        switch_mode_info = ''
        switch_mode_info = switch_api.get_switchinfo_climode(chan, switch_mode_info)
        
        # send 'conf' cli command to switch via ssh
        switch_api.send_switch_cli(chan, cli_confmode)
        switch_cli_return = ''
        switch_mode_info = switch_api.get_switchinfo_climode(chan, switch_cli_return)
        print 'set_switch_vlan cli_confmode return = %s \r\n' % switch_mode_info,
        # send 'vlan xx ' cli command to switch via ssh Create or Set vlan
        switch_api.send_switch_cli(chan, cli_vlanmode)
        # send cli command exit vlan mode
        switch_api.send_switch_cli(chan, cli_exit)
        
        # Check interface mode
        switch_api.send_switch_cli(chan, cli_show_ifx_mode)
        # Get the interface mode info
        return_switchport_info = switch_api.get_switchinfo_cliexecut(chan,switch_mode_info)
        print 'set_switch_vlan cli_confmode return_switchport_info = \r\n%s \r\n' % return_switchport_info,
        # Parse the interface mode info
        switch_port_mode = switch_api.get_switchport_mode(return_switchport_info, switch_ifx)
        print 'set_switch_vlan cli_confmode switch_port_mode = %s \r\n' % switch_port_mode,
        #into interface mode
        switch_api.send_switch_cli(chan, cli_ifx_mode)
        #if the ifx is access mode should switch to trunnk then remova all vlan ,finally set vlan 
        if switch_port_mode == access:
            print 'set_switch_vlan switch_port_mode is access! \r\n'
            # change portmode into trunk
            #send_switch_cli(chan, cli_ifx_set_trunkmode)
            #print 'set_switch_vlan cli_ifx_set_trunkmode send! \r\n'
            # change portmode into uplink
            switch_api.send_switch_cli(chan, cli_ifx_set_uplinkmode)
            print 'set_switch_vlan cli_ifx_set_uplinkmode send! \r\n'
            # remova all vlan list
            switch_api.send_switch_cli(chan, cli_ifx_remove_vlan)
            print 'set_switch_vlan cli_ifx_remove_vlan send! \r\n'
            # add vlan into allow vlan list
            switch_api.send_switch_cli(chan, cli_ifx_add_vlan)
            print 'set_switch_vlan cli_ifx_add_vlan send! \r\n'
        elif switch_port_mode == trunk:
            print 'set_switch_vlan switch_port_mode is trunk! \r\n'
            # add vlan into trunk allow vlan list
            switch_api.send_switch_cli(chan, cli_ifx_add_vlan)
        elif switch_port_mode == uplink:
            print 'set_switch_vlan switch_port_mode is uplink! \r\n'
            # add vlan into trunk allow vlan list
            switch_api.send_switch_cli(chan, cli_ifx_add_vlan)
        else:
            print 'set_switch_vlan err : port mode error \r\n' 

        print 'set_switch_vlan send_switch_cli OK \r\n' 
        # send cli command exit interface mode and config mode
        switch_api.send_switch_cli(chan, cli_exit)
        switch_api.send_switch_cli(chan, cli_conf_exit)

    finally:
        print 'set_switch_vlan end !'

    # close the ssh conect with switch
    sshclient.ssh_close(chan, t)

    return 0

def unset_switch_vlan(ssh_host, ssh_port, ifx, vlan):
    # send cli to switch by ssh connet
    
    # paramater check is here
    
    # create cli command
    
    sshhost = ssh_host
    sshport = ssh_port
    switch_ifx = ifx
    switch_vlan = str(vlan)
    
    # first step into vlan mode 
    cli_confmode = 'configure\r\n'
    cli_vlanmode = 'vlan ' + switch_vlan + '\r\n'
    #print 'set_switch_vlan cli_vlanmode = %s \r\n' % cli_vlanmode,

    cli_vlan_noaddifx = 'no add interface ' + switch_ifx + '\r\n'
    #print 'set_switch_vlan cli_vlan_addifx = %s \r\n' % cli_vlan_addifx,
    
    cli_exit = 'exit\r\n'
    cli_conf_exit = 'exit\r\n'
	
    # create ssh connect by host
    user = get_sshserver_username(sshhost)
    password = get_sshserver_password(sshhost)
    
    t= sshclient.ssh_connect(user, password, sshhost, sshport)
    if t == -1:
        print 'unset_switch_vlan ssh connect failed t == -1\r\n'
        return -1
    
    chan = sshclient.ssh_channel(t)
    if chan == -1:
        print 'unset_switch_vlan ssh channel create failed chan == -1 \r\n'
        return -1
    
    # send the cli to switch
    
    try:
        chan.settimeout(5.0)
        # get switch cli mode info via ssh
        switch_mode_info = ''
        switch_mode_info = switch_api.get_switchinfo_climode(chan, switch_mode_info)
        
        switch_api.send_switch_cli(chan, cli_confmode)
        switch_cli_return = ''
        switch_mode_info = switch_api.get_switchinfo_climode(chan, switch_cli_return)
        print 'set_switch_vlan cli_confmode return = %s \r\n' % switch_mode_info,
        
        # Check interface mode
        cli_show_ifx_mode = 'show interfaces ' + switch_ifx + ' switchport \r\n'
        switch_api.send_switch_cli(chan, cli_show_ifx_mode)
        # Get the interface mode info
        return_switchport_info = switch_api.get_switchinfo_cliexecut(chan,switch_mode_info)
        print 'set_switch_vlan cli_confmode return_switchport_info = \r\n%s \r\n' % return_switchport_info,
        # Parse the interface mode info
        switch_port_mode = switch_api.get_switchport_mode(return_switchport_info, switch_ifx)
        print 'set_switch_vlan cli_confmode switch_port_mode = %s \r\n' % switch_port_mode,
        
        if switch_port_mode == 'ACCESS':
            # send cli command into vlan mode
            switch_api.send_switch_cli(chan, cli_vlanmode)
            # send cli command to switch via ssh
            switch_api.send_switch_cli(chan, cli_vlan_noaddifx)
            # send cli command exit vlan mode and config mode
            switch_api.send_switch_cli(chan, cli_exit)
            switch_api.send_switch_cli(chan, cli_conf_exit)
        elif switch_port_mode == 'TRUNK':
            #into interface mode
            cli_ifx_mode = 'interface ' + switch_ifx +  '\r\n'
            switch_api.send_switch_cli(chan, cli_ifx_mode)
            print 'set_switch_vlan cli_ifx_mode is send! \r\n'
            # remova vlan from vlan list
            cli_ifx_remove_vlan = 'switchport trunk allowed vlan rem '+ switch_vlan + '\r\n'
            #print 'set_switch_vlan cli_confmode cli_ifx_remove_vlan = %s \r\n' % cli_ifx_remove_vlan,
            switch_api.send_switch_cli(chan, cli_ifx_remove_vlan)
            # send cli command exit vlan mode and config mode
            switch_api.send_switch_cli(chan, cli_exit)
            switch_api.send_switch_cli(chan, cli_conf_exit)
        elif switch_port_mode == 'UPLINK':
            #into interface mode
            cli_ifx_mode = 'interface ' + switch_ifx +  '\r\n'
            switch_api.send_switch_cli(chan, cli_ifx_mode)
            print 'set_switch_vlan cli_ifx_mode is send! \r\n'
            # remova vlan from vlan list
            cli_ifx_remove_vlan = 'switchport trunk allowed vlan rem '+ switch_vlan + '\r\n'
            #print 'set_switch_vlan cli_confmode cli_ifx_remove_vlan = %s \r\n' % cli_ifx_remove_vlan,
            switch_api.send_switch_cli(chan, cli_ifx_remove_vlan)
            # send cli command exit vlan mode and config mode
            switch_api.send_switch_cli(chan, cli_exit)
            switch_api.send_switch_cli(chan, cli_conf_exit)
        else:
            print 'unset_switch_vlan switch_port_mode is error! \r\n' 
        print 'unset_switch_vlan send_switch_cli OK \r\n' 

    finally:
        print 'unset_switch_vlan end !'

    # close the ssh conect with switch
    sshclient.ssh_close(chan, t)
    
    return 0


def get_lldp_neighbor_details(recv_str):

    #print 'get_lldp_neighbor start! \r\n'
    if len(recv_str) == 0:
        print 'get_lldp_neighbor para erro: recv_str !'
        return -1

    # save the data to local array
    neighbor_list = []

    neighbor_list = get_neighbor_list_details( recv_str )
    print 'get_lldp_neighbor neighbor_list = \r\n%s \r\n' % neighbor_list,
    
    # host should get from db by config set,there just is demo !
    host = '192.168.21.35'
    # save lldp neighbors info to db
    switch_db.add_port_neighbors(host, neighbor_list)

    #print 'get_lldp_neighbor end! \r\n'
    return 0

def get_lldp_neighbor(recv_str):

    #print 'get_lldp_neighbor start! \r\n'
    if len(recv_str) == 0:
        print 'get_lldp_neighbor para erro: recv_str !'
        return -1

    # save the data to local array
    neighbor_list = []

    neighbor_list = get_neighbor_list( recv_str )
    print 'get_lldp_neighbor neighbor_list = \r\n%s \r\n' % neighbor_list,
    
    # host should get from db by config set,there just is demo !
    host = '192.168.21.35'
    # save lldp neighbors info to db
    switch_db.add_port_neighbors(host, neighbor_list)

    #print 'get_lldp_neighbor end! \r\n'
    return 0

def get_neighbor_list_details( recv_str ):

    # save the data to local array
    neighbor_list = []
    recv_tmp = ''
    tuple_count = 0
    recv_str_tail = 0

    # parse the recive message by cli type
    # init the data
    Local_ifx = 'LLDP neighbor-information of port ['
    Local_ifx_val = ''
    Local_ifx_tail = ']\r\n'
    
    Neighbor_index = 'Neighbor index                    : '
    Neighbor_index_val = ''

    Device_type = '  Device type                       : '
    
    ChassisID_type = '  Chassis ID type                   : '
    ChassisID_type_val = ''
    
    ChassisID = '  Chassis ID                        : '
    ChassisID_val = ''
    
    SystemName = '  System name                       : '
    SystemName_val = ''
    
    System_des = '  System description                : '
    
    PortID_type = '  Port ID type                      : '
    PortID_type_val = ''
    
    PortID = 'Port ID                           : '
    PortID_val = ''
    
    Port_des = '  Port description                  :'
    
    Port_VLANID = 'Port VLAN ID                      : '
    Port_VLANID_val = ''
    
    PPVID = '  Port and protocol VLAN ID(PPVID)  : '
    UnitEnd = '  Maximum frame Size                :'

    while True:

        ret = recv_str.find(UnitEnd)
        if ret == -1:
            break;
        recv_str_tail = ret + len(UnitEnd)
        recv_tmp = recv_str[0:recv_str_tail]
        # get val message by search string in revice message
        Local_ifx_val = switch_api.get_val_by_str(Local_ifx, Local_ifx_tail, recv_tmp)
        if len(Local_ifx_val) == 0:
            print'get_lldp_neighbor can not find Local_ifx_val !\r\n'
        #print 'get_lldp_neighbor Local_ifx_val = %s \r\n' % Local_ifx_val,
    
        Neighbor_index_val = switch_api.get_val_by_str(Neighbor_index, Device_type, recv_tmp)
        if len(Neighbor_index_val) == 0:
            #print 'get_lldp_neighbor Neighbor_index_val not find = %s \r\n' % Neighbor_index_val,
            break
        Neighbor_index_val = Neighbor_index_val[:-2] 
        #print 'get_lldp_neighbor Neighbor_index_num = %s \r\n' % Neighbor_index_val,
    
        ChassisID_type_val = switch_api.get_val_by_str(ChassisID_type, ChassisID, recv_tmp)
        ChassisID_type_val = ChassisID_type_val[:-2]
        #print 'get_lldp_neighbor ChassisID_type_val = %s \r\n' % ChassisID_type_val,
    
        ChassisID_val = switch_api.get_val_by_str(ChassisID, SystemName, recv_tmp)
        ChassisID_val = ChassisID_val[:ChassisID_val.find('\r\n')]
        #print 'get_lldp_neighbor ChassisID_val = %s \r\n' % ChassisID_val,
    
        SystemName_val = switch_api.get_val_by_str(SystemName, System_des, recv_tmp)
        SystemName_val = SystemName_val[:-2]
        #print 'get_lldp_neighbor SystemName_val = %s \r\n' % SystemName_val,
    
        PortID_type_val = switch_api.get_val_by_str(PortID_type, PortID, recv_tmp)
        PortID_type_val = PortID_type_val[:PortID_type_val.find('\r\n')]
        #print 'get_lldp_neighbor PortID_type_val = %s \r\n' % PortID_type_val,
    
        PortID_val = switch_api.get_val_by_str(PortID, Port_des, recv_tmp)
        PortID_val = PortID_val[:PortID_val.find('\r\n')]
        #print 'get_lldp_neighbor PortID_val = %s \r\n' % PortID_val,
    
        Port_VLANID_val = switch_api.get_val_by_str(Port_VLANID, PPVID, recv_tmp)
        Port_VLANID_val = Port_VLANID_val[:-2]
        #print 'get_lldp_neighbor Port_VLANID_val = %s \r\n' % Port_VLANID_val,

        recv_str = recv_str[recv_str_tail:-1]
        #print '\r\n#################################################### \r\n'
        #print 'get_lldp_neighbor recv_str 3 = %s \r\n' % recv_str,
        #print '\r\n#################################################### \r\n'
        #print 'get_lldp_neighbor recv_str_head = %d \r\n' % recv_str_tail,

        if len(Local_ifx_val) > 0:
        	ifx = Local_ifx_val
        #print 'get_lldp_neighbor ifx = %s \r\n' % ifx,
        neighbor_tuple = (ifx, Neighbor_index_val, PortID_type_val, PortID_val)
        neighbor_list.insert( tuple_count, neighbor_tuple )
        tuple_count = tuple_count +1
        print '\r\n-----------------serach times = %d ------------------\r\n' % tuple_count,
        continue

    return neighbor_list

def get_neighbor_list( recv_str ):

    # save the data to local array
    neighbor_list = []
    recv_tmp = ''
    tuple_count = 0
    recv_str_tail = 0

    # parse the recive message by cli type
    # init the data

    SystemName = 'System Name'
    SystemName_val = ''
    
    Local_ifx = 'Local Intf'
    Local_ifx_val = ''
    
    PortID = 'Port ID'
    PortID_val = ''
    
    Capability = 'Capability'
    Capability_val = ''
    
    Agingtime = 'Aging-time'
    Agingtime_val = ''

    while True:

        SystemName_val = switch_api.get_val_by_str(SystemName, System_des, recv_tmp)
        SystemName_val = SystemName_val[:-2]
        #print 'get_lldp_neighbor SystemName_val = %s \r\n' % SystemName_val,

        # get val message by search string in revice message
        Local_ifx_val = switch_api.get_val_by_str(Local_ifx, Local_ifx_tail, recv_tmp)
        if len(Local_ifx_val) == 0:
            print'get_lldp_neighbor can not find Local_ifx_val !\r\n'
        #print 'get_lldp_neighbor Local_ifx_val = %s \r\n' % Local_ifx_val,
    
        PortID_val = switch_api.get_val_by_str(PortID, Port_des, recv_tmp)
        PortID_val = PortID_val[:-2]
        #print 'get_lldp_neighbor PortID_val = %s \r\n' % PortID_val,

        recv_str = recv_str[recv_str_tail:-1]
        #print '\r\n#################################################### \r\n'
        #print 'get_lldp_neighbor recv_str 3 = %s \r\n' % recv_str,
        #print '\r\n#################################################### \r\n'
        #print 'get_lldp_neighbor recv_str_head = %d \r\n' % recv_str_tail,

        if len(Local_ifx_val) > 0:
            ifx = Local_ifx_val
        #print 'get_lldp_neighbor ifx = %s \r\n' % ifx,
        neighbor_tuple = (ifx, Neighbor_index_val, ChassisID_type_val, ChassisID_val)
        neighbor_list.insert( tuple_count, neighbor_tuple )
        tuple_count = tuple_count +1
        print '\r\n-----------------serach times = %d ------------------\r\n' % tuple_count,
        continue

    return neighbor_list


def set_sshserver_hostinfo(index, sshhost, sshport, retry, reconnect):
    # parameter check

    # save host info into db
    ret = switch_db.get_hostinfo_byhost(sshhost)
    if ret == [] :
        # not find host info ,Create new one
        switch_db.add_hostinfo(index, sshhost, sshport, retry, reconnect)
    else:
        # find old hostinfo ,Update it 
        switch_db.update_hostinfo(index, sshhost, sshport, retry, reconnect)
    return 0

def get_sshserver_hostinfo():

    # There will get all hostinfo from db
    hostinfo = switch_db.get_hostinfo()

    return hostinfo

def get_sshserver_hostinfo_byhost( sshhost ):

    # There Should get hostinfo from db
    hostinfo = switch_db.get_hostinfo_byhost(sshhost)
    if hostinfo != []:
        h_host = hostinfo[0].ip_address
        h_port = hostinfo[0].port_id
        h_retry = hostinfo[0].retry_times
        h_recont = hostinfo[0].reconnect_time
        hostinfo_t = (h_host, h_port, h_retry, h_recont)

    return hostinfo_t

def set_sshserver_userinfo(index, username, passwd):
    # parameter check
    
    #save user config info 
    # should save into db
    userinfo_t = (index, username, passwd)
    ret = switch_db.get_userinfo(index)
    if ret == [] :
        # not find user info ,Create new one
        switch_db.add_userinfo(index, username, passwd)
    else:
        # find old user info ,Update it 
        switch_db.update_userinfo(index, username, passwd)

    return 0


def get_sshserver_username( sshhost ):
    
    # get server id from db by host
    index =  switch_db.get_sshserver_id(sshhost)
    print 'get_sshserver_username index = %s \r\n' % index,
    # get username from db by host id
    usercfg = switch_db.get_userinfo(index)
    print '###########get_sshserver_username usercfg = %s \r\n' % usercfg,
    username = usercfg[0].username
    print 'get_sshserver_username username = %s \r\n' % username,
    return username

def get_sshserver_password( sshhost):
    
    # get server id from db by host
    index =  switch_db.get_sshserver_id(sshhost)
    print 'get_sshserver_password index = %s \r\n' % index,
    # get username from db by host id
    usercfg = switch_db.get_userinfo(index)
    passwd = usercfg[0].password
    print 'get_sshserver_password passwd = %s \r\n' % passwd,
    return passwd
    


def set_ruijie_vlan(vif_id, net_id):
    LOG.info("set_ruijie_vlan, vif id is %s, net id is %s" 
             % (vif_id, net_id))
    vm_eth_binding = rgos_db.get_ruijie_vm_eth_binding(vif_id)
    if vm_eth_binding == []:
        return
    mac_address = vm_eth_binding[0].mac_address
    LOG.info("interface id %s has been connected to mac %s" 
             % (vif_id, mac_address))
    switch_binding = rgos_db.get_ruijie_switch_eth_binding(mac_address)
    if switch_binding == []:
        return;
    ip = switch_binding[0].ip_address
    ifx = switch_binding[0].port_id
    ovs_binding = vlan_mgr.get_network_binding(None, net_id)
    if ovs_binding == None:
        return
    vlan = ovs_binding.segmentation_id
    LOG.info("the switch ip is %s, ifx is %s, vlan is %s" 
            % (ip, ifx, vlan))
    ruijie_vlan_binding = rgos_db.get_ruijie_vlan_binding(ip, ifx, vlan)
    if ruijie_vlan_binding == []:
        LOG.info("to set the vlan of ruijie switch now")
        set_switch_vlan(ip, 22, ifx, vlan)
    rgos_db.add_ruijie_vlan_binding(ip, ifx, vlan, vif_id)
    return
    
def unset_ruijie_vlan(vif_id, net_id):
    LOG.info("unset_ruijie_vlan, net id is %s, vif id is %s, " 
             % (net_id, vif_id))
    vm_eth_binding = rgos_db.get_ruijie_vm_eth_binding(vif_id)
    if vm_eth_binding == []:
        return
    mac_address = vm_eth_binding[0].mac_address
    LOG.info("vif id %s has been connected to mac %s" 
             % (vif_id, mac_address))
    switch_binding = rgos_db.get_ruijie_switch_eth_binding(mac_address)
    if switch_binding == []:
        return;
    ip = switch_binding[0].ip_address
    ifx = switch_binding[0].port_id
    ovs_binding = vlan_mgr.get_network_binding(None, net_id)
    if ovs_binding == None:
        return
    vlan = ovs_binding.segmentation_id
    LOG.info("the switch ip is %s, ifx is %s, vlan is %s" 
            % (ip, ifx, vlan))
    print ("-----> TRY TO UNSET RUIJIE VLAN swith ip %s ifx %s vid %s" % (ip, ifx, vlan))
    rgos_db.remove_ruijie_vlan_binding(ip, ifx, vlan, remote_iface_id)
    ruijie_vlan_binding = rgos_db.get_ruijie_vlan_binding(ip, ifx, vlan)
    if ruijie_vlan_binding == []:
        LOG.info("to set the vlan of ruijie switch now")
        print ("-----> SATRT UNSET RUIJIE VLAN swith ip %s ifx %s vid %s" % (ip, ifx, vlan))
        unset_switch_vlan(ip, 22, ifx, vlan)
        print ("-----> END UNSET RUIJIE VLAN swith ip %s ifx %s vid %s" % (ip, ifx, vlan))
    return 

def update_ruijie_vlan(vif_id, net_id, old_seg_id):
    LOG.info("update_ruijie_vlan, net id is %s, vif id is %s, old vid %s, " 
             % (net_id, vif_id, old_seg_id))
    vm_eth_binding = rgos_db.get_ruijie_vm_eth_binding(vif_id)
    if vm_eth_binding == []:
        return
    mac_address = vm_eth_binding[0].mac_address
    LOG.info("interface id %s has been connected to mac %s" 
             % (vif_id, mac_address))
    switch_binding = rgos_db.get_ruijie_switch_eth_binding(mac_address)
    if switch_binding == []:
        return;
    ip = switch_binding[0].ip_address
    ifx = switch_binding[0].port_id
    ovs_binding = vlan_mgr.get_network_binding(None, net_id)
    if ovs_binding == None:
        return
    vlan = ovs_binding.segmentation_id
    
    # del old ruijie switch vlan
    print ("-----> TRY TO UNSET RUIJIE VLAN swith ip %s ifx %s vid %s" % (ip, ifx, old_seg_id))
    rgos_db.remove_ruijie_vlan_binding(ip, ifx, old_seg_id, vif_id)
    ruijie_vlan_binding = rgos_db.get_ruijie_vlan_binding(ip, ifx, old_seg_id)
    if ruijie_vlan_binding == []:
        LOG.info("to set the vlan of ruijie switch now")
        print ("-----> SATRT UNSET RUIJIE VLAN swith ip %s ifx %s vid %s" % (ip, ifx, old_seg_id))
        unset_switch_vlan(ip, 22, ifx, old_seg_id)
        print ("-----> END UNSET RUIJIE VLAN swith ip %s ifx %s vid %s" % (ip, ifx, old_seg_id))
    
    print ("-----> TRY TO SET RUIJIE VLAN swith ip %s ifx %s vid %s" % (ip, ifx, vlan))
    ruijie_vlan_binding = rgos_db.get_ruijie_vlan_binding(ip, ifx, vlan)
    if ruijie_vlan_binding == []:
        LOG.info("to set the vlan of ruijie switch now")
        print ("-----> SATRT SET RUIJIE VLAN swith ip %s ifx %s vid %s" % (ip, ifx, vlan))
        set_switch_vlan(ip, 22, ifx, vlan)
        print ("-----> END SET RUIJIE VLAN swith ip %s ifx %s vid %s" % (ip, ifx, vlan))
    rgos_db.add_ruijie_vlan_binding(ip, ifx, vlan, vif_id)
    


