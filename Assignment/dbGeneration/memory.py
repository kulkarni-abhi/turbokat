import time
from datetime import datetime
import random
from MySql import MySql

ts = time.time()
vmIds = [1,2,3,6]
memory_capacities = [2048, 4096, 8192]
total = memory_capacities[random.randint(0,2)]


for vmId in vmIds:
    for i in range(300):
        table = 'memory'
        ts += 60
 
        values = {
            'vmId' : vmId,
            'total': total,
            'used' : random.randint(1024,total-100),
            'timestamp': datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        }

        values['free'] = values['total'] - values['used']


        db = MySql(
                host='10.105.4.76',
                db='inventory',
                user='admin',
                passwd='admin',
                autocommit=True,
                keep_alive=True)

        db.insert(table, values)
