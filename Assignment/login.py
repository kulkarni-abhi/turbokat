import putil
from MySql import MySql
from Constants import *


class Login():

    def __init__(self):
        self.db = putil._connect_database()
        self.tableName = usersTable

    def username(self):
        return self._username

    def firstname(self):
        return self._firstname

    def lastname(self):
        return self._lastname

    def role(self):
        return self._role

    def fullname(self):
        return "{0} {1}".format(self._firstname.title(), self._lastname.title())

    def authenticate(self, username=None, password=None):
        row = self.db.getOne(
            self.tableName, where=("username = %s", [username]))

        if row:
            if username == row[3] and password == row[4]:
                self._username = username
                self._firstname = row[1]
                self._lastname = row[2]
                self._role = row[5]
                return True
        return False
