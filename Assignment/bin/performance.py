from __future__ import print_function
import sys
import os
import time
import psutil
import urllib.request
import urllib.parse
from datetime import datetime

webserver = sys.argv[1]
vmId = sys.argv[2]

def update_db(action,table,data):
    params = urllib.parse.urlencode(data)
    url = "http://{0}:8080/{1}&{2}".format(webserver,action,params)
    with urllib.request.urlopen(url) as response:
       html = response.read() 
       print(html)

def timestamp():
    ts = time.time()
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def convert_bytes(bytes, to, bsize=1024):
    """
       convert bytes to megabytes, etc.
       sample code:
           print('mb= ' + str(bytesto(314575262000000, 'm')))
       sample output:
           mb= 300002347.946
    """

    a = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
    r = float(bytes)
    for i in range(a[to]):
        r = r / bsize

    return(r)

def filesystem_usage():
    templ = "%-17s %18s %18s %18s %15s%%"
    print(templ % ("Mount", "Total", "Used", "Free", "Use "))
    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts or part.fstype == '':
                # skip cd-rom drives with no disk in it; they may raise
                # ENOENT, pop-up a Windows GUI error for a non-ready
                # partition or just hang.
                continue
        usage = psutil.disk_usage(part.mountpoint)
        capacity = int(convert_bytes(usage.total,"m"))
        used = int(convert_bytes(usage.used,"m"))
        free = int(convert_bytes(usage.free,"m")
        precent_used = int(usage.percent)
        print(templ % (
            part.mountpoint,
            capacity,
            used,
            free,
            percent_used))

        fsData = dict()
        fsData['vmId'] = vmId
        fsData['name'] = part.mountpoint
        fsData['capacity'] = capacity
        fsData['used'] = used
        fsData['available'] = free
        fsData['percent_used'] = percent_used
        fsData['timestamp'] = timestamp()
        update_db('update','filesystems',fsData)

def memory_usage():
    virt = psutil.virtual_memory()
    swap = psutil.swap_memory()
    print("Time: {0}".format(timestamp()))

    total = int(virt.total / 1024)
    free = int(virt.free / 1024)
    used = int(virt.used / 1024)

    templ = "%-10s %10s %10s %10s %10s %10s"
    print(templ % ('total', 'used', 'free', 'shared', 'buffers', 'cache'))
    print(templ % (
        total,
        used,
        free,
        int(getattr(virt, 'shared', 0) / 1024),
        int(getattr(virt, 'buffers', 0) / 1024),
        int(getattr(virt, 'cached', 0) / 1024)))

    memData = dict()
    memData['vmId'] = vmId
    memData['total'] = total
    memData['used'] = used
    memData['free'] = free
    memData['timestamp'] = timestamp()
    update_db('insert','memory',memData)

def cpu_usage():
    print("Time: {0}".format(timestamp()))
    num_cpus = psutil.cpu_count()
    if num_cpus > 8:
        num_cpus = 8  # try to fit into screen
        cpus_hidden = True
    else:
        cpus_hidden = False

    cpus_percent = psutil.cpu_percent(percpu=True)
    for i in range(num_cpus):
        print("CPU %-6i" % i, end="")
    if cpus_hidden:
        print(" (+ hidden)", end="")

    print()
    for id in range(num_cpus):
        name = "cpu#{0}".format(id)
        percent_used = cpus_percent.pop(0)
        print("%-10s" % percent_used, end="")
        cpuData = dict()
        cpuData['name'] = name
        cpuData['percent_used'] = percent_used
        cpuData['vmId'] = vmId
        cpuData['timestamp'] = timestamp()
        update_db('insert','processors',cpuData)
    print()

filesystem_usage()
print("\n")
memory_usage()
print("\n")
cpu_usage()
