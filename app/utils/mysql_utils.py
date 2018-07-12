# _*_ coding:utf-8 _*_
# import MySQLdb

# import datetime
import os

import mysql.connector
import ConfigParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


cf = ConfigParser.ConfigParser()
filename = 'config.ini'
curr_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(curr_dir, filename)
cf.read(config_file)  # 读取配置文件

remoteSSH = False
# 这个参数主要是用于控制远程ssh连接数据库还是本地连接数据库,True为远程，False为本地

server_ip = cf.get("Database", "server_ip")
ssh_username = cf.get("Database", "ssh_username")
ssh_password = cf.get("Database", "ssh_password")
user = cf.get("Database", "user")
password = cf.get("Database", "password")
host = cf.get("Database", "host")
database = cf.get("Database", "database")
charset = cf.get("Database", "charset")


def get_server():
    if remoteSSH:
        from sshtunnel import SSHTunnelForwarder
        return SSHTunnelForwarder(
                (server_ip, 22),
                ssh_password=ssh_password,
                ssh_username=ssh_username,
                remote_bind_address=(host, 3306)
                )
    return None


class Database:
    server = get_server()

    def __init__(self):
        config = dict(
            user=user,
            password=password,
            host=host,
            database=database,
            charset=charset,
        )
        if remoteSSH:
            self.server.start()
            config = dict(
                user=user,
                password=password,
                host=host,
                port=self.server.local_bind_port,
                database=database,
                charset=charset,
            )

        try:
            self.connection = mysql.connector.connect(**config)
        except Exception, err:
            print(err)
        self.cursor = self.connection.cursor(buffered=True, dictionary=True)

    def insert_del_update(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            row_count = self.cursor.rowcount
            self.connection.commit()
            return row_count
        except Exception, err:
            print err
            self.connection.rollback()

    def insert_del_update_query_one(self, query1, query2, params1=(), params2=()):
        try:
            self.cursor.execute(query1, params1)
            self.cursor.execute(query2, params2)
            self.connection.commit()
        except Exception, err:
            print err
            self.connection.rollback()
        return self.cursor.fetchone()

    def query_one(self, query, params=()):
        try:
            self.cursor.execute(query, params)
        except Exception, err:
            print err
        return self.cursor.fetchone()

    def query_all(self, query, params=()):
        try:
            self.cursor.execute(query, params)
        except Exception, err:
            print err
        return self.cursor.fetchall()

    def __del__(self):
        self.cursor.close()
        self.connection.close()
        if remoteSSH:
            self.server.stop()

