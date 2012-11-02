#
#from quantum.db import api as db
#from quantum.plugins.openvswitch.ruijie import ruijie_db
#
#db_connection_url = 'mysql://root:ruijie@127.0.0.1:3306/ovs_quantum'
#options = {"sql_connection": db_connection_url}
#options.update({"sql_max_retries": -1})
#options.update({"reconnect_interval": 2})
#db.configure_db(options)



    
    
    
#mysql> select uuid,tenant_id,name,op_status from networks;
#+--------------------------------------+-----------+--------+-----------+
#| uuid                                 | tenant_id | name   | op_status |
#+--------------------------------------+-----------+--------+-----------+
#| 19f87b8b-586a-4cb0-90a4-1353dc5021b9 | miaosf    | net500 | UP        |
#| 1cc1e64f-cc38-4231-885a-8ff255b89dd8 | miaosf    | net100 | UP        |
#| b5c46bcc-e3b7-4859-a0c0-1a3edcb89e79 | miaosf    | net3   | UP        |
#| d7ab5ef4-858e-4bd4-a9ba-de1bae1bb000 | miaosf    | net2   | UP        |
#| fa16a2fe-2fb8-4884-ad74-c6766909834e | miaosf    | net100 | UP        |
#+--------------------------------------+-----------+--------+-----------+
#
#
#
#mysql> select uuid,network_id,interface_id,state, op_status from ports;                   
#+--------------------------------------+--------------------------------------+----------------+-------+-----------+
#| uuid                                 | network_id                           | interface_id   | state | op_status |
#+--------------------------------------+--------------------------------------+----------------+-------+-----------+
#| 397cedd8-a5f3-4aa8-8cfd-42a5dfe89d5e | fa16a2fe-2fb8-4884-ad74-c6766909834e |                | DOWN  | DOWN      |
#| 686799b4-2115-4386-adf5-ba6f076adfd6 | 1cc1e64f-cc38-4231-885a-8ff255b89dd8 | NULL           | DOWN  | DOWN      |
#| a1d10a14-3966-46eb-8a2c-508c715775fe | 19f87b8b-586a-4cb0-90a4-1353dc5021b9 | 11111-2222     | DOWN  | DOWN      |
#| ae69eb70-03a8-4530-b0d3-69031042a4c2 | b5c46bcc-e3b7-4859-a0c0-1a3edcb89e79 | gw-e4cdc032-c8 | DOWN  | UP        |
#| eea7c69a-b70f-4131-8eb4-ea57859314a6 | d7ab5ef4-858e-4bd4-a9ba-de1bae1bb000 | miaosf_port    | DOWN  | DOWN      |
#+--------------------------------------+--------------------------------------+----------------+-------+-----------+
#
#
#mysql> select vlan_id,network_id from vlan_bindings;
#+---------+--------------------------------------+
#| vlan_id | network_id                           |
#+---------+--------------------------------------+
#|       1 | 1cc1e64f-cc38-4231-885a-8ff255b89dd8 |
#|       2 | d7ab5ef4-858e-4bd4-a9ba-de1bae1bb000 |
#|       3 | b5c46bcc-e3b7-4859-a0c0-1a3edcb89e79 |
#|       4 | 19f87b8b-586a-4cb0-90a4-1353dc5021b9 |
#+---------+--------------------------------------+
#4 rows in set (0.00 sec)
