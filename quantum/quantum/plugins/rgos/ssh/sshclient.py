#!/usr/bin/env python

# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distrubuted in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.


import base64
from binascii import hexlify
import getpass
import os
import select
import socket
import sys
import threading
import time
import traceback
import paramiko

def agent_auth(transport, username):
    """
    Attempt to authenticate to the given transport using any of the private
    keys available from an SSH agent.
    """
    
    agent = paramiko.Agent()
    agent_keys = agent.get_keys()
    if len(agent_keys) == 0:
        return
        
    for key in agent_keys:
        print 'Trying ssh-agent key %s' % hexlify(key.get_fingerprint()),
        try:
            transport.auth_publickey(username, key)
            print '... success!'
            return
        except paramiko.SSHException:
            print '... nope.'


def manual_auth(username, hostname, passwd, t):
    default_auth = 'p'
    #auth = raw_input('Auth by (p)assword, (r)sa key, or (d)ss key? [%s] ' % default_auth)
    #if len(auth) == 0:
    auth = default_auth

    if auth == 'r':
        default_path = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
        path = raw_input('RSA key [%s]: ' % default_path)
        if len(path) == 0:
            path = default_path
        try:
            key = paramiko.RSAKey.from_private_key_file(path)
        except paramiko.PasswordRequiredException:
            password = getpass.getpass('RSA key password: ')
            key = paramiko.RSAKey.from_private_key_file(path, password)
        t.auth_publickey(username, key)
    elif auth == 'd':
        default_path = os.path.join(os.environ['HOME'], '.ssh', 'id_dsa')
        path = raw_input('DSS key [%s]: ' % default_path)
        if len(path) == 0:
            path = default_path
        try:
            key = paramiko.DSSKey.from_private_key_file(path)
        except paramiko.PasswordRequiredException:
            password = getpass.getpass('DSS key password: ')
            key = paramiko.DSSKey.from_private_key_file(path, password)
        t.auth_publickey(username, key)
    else:
        #pw = getpass.getpass('Password for %s@%s: ' % (username, hostname))
        pw = passwd
        t.auth_password(username, pw)



def ssh_connect(user, passwd, host, sshport):
    # setup logging
    paramiko.util.log_to_file('rgos_ssh.log')

    username = user
    password = passwd
    hostname =host
    if len(hostname) == 0:
        print '*** Hostname required.'
        sys.exit(1)
    port = sshport
    #port = 22

    # now connect
    try:
        print '\r\n*** SSH socket start.'
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))
        print '*** SSH socket connect end.'
    except Exception, e:
        print '*** Connect failed: ' + str(e)
        traceback.print_exc()
        sys.exit(1)

    try:
        print '*** SSH try Transport start.'
        t = paramiko.Transport(sock)
        try:
            print '*** SSH try Transport start_client start.'
            t.start_client()
        except paramiko.SSHException:
            print '*** SSH negotiation failed.'
            sys.exit(1)

        try:
            print '*** SSH try load_host_keys start.'
            keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        except IOError:
            try:
                keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
            except IOError:
                print '*** Unable to open host keys file'
                keys = {}

        # check server's host key -- this is important.
        key = t.get_remote_server_key()
        if not keys.has_key(hostname):
            print '*** WARNING: Unknown host key!'
        elif not keys[hostname].has_key(key.get_name()):
            print '*** WARNING: Unknown host key!'
        elif keys[hostname][key.get_name()] != key:
            print '*** WARNING: Host key has changed!!!'
            return -1
        else:
            print '*** Host key OK.'

        agent_auth(t, username)
        print '*** is_authenticated start.'
        if not t.is_authenticated():
            manual_auth(username, hostname,password,t)
        if not t.is_authenticated():
            print '*** Authentication failed. :('
            t.close()
            return -1
        print '*** is_authenticated end.'
        return t

    except Exception, e:
        print '*** Caught exception: ' + str(e.__class__) + ': ' + str(e)
        traceback.print_exc()
        try:
            t.close()
            return -1
        except:
            pass
        
def ssh_channel(transport):
    
    try:
        chan = transport.open_session()
        chan.get_pty()
        chan.invoke_shell()
        print '*** Here we go!'
        print
        return chan
    
    except Exception, e:
        print '*** Caught exception: ' + str(e.__class__) + ': ' + str(e)
        traceback.print_exc()
        try:
            transport.close()
            return -1
        except:
            pass

def ssh_close(chan, t):
    if chan != -1:
        chan.close()
        print '*** SSH channel connect closed.'
    
    t.close()
    print '*** SSH transport connect closed.'
