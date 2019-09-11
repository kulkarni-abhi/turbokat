import os
import sys
import web
import json
import putil
import urllib
from login import Login
from urlparse import urlparse
from dashboard import Dashboard
from monitor import Monitor

urls = ('/', 'LoginPage', '/login', 'LoginPage', '/logout', 'LogoutPage',
        '/loginFailed', 'LoginFailedPage', '/dashboard', 'DashboardPage',
        '/checkin', 'CheckinPage', '/checkout', 'CheckoutPage', '/monitor',
        'MonitorPage', '/insert', 'InsertDataPage', '/update', 'UpdateDataPage',
        '/servers', 'ServerPage', '/add', 'ServerPage')

webserver = sys.argv[1]
web.config.debug = False
app = web.application(urls, locals())
session = web.session.Session(app, web.session.DiskStore('sessions'))

render = web.template.render('templates/')


class LoginPage:

    def GET(self):
        return render.index()

    def POST(self):
        data = web.data()
        vals = data.split('&')
        params = dict()
        for pair in vals:
            key, val = pair.split('=')
            params[key] = urllib.unquote(val)
        login = Login()
        if not login.authenticate(**params):
            session.logged_in = False
            raise web.seeother('/loginFailed')
        session.logged_in = True
        session.fullname = login.fullname()
        session.role = login.role()
        session.username = login.username()
        raise web.seeother('/dashboard?username={0}&fullname={1}'.format(
            login.username(), login.fullname()))


class LoginFailedPage:

    def GET(self):
        return render.loginFailed()


class LogoutPage:

    def GET(self):
        session.logged_in = False
        raise web.seeother('/')


class DashboardPage:

    def GET(self):
        input = web.input()
        if session.logged_in:
            dashboard = Dashboard()
            dashboard.servers(input.username)

            fields = ['os']
            aggregation = {
                'aggr_fun': 'COUNT',
                'aggr_field': 'id',
                'alias': 'osCount',
                'groupby': 'os'
            }

            user_data = dashboard.server_distribution(
                input.username, aggregation=aggregation, fields=fields)

            aggregation['alias'] = 'serverCount'

            all_data = dashboard.server_distribution(
                'NULL', aggregation=aggregation, fields=fields)

            return render.dashboard(input.username, input.fullname, user_data,
                                    all_data)
        else:
            raise web.seeother('/loginFailed')


class CheckinPage:

    def GET(self):
        input = web.input()
        if session.logged_in:
            dashboard = Dashboard()
            dashboard.checkin_server(input.username, input.id, input.hostname,
                                     input.os)
            raise web.seeother('/dashboard?username={0}&fullname={1}'.format(
                session.username, session.fullname))
        else:
            raise web.seeother('/loginFailed')


class CheckoutPage:

    def GET(self):
        input = web.input()
        if session.logged_in:
            dashboard = Dashboard()
            dashboard.checkout_server(input.username, input.id, input.hostname,
                                      input.os, webserver)
            raise web.seeother('/dashboard?username={0}&fullname={1}'.format(
                session.username, session.fullname))
        else:
            raise web.seeother('/loginFailed')


class InsertDataPage:

    def GET(self):
        input = web.input()
        putil.insertDb(input)


class UpdateDataPage:

    def GET(self):
        input = web.input()
        putil.updateDb(input)


class MonitorPage:

    def GET(self):
        input = web.input()
        if session.logged_in:
            monitor = Monitor()
            monitor.filesystems(input.id)
            monitor.processors(input.id)
            monitor.memory(input.id)
            return render.monitor(session.username, session.fullname, input.id,
                                  input.hostname)
        else:
            raise web.seeother('/loginFailed')

class ServerPage:

    def GET(self):
        msg = ""
        return render.servers(session.username, session.fullname)

    def POST(self):
        input = web.input()
        print input
        dashboard = Dashboard()
        dashboard.add_server(input.hostname, input.ip, input.user, input.password, input.os, input.desc)
        raise web.seeother('/dashboard?username={0}&fullname={1}'.format(
            session.username, session.fullname))

if __name__ == '__main__':
    app.run()
