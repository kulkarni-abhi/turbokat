import time
from datetime import datetime
import random
from MySql import MySql

ts = time.time()

table = 'processors'
vmIds = [1,2,3,6]
cpuRange = [1,2,4,8]

for vmId in vmIds:
    cpuCnt = cpuRange[random.randint(0,3)]
    for cpu in range(cpuCnt):
        for i in range(60):
            ts += 60
            values = {
                'vmId': vmId,
                'name': 'cpu#{0}'.format(cpu),
                'percent_used': random.randint(10,100),
                'timestamp': datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            }

            db = MySql(
                host='10.105.4.76',
                db='inventory',
                user='admin',
                passwd='admin',
                autocommit=True,
                keep_alive=True)

            db.insert(table, values)
