import os
import json
import putil
from Constants import *


class Dashboard():

    def __init__(self):
        self.db = putil._connect_database()
        self.tableName = serversTable

    def servers(self, username):
        rows = self.db.getAll(self.tableName)

        table = "<table class=\"table table-bordered\" id=\"dataTable\" width=\"100%\" cellspacing=\"0\">"
        table += "<thead>"
        thead = "<tr>"
        thead += "<th>Id</th>"
        thead += "<th>Hostname</th>"
        thead += "<th>IP Address</th>"
        thead += "<th>Operating System</th>"
        thead += "<th>Description</th>"
        thead += "<th>Owner</th>"
        thead += "<th>Action</th>"
        thead += "</tr>"
        table += thead
        table += "</thead>"
        table += "<tfoot>"
        table += thead
        table += "</tfoot>"

        if rows:
            table += "<tbody>"
            for row in rows:
                table += "<tr>"
                for x, col in enumerate(row[:-2]):
                    if col == None:
                        col = "-"

                    if x == 1:
                        col = "<a href=monitor?id={0}&hostname={1}>{2}</a>".format(
                            row[0], row[1], col)
                    table += "<td>{0}</td>".format(col)

                btnClass = "class=\"btn btn-link btn-sm\" role=\"button\""
                if row[-3] == None:
                    href = "checkout?id={0}&username={1}&hostname={2}&os={3}".format(
                        row[0], username, row[1], row[3])
                    checkout = "<a {0} href=\"{1}\">CheckOut</a>".format(
                        btnClass, href)
                    table += "<td>{0}</td>".format(checkout)
                elif row[-3] == username:
                    href = "checkin?id={0}&username={1}&hostname={2}&os={3}".format(
                        row[0], username, row[1], row[3])
                    checkin = "<a {0} href=\"{1}\">CheckIn</a>".format(
                        btnClass, href)
                    table += "<td>{0}</td>".format(checkin)
                elif row[-3] != username:
                    checkout = "<button type=\"button\" {0} disabled>NA</button>".format(
                        btnClass)
                    table += "<td>{0}</td>".format(checkout)

                table += "</tr>"
            table += "</tbody>"
            table += "</table>"

            html_file = "static/{0}-table.html".format(username)
            file = open(html_file, "w")
            file.write(table)
            file.close()

    def server_distribution(self,
                            username,
                            fields=["*"],
                            aggregation={},
                            where_clause={}):
        where_str = None
        where_clause["owner"] = username
        if len(where_clause) != 0:
            where_list = []
            for key in where_clause:
                where_list.append("%s='%s'" % (key, where_clause[key]))
            where_str = "where %s " % (" and ".join(where_list))
            if username == 'NULL':
                where_str = "where owner is NULL"

        group_by = None
        if len(aggregation) != 0:
            aggr_field = aggregation['aggr_field']
            aggr_function = aggregation['aggr_fun']
            alias = aggregation['alias']
            group_by = aggregation['groupby']

            fields.append("%s(%s) as %s" % (aggr_function, aggr_field, alias))

        sql = "select %s from %s" % (",".join(fields), self.tableName)
        if where_str != None:
            sql = "%s %s" % (sql, where_str)

        if group_by != None:
            sql = "%s group by %s" % (sql, group_by)

        sql = "%s order by %s" % (sql, "os")

        rows = None

        table_data_str = ""
        try:
            rows = self.db.run_query(sql)
        except:
            raise

        osTypes = ["CENTOS", "RHEL", "SLES", "UBUNTU", "WINDOWS"]
        osCount = [0, 0, 0, 0, 0]
        if rows != None:
            for row in rows:
                osCount[osTypes.index(row[0])] = int(row[1])

        return osCount

    def checkin_server(self, username, id, hostname, osName):
        ###Enable this piece of code only when you have valid IP addresses in table
        if osName.lower() == 'windows':
            putil.delete_windows_task(hostname)
        else:
            putil.delete_linux_task(hostname)
        self.db.update(self.tableName, {"owner": None}, ("id=%s", [id]))

    def checkout_server(self, username, id, hostname, osName, webserver):
        ###Enable this piece of code only when you have valid IP addresses in table
        if osName.lower() == 'windows':
            putil.schedule_windows_task(hostname, id, webserver)
        else:
            putil.schedule_linux_task(hostname, id, webserver)
        self.db.update(self.tableName, {"owner": username}, ("id=%s", [id]))

    def add_server(self, hostname, ip, user, password, osName, desc):
        data = {
            'hostname': hostname,
            'ipAddress': ip,
            'os': osName,
            'description': desc,
            'username': user,
            'passwd': password
        }
        self.db.insert(self.tableName, data)

        cur_dir = os.path.dirname(__file__)
        hosts_file = os.path.join(cur_dir, 'hosts')

        entry = "{0} ansible_port=5986 ansible_user={1} ansible_password={2}".format(
            ip, user, password)
        entry = "{0} ansible_connection=winrm ansible_winrm_server_cert_validation=ignore".format(
            entry)
        entry = "{0} ansible_winrm_operation_timeout_sec=60 ansible_winrm_read_timeout_sec=70 ".format(
            entry)
        if osName.lower() != "windows":
            entry = "{0} ansible_ssh_port=22 ansible_ssh_user={1} ansible_ssh_pass={2}".format(
                ip, user, password)
            entry = "{0} ansible_connection=ssh ansible_sudo_pass={1}".format(
                entry, password)

        file = open(hosts_file, "a")
        file.write("[{0}]\n".format(hostname))
        file.write("{0}\n".format(entry))
        file.close()
