import time
from datetime import datetime
import random
from MySql import MySql

ts = time.time()

table = 'filesystems'
filesystems = ['/', '/tmp', '/var', '/data']
vmIds = [1,2,3,6]

for vmId in vmIds:
    for fs in filesystems:
        for i in range(1):
            ts += 60
            values = {
                'capacity' : random.randint(20,150) * 1024,
                'vmId': vmId,
                'name': fs,
                'timestamp': datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            }

            values['used'] = random.randint(1,values['capacity'])
            values['available'] = values['capacity'] - values['used']
            values['percent_used'] = values['used'] * 100 / values['capacity']

            db = MySql(
                host='10.198.36.31',
                db='inventory',
                user='admin',
                passwd='admin',
                autocommit=True,
                keep_alive=True)

            db.insert(table, values)
