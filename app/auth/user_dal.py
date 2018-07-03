# _*_ coding:utf-8 _*_

from ..model import user_model
from ..utils import mysql_utils
from . import hash


class UserDal:
    def __init__(self):
        pass
    persist = None

    # 通过用户名及密码查询用户对象
    @classmethod
    def login_auth(cls, params):
        password = hash.salted_password(params['password'])

        sql = "select * from 352dt_user_info where uname = %s and password = %s"
        row = mysql_utils.Database().query_one(sql, (params['uname'], password))
        if row is not None:
            user = user_model.User(uid=row[1], uname=row[2], usergroup=row[4])
            # 实例化一个对象，将查询结果逐一添加给对象的属性
        else:
            return None

        return user

    # 通过用户名及密码注册对象
    @classmethod
    def register(cls, params):
        if cls.register_name_check(params):
            password = hash.salted_password(params['password'])
            if 'user_group' in params.keys():
                user_group = params['user_group']
            else:
                user_group = '12345'
            sql = "insert into 352dt_user_info (uid, uname, password, user_group, ctime, utime) " \
                  "values (UUID(), %s, %s, %s, now(), now())"
            mysql_utils.Database().insert_del_update(sql, (params['uname'], password, user_group))
            return True
        else:
            return False

    # 通过用户名及密码注册对象
    @classmethod
    def register_name_check(cls, params):
        sql = "select * from 352dt_user_info where uname = %s "
        row = mysql_utils.Database().query_one(sql, (params['uname'],))
        print(row)
        if row is not None:
            return False
        else:
            return True
