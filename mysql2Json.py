#!/usr/bin/python
# coding=utf-8

import MySQLdb, sys
from MySQLdb import cursors
from collections import OrderedDict

class MysqlPython(object):
    """
        Python Class for connecting  with MySQL server and accelerate development project using MySQL
        Extremely easy to learn and use, friendly construction.
    """

    __instance   = None
    __host       = 'kaz16mysqlmedium.ckh7idnurzxi.us-west-2.rds.amazonaws.com'
    __user       = 'kazrootuser'
    __password   = 'GAS23ips'
    __database   = 'KYW2'
    __session    = None
    __connection = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance or not cls.__database:
             cls.__instance = super(MysqlPython, cls).__new__(cls,*args,**kwargs)
        return cls.__instance
    ## End def __new__

    #def __init__(self, host='localhost', user='root', password='', database=''):
    def __init__(self):
        self.__host     = self.__host
        self.__user     = self.__user
        self.__password = self.__password
        self.__database = self.__database
    ## End def __init__

    def __open(self):
        try:
            cnx = MySQLdb.connect(self.__host, self.__user, self.__password, self.__database, cursorclass=MySQLdb.cursors.DictCursor)
            self.__connection = cnx
            self.__session    = cnx.cursor()
        except MySQLdb.Error as e:
            print("Error %d: %s" % (e.args[0],e.args[1]))
    ## End def __open

    def __close(self):
        self.__session.close()
        self.__connection.close()
    ## End def __close

    def get_next(self, query_select):

        self.__open()
        self.__session.execute(query_select)
        number_rows = self.__session.rowcount
        number_columns = len(self.__session.description)

        result =self.__session.fetchall()
        return result


    def custom_query(self, sql):
        result = []
        self.__open()
        self.__session.execute(sql)
        self.__connection.commit()
        number_rows = self.__session.rowcount
	if number_rows > 0:
              result = self.__session.fetchall()
        self.__close()
        return result

## End class
