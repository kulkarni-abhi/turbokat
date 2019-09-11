import json
import putil
from Constants import *


class Monitor():

    def __init__(self):
        self.tableName = "filesystems"
        self.db = putil._connect_database()

    def filesystems(self, vmId):
        self.tableName = 'filesystems'

        rows = self.db.getAll(
            self.tableName,
            fields=("name", "available", "used", "percent_used", "capacity"),
            where=("vmId = %s", [vmId]))

        table = "<table class=\"table table-sm table-bordered\" id=\"dataTable\" width=\"100%\" cellspacing=\"0\">"
        table += "<thead>"
        thead = "<tr>"
        thead += "<th>Name</th>"
        thead += "<th>Free (MB)</th>"
        thead += "<th>Used (MB)</th>"
        thead += "<th>Used (%)</th>"
        thead += "<th>Capacity (MB)</th>"
        thead += "</tr>"
        table += thead
        table += "</thead>"

        if rows:
            table += "<tbody>"
            for row in rows:
                table += "<tr>"
                for col in row:
                    table += "<td>{0}</td>".format(col)
                table += "</tr>"
            table += "</tbody>"
            table += "</table>"

            html_file = "static/fs-summary-{0}".format(vmId)
            file = open(html_file, "w")
            file.write(table)
            file.close()

    def processors(self, vmId):
        self.tableName = 'processors'
        sql = "select distinct name from %s where vmId=%s" % (self.tableName,
                                                              vmId)
        rows = self.db.run_query(sql)
        json_data = dict()
        json_data['data'] = list()
        json_data['animationEnabled'] = True
        json_data['exportEnabled'] = True
        json_data['axisY'] = {"title": "Percentage"}
        json_data['toolTip'] = {"shared": True}
        json_data['legend'] = {
            "cursor": "pointer",
            "itemclick": "toggleDataSeries"
        }

        if rows:
            for row in rows:
                for col in row:
                    innerSql = "select * from %s where vmId=%s and name='%s'" % (
                        self.tableName, vmId, col)
                    innerSql = "%s order by id desc limit 60" % innerSql
                    sql = "select percent_used,timestamp from (%s)var1 order by id asc" % innerSql
                    innerRows = self.db.run_query(sql)
                    cpuData = dict()
                    cpuData["type"] = "spline"
                    cpuData["name"] = col
                    cpuData["showInLegend"] = True
                    cpuData["dataPoints"] = list()
                    if innerRows:
                        for irow in innerRows:
                            cpuData["dataPoints"].append({
                                "label": irow[1],
                                "y": irow[0]
                            })
                        json_data['data'].append(cpuData)
        file = open("static/processor_chart_template.js")
        text = file.read()
        file.close()

        text = text.replace('JSON_DATA', json.dumps(json_data))
        file = open("static/{0}-processor-chart.js".format(vmId), "w")
        file.write(text)
        file.close()

    def memory(self, vmId):
        self.tableName = 'memory'
        innerSql = "select * from %s where vmId=%s" % (self.tableName, vmId)
        innerSql = "%s order by id desc limit 60" % (innerSql)
        sql = "select used,timestamp from (%s)var1 order by id asc" % innerSql
        rows = self.db.run_query(sql)

        json_data = dict()
        if rows:
            json_data['animationEnabled'] = True
            json_data['axisY'] = {'title': 'Used (Mb)'}
            json_data['data'] = list()
            memoryData = dict()
            memoryData['type'] = "splineArea"
            memoryData['color'] = "rgba(54,158,173,.7)"
            memoryData['markerSize'] = 5
            memoryData['dataPoints'] = list()
            for row in rows:
                memoryData['dataPoints'].append({'label': row[1], 'y': row[0]})
            json_data['data'].append(memoryData)
        file = open("static/memory_chart_template.js")
        text = file.read()
        file.close()

        text = text.replace('JSON_DATA', json.dumps(json_data))
        file = open("static/{0}-memory-chart.js".format(vmId), "w")
        file.write(text)
        file.close()
