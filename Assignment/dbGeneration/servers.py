import time
from datetime import datetime
import random
from MySql import MySql

ts = time.time()

table = 'servers'
servers = [
    ('10.105.5.187','testlink.local','testlink-server','CENTOS', 'abhishek'),
    ('10.105.5.189','docker.local','docker-server','UBUNTU', None),
    ('10.105.5.184','web-server.local','web-server','RHEL', None),
    ('10.105.5.182','nfs.local','nfs-server','SLES', None),
    ('10.105.5.185','cifs.local','cifs-server','WINDOWS', None)
]
vmIds = [1]

for vmId in vmIds:
    for server in servers:
            values = {
                'hostname' : server[1],
                'ipAddress': server[0],
                'os': server[3],
                'description': server[2],
                'username': 'root',
                'passwd': 'ca$hc0w',
                'owner': server[4]
            }

            db = MySql(
                host='10.198.36.31',
                db='inventory',
                user='admin',
                passwd='admin',
                autocommit=True,
                keep_alive=True)

            db.insert(table, values)
