# _*_ coding:utf-8 _*_

from model import user_model
from utils import mysql_utils
from . import hash

#用户类
class UserDal:
    def __init__(self):
        pass
    persist = None

    @classmethod #检查uid
    def check_uid(cls, params):
        sql = "select * from 352dt_user_info where uid = %s"
        row = mysql_utils.Database().query_one(sql, (params['uid'],))
        if row is not None:
            user = user_model.User(uid=row['uid'], uname=row['uname'], usergroup=row['user_group'],
                                   nickname=row['nickname'], mail=row['mail'], phone=row['phone'])
            # 实例化一个对象，将查询结果逐一添加给对象的属性
        else:
            return None
        return user

    # 通过用户名及密码查询用户对象
    @classmethod
    def login_auth(cls, params):
        passwd = hash.salted_password(params['passwd'])

        sql = "select * from 352dt_user_info where uname = %s and passwd = %s"
        row = mysql_utils.Database().query_one(sql, (params['uname'], passwd))
        if row is not None:
            user = user_model.User(uid=row['uid'], uname=row['uname'], usergroup=row['user_group'],
                                   nickname=row['nickname'], mail=row['mail'], phone=row['phone'])
            # 实例化一个对象，将查询结果逐一添加给对象的属性
        else:
            return None

        return user

    # 通过用户名及密码注册对象
    @classmethod
    def register(cls, params):
        if cls.register_name_check(params):
            passwd = hash.salted_password(params['passwd'])
            if 'user_group' in params.keys():
                user_group = params['user_group']
            else:
                user_group = '12345'
            if 'phone' in params.keys():
                phone = params['phone']
            else:
                phone = None
            sql = "insert into 352dt_user_info (uid, uname, passwd, user_group, nickname, mail, phone, ctime, utime) " \
                  "values (UUID(), %s, %s, %s, %s, %s, %s, now(), now())"
            rowcount = mysql_utils.Database().insert_del_update(sql, (params['uname'], passwd, user_group, params['nickname'],
                                                           params['mail'], phone,))
            if rowcount > 0:
                return True
        else:
            return False

    # 通过用户名及密码注册对象
    @classmethod
    def register_name_check(cls, params):
        sql = "select * from 352dt_user_info where uname = %s "
        row = mysql_utils.Database().query_one(sql, (params['uname'],))
        if row is not None:
            return False
        else:
            return True
