# _*_ coding:utf-8 _*_

from flask_login import UserMixin


# define profile.json constant, the file is used to
#  save user name and password_hash
# 用户类
class User(UserMixin):
    def __init__(self, uid=None, uname=None, usergroup=None, nickname=None, mail=None, phone=None, login_time=None):
        self.uid = uid
        self.uname = uname
        self.usergroup = usergroup
        self.nickname = nickname
        self.mail = mail
        self.phone = phone
        self.login_time = login_time

    def to_dict(self):
        return self.__dict__

    def get_id(self):
        return self.uid
