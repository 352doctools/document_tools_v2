# _*_ coding:utf-8 _*_

from flask import render_template, request, g, session
from flask_login import logout_user
import json
import user_dal
from . import auth
from utils.is_json import is_json
from utils.post_json import post_json
import utils.jwt_utils as jwt_utils
import time


# 登陆路由
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return post_json('error', '请使用post方法')
    elif request.method == 'POST':
        login_time = int(time.time())
        if is_json(request.get_data()):
            data = json.loads(request.get_data())
            if 'uname' in data.keys() and 'passwd' in data.keys():
                user = user_dal.UserDal().login_auth(data, login_time)
            else:
                return post_json('error', '输入参数不完整或者不正确')
        else:
            return post_json('error', '输入参数不完整或者不正确')
        if user is not None:
            token = jwt_utils.encode_auth_token(user.uid, login_time)
            session.pop(user.uid, None)
            session[user.uid] = token
            return post_json('success', data=token.decode())
        else:
            return post_json('error', '用户名或密码错误')
    else:
        return render_template('404.html')


# 获得用户信息
@auth.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'GET':
        return post_json('error', '请使用post方法')
    elif request.method == 'POST':
        if g.string == 'token认证失败':
            return post_json('error', g.string)
        uid = jwt_utils.get_uid_token(request)[0]
        user_temp = user_dal.UserDal().check_uid({'uid': uid})
        return post_json('success', data=user_temp.to_dict())
    else:
        return render_template('404.html')


# 登出路由
@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'GET':
        return post_json('error', '请使用post方法')
    elif request.method == 'POST':
        login_time = int(time.time())
        if g.string == 'token认证失败':
            return post_json('error', g.string)
        else:
            uid = jwt_utils.get_uid_token(request)[0]
            session.pop(uid, None)
            user_dal.UserDal().update_login_time(uid, -login_time)
            success = True
        if success:
            return post_json('success', '用户登出成功')
        else:
            return post_json('error', '用户登出失败')
    else:
        return render_template('404.html')


# 注册路由
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return post_json('error', '请使用post方法')
    elif request.method == 'POST':
        if is_json(request.get_data()):
            data = json.loads(request.get_data())
            if 'uname' in data.keys() and 'passwd' in data.keys() and 'nickname' in data.keys() \
                    and 'mail' in data.keys():
                success = user_dal.UserDal().register(data)
            else:
                return post_json('error', '输入参数不完整或者不正确')
        else:
            return post_json('error', '输入参数不完整或者不正确')
        if success:
            return post_json('success', '注册成功')
        else:
            return post_json('error', '注册失败')
    else:
        return render_template('404.html')


# 注册用户名重复检查路由
@auth.route('/register_name_check', methods=['GET', 'POST'])
def register_name_check():
    if request.method == 'GET':
        return post_json('error', '请使用post方法')
    elif request.method == 'POST':
        if is_json(request.get_data()):
            data = json.loads(request.get_data())
            if 'uname' in data.keys():
                success = user_dal.UserDal().register_name_check(data)
            else:
                return post_json('error', '输入参数不完整或者不正确')
        else:
            return post_json('error', '输入参数不完整或者不正确')

        if success:
            return post_json('success', '注册用户名不存在，可以注册')
        else:
            return post_json('error', '注册用户名已经存在，换一个用户名试试')
    else:
        return render_template('404.html')
