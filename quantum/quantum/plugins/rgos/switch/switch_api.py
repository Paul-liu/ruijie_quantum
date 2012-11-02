import socket
import string
from quantum.plugins.rgos.ssh import sshclient
from quantum.plugins.rgos.db import rgos_db


def get_switchinfo_climode(chan, switch_mode_info):

    #print 'get_switchinfo_climode start! \r\n'
    while True:
        try:
            switch_mode_info = chan.recv(1024)
            print 'get_switchinfo_climode recive switch_mode_info = %s \r\n' % switch_mode_info ,
            if len(switch_mode_info) == 0:
                print '\r\n get_switchinfo_climode *** EOF\r\n',
            break
        except socket.timeout:
            break

    #print 'get_switchinfo_climode : %s end! \r\n' % switch_mode_info,
    return switch_mode_info

def send_switch_cli(chan, cli):

    #print 'send_switch_cli start! \r\n'

    try:
        # send cli for get switch info
        space = ' '
        if len(cli) == 0:
            print 'send_switch_cli para erro:[cli] !'
        print 'send_switch_cli len(cli) = %d \r\n' % len(cli) ,
        switch_cli = cli
        y = chan.send(switch_cli)
        #print '========send_switch_cli send switch_cli send y= %d \r\n' % y,
        print '========send_switch_cli send switch_cli.split = %s \r\n' % switch_cli.split() ,
        #print 'send_switch_cli send end = [%s] \r\n' % switch_cli ,
        # Recive the send message about cli
        if switch_cli != space:
            get_send2switch_cli(chan, switch_cli)
            print 'send_switch_cli is space used for more ! \r\n'

        #print '========send_switch_cli end! \r\n'
        
    except socket.timeout:
        pass


def get_send2switch_cli(chan, switch_cli):

    #print '########get_send2switch_cli start! \r\n'

    if len(switch_cli) == 0:
        print 'get_send2switch_cli para erro !'

    cli_str = ''
    while True:
        try:
            x = chan.recv(512)
            if len(cli_str) < len(switch_cli):
                #print '########get_send2switch_cli recv switch_cli = %s \r\n' % x ,
                cli_str = cli_str + x
                continue
            #print '########get_send2switch_cli recv cli_str = [%s] \r\n' % cli_str ,
            print '########get_send2switch_cli recv cli_str.split = %s \r\n' % cli_str.split() ,
            break
        except socket.timeout:
            break

    #print '########get_send2switch_cli end! \r\n'

def get_switchinfo_cliexecut(chan,switch_mode_info):

    #print 'get_switchinfo_cliexecut start! \r\n'

    switch_cli_return = ''
    recv_buf = 120
    recv_times = 1
    while True:
        try:
            # recive the switch cli return info
            y = ''
            more = '--More--'
            enter = '\r\n'
            y = chan.recv(recv_buf)
            #print 'recv switch_cli y = [%s] \r\n' % y,
            #print 'recv switch_cli len(y) = %d \r\n' % len(y),
            if len(y) != len(switch_mode_info):
                # cli return not completed countine recive!
                if y.find(more,0,) == -1:
                    #print 'recv switch_cli if 0 find more y = %d \r\n' % y.find(more),
                    #print 'recv switch_cli if 0 not find more y = [%s] \r\n' % y,
                    switch_cli_return = switch_cli_return + y
                    continue
                else:
                    # when recv the 'more' message ,auto send space and enter command ,contuine recive show
                    #print 'recv switch_cli find more y.find = %d \r\n' % y.find(more),
                    #print 'recv switch_cli find more switch_cli_return before = \r\n[%s] \r\n' % switch_cli_return,
                    #print 'recv switch_cli find more y.splite() = %s \r\n' % y.split(),
                    #print 'recv switch_cli find more y = [%s]\r\n' % y,
                    print 'recv switch cli return info is too much, send space continue recive ...\r\n'
                    switch_cli_more = ' '
                    send_switch_cli(chan, switch_cli_more)
                    #switch_cli_return = switch_cli_return + y
                    #print 'recv switch_cli find more switch_cli_return after = ==========> \r\n[%s] \r\n' % switch_cli_return,
                    continue
            else:
                # cli return message is recviced complete!
                print 'recv switch_cli len(y) = switch_mode_info %d quit recv !\r\n' % len(switch_mode_info),
                break
            
            print 'recv switch cli return info is completed ! \r\n'
            #print 'recv switch_cli if end len(y) = %d \r\n' % len(y),
        except socket.timeout:
            break

    #print 'recv switch_cli return info len = %d \r\n' % len(switch_cli_return),
    #print 'recv switch_cli return info =\r\n %s \r\n' % switch_cli_return,
    #print 'get_switchinfo_cliexecut end! \r\n'
    return switch_cli_return


def get_val_by_str(headstr, tailstr, message):

    val = ''
    
    #print 'get_val_by_str message = %s \r\n' % message,
    head = message.find(headstr)
    if head == -1:
        print 'get_val_by_str not find head ! \r\n'
        return val
    head = head + len(headstr)
    #print 'get_val_by_str head = %d \r\n' % head,

    tail = message.find(tailstr)
    if tail == -1:
        print 'get_val_by_str not find tail ! \r\n'
        return val
    #print 'get_val_by_str tail = %d \r\n' % tail,
    val = message[head:tail]
    #print 'get_val_by_str val = %s \r\n' % val,
    return val


def get_switchport_mode(recv_info, ifx):
    
    ##########################################################
    #Ruijie(config)#show interfaces Gi0/10 switchport
    #Interface                        Switchport Mode      Access Native Protected VLAN lists
    #-------------------------------- ---------- --------- ------ ------ --------- ----------
    #GigabitEthernet 3/0/10           enabled    TRUNK     1      1      Disabled  1-2
    ##########################################################
    str_ifx = ''
    list_ifx = []
    portmode = ''
    port_info = ''
    info_head = -1
    info_tail= -1
    
    # parse the recv_info 
    str_ifx = ifx
    if str_ifx.find('GigabitEthernet') == -1:
        list_ifx = str_ifx.split()
        #print 'get_switchport_mode find list_ifx = %s \r\n' %list_ifx,
        str_ifx = list_ifx[1]

    #print 'get_switchport_mode find recv_info = %s \r\n' %recv_info,
    #print 'get_switchport_mode find str_ifx = %s \r\n' %str_ifx,
    info_head = recv_info.find(str_ifx)
    #print 'get_switchport_mode find info_head = %d \r\n' %info_head,
    if  info_head != -1:
        info_tail = recv_info.find('\r\n',info_head)
        #print 'get_switchport_mode find tail = %d \r\n' %info_tail,
        if info_tail != -1:
            port_info = recv_info[info_head:info_tail]
            val = port_info.find('TRUNK')
            if val != -1:
                portmode = 'TRUNK'
                return portmode
            val = port_info.find('ACCESS')
            if val != -1:
                portmode = 'ACCESS'
                return portmode
            val = port_info.find('UPLINK')
            if val != -1:
                portmode = 'UPLINK'
                return portmode
        else:
            print 'get_switchport_mode error can not find tail \r\n'

    print 'get_switchport_mode error can not find ifx \r\n'
    return portmode
