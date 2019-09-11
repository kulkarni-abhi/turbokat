import os
import json
import time
import subprocess
import collections
from MySql import MySql
from Constants import *


def _connect_database():
    db = MySql(
        host=dbHost,
        db=dbName,
        user=dbUser,
        passwd=dbPass,
        autocommit=autoCommit,
        keep_alive=keepAlive)
    return db


def run_cmd(command, verbose=True, realtime=False, return_json=False):
    '''
    A tool to run shell command from python2
    examples:
    (result,output,error)=putil.run_cmd('ps ax')
    result: True or false

    when outfile is given. command output is written to a file instead of console
    when return_json is given. output is an json
    when realtime is given, response printed on console in realtime

    '''

    print("putil.run_cmd: %s" % (command))

    start_time = time.time()
    if not realtime:
        p = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        std_out, std_err = p.communicate()
        rc = p.returncode
    else:
        std_out = std_err = ''
        p = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1)
        for line in iter(p.stdout.readline, b''):
            print line,
            std_out += line
        p.stdout.close()
        p.wait()
        rc = p.returncode

    result = True
    elapsed = time.time() - start_time

    if rc != 0:
        result = False

    if std_out:
        std_out = std_out.strip()
    else:
        std_out = ''

    if std_err:
        std_err = std_err.strip()
    else:
        std_err = ''

    if return_json:
        json_output = {}
        try:
            json_output = json.loads(std_out)
        except Exception as ex:
            result = False
            json_output = std_out
            std_err += "\nFailed to load stdout into json: %s" % ex

    if (std_out and len(std_out) > 5000) or (std_err and len(std_err) > 5000):
        verbose = False

    if verbose:
        debug_str = "::exit   (%.2f secs)::%s\n::stdout (%d bytes)::\n%s\n::stderr (%d bytes)::\n%s" % (
            elapsed, rc, len(std_out), std_out, len(std_err), std_err)
    else:
        # none verbose
        global EXEC_ID
        try:
            EXEC_ID += 1
        except:
            EXEC_ID = 1
        if return_json:
            outfile_name = 'local_run_cmd_%s.json' % EXEC_ID
        else:
            outfile_name = 'local_run_cmd_%s.txt' % EXEC_ID
        outfile = os.path.join('/tmp', outfile_name)
        debug_str = "::exit   (%.2f secs)::%s\n::stdout (%d bytes)::\n%s\n" % (
            elapsed, rc, len(std_out), "please see output in " + outfile)

        with open(outfile, 'w') as f:
            data = collections.OrderedDict()
            data['host'] = 'localhost'
            data['command'] = command
            data['exit'] = rc
            data['stderr'] = std_err
            if return_json:
                data['stdout'] = json_output
            else:
                data['stdout'] = std_out.split('\n')
            f.write(json.dumps(data, indent=2))

    if result:
        print(debug_str)
    else:
        print(debug_str)

    if return_json:
        return result, json_output, std_err
    else:
        return result, std_out, std_err


def run_remote_cmd(hostname, osName, command):
    cur_dir = os.path.dirname(__file__)
    hosts_file = os.path.join(cur_dir, 'hosts')
    playbook = os.path.join(cur_dir, 'yamls/run_windows_cli.yml')
    if osName.lower() != 'windows':
        playbook = os.path.join(cur_dir, 'yamls/run_linux_cli.yml')

    cmd = "ansible-playbook -i {0} {1} --extra-vars=\"hostname={2} ignore_errors='yes' command='{3}'\"".format(
        hosts_file, playbook, hostname, command)
    return run_cmd(cmd)


def copy_file(hostname, osName, src, dst):
    cur_dir = os.path.dirname(__file__)
    hosts_file = os.path.join(cur_dir, 'hosts')
    playbook = os.path.join(cur_dir, "yamls", "copy_file_to_linux.yml")
    if osName.lower() == 'windows':
        playbook = os.path.join(cur_dir, "yamls", "copy_file_to_windows.yml")
    cmd = "ansible-playbook -i {0} {1} --extra-vars=\"src_file_path='{2}' hostname='{3}' verbose='True' dest_file_path='{4}' \"".format(
        hosts_file, playbook, src, hostname, dst)
    return run_cmd(cmd)


def delete_file(hostname, osName, filename):
    cur_dir = os.path.dirname(__file__)
    hosts_file = os.path.join(cur_dir, 'hosts')
    playbook = os.path.join(cur_dir, "yamls", "delete_file_linux.yml")
    if osName.lower() == 'windows':
        playbook = os.path.join(cur_dir, "yamls", "delete_file_windows.yml")
    cmd = "ansible-playbook -i {0} {1} --extra-vars=\"filename='{2}' hostname='{3}' \"".format(
        hosts_file, playbook, filename, hostname)
    return run_cmd(cmd)


def schedule_windows_task(hostname,id,webserver):
    cur_dir = os.path.dirname(__file__)
    src = os.path.join(cur_dir, 'bin', 'performance.py')
    dst = "C:\\performance.py"
    copy_file(hostname, 'windows', src, dst)

    src_bat = os.path.join(cur_dir, 'bin', '{0}.bat'.format(hostname))
    dst_bat = "C:\\performance.bat"
    cmd = "schtasks /create /sc minute /mo 1 /tn \"Performance\" /tr \"python C:\\\\performance.py {0} {1}\"".format(webserver,id)
    file = open(src_bat,"w")
    file.write(cmd)
    file.close()

    run_cmd("chmod 777 {0}".format(src_bat))    
    copy_file(hostname, 'windows', src_bat, dst_bat)

    cmd = dst_bat
    run_remote_cmd(hostname, 'windows', cmd)


def delete_windows_task(hostname):
    cmd = "schtasks /delete /tn \"Performance\" /f"
    run_remote_cmd(hostname, 'windows', cmd)
    delete_file(hostname, 'windows', "C:\\performance.py")


def schedule_linux_task(hostname,id,webserver):
    cur_dir = os.path.dirname(__file__)
    src = os.path.join(cur_dir, 'bin', 'performance.py')
    copy_file(hostname, 'linux', src, '/root/performance.py')

    cmd = "crontab -l > /tmp/cron.list"
    run_remote_cmd(hostname, 'linux', cmd)

    cmd = "echo \"* * * * * python /root/performance.py {0} {1}\" >> /tmp/cron.list".format(webserver,id)
    run_remote_cmd(hostname, 'linux', cmd)

    cmd = "crontab /tmp/cron.list"
    run_remote_cmd(hostname, 'linux', cmd)


def delete_linux_task(hostname):
    cur_dir = os.path.dirname(__file__)
    src = os.path.join(cur_dir, 'bin', 'performance.py')

    cmd = "crontab -l | grep -v performance.py > /tmp/cron.list"
    run_remote_cmd(hostname, 'linux', cmd)

    cmd = "crontab /tmp/cron.list"
    run_remote_cmd(hostname, 'linux', cmd)
    delete_file(hostname, 'linux', "/root/performance.py")
    delete_file(hostname, 'linux', "/tmp/cron.list")

def insertDb(input):
    db = _connect_database()
    args = dict(input)
    table = args['table']
    vmId = args['vmId']
    del args['table']

    db.insert(table,args)

def updateDb(input):
    db = _connect_database()
    args = dict(input)
    table = args['table']
    vmId = args['vmId']
    del args['table']
    db.update(table, args,
           ("vmId=%s", [vmId]))
