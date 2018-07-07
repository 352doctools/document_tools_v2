# _*_ coding:utf-8 _*_

from flask import render_template, request
import json
import user_dal

from . import auth
from app.utils.is_json import is_json
from app.utils.post_json import post_json


@auth.route('/login', methods=['GET', 'POST'])
def login():
        if request.method == 'GET':
            return '<h1>请使用post方法</h1>'
        elif request.method == 'POST':
            if is_json(request.get_data()):
                data = json.loads(request.get_data())
                if 'uname' in data.keys() and 'password' in data.keys():
                    user = user_dal.UserDal().login_auth(data)
                else:
                    return '输入参数不完整或者不正确'
            else:
                return '输入参数不完整或者不正确'
            if user is not None:
                return post_json(0, 'success', user.to_dict())
            else:
                return post_json(data='用户名或密码错误')
        else:
            return render_template('404.html')


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'GET':
        return '<h1>请使用post方法</h1>'
    elif request.method == 'POST':
        if is_json(request.get_data()):
            data = json.loads(request.get_data())
            if 'uid' in data.keys() and 'uname' in data.keys():
                success = True
            else:
                return '输入参数不完整或者不正确'
        else:
            return '输入参数不完整或者不正确'
        data = json.loads(request.get_data())
        if success:
            return post_json(0, 'success', data='用户登出成功')
        else:
            return post_json(data='用户登出失败')
    else:
        return render_template('404.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return '<h1>请使用post方法</h1>'
    elif request.method == 'POST':
        if is_json(request.get_data()):
            data = json.loads(request.get_data())
            if 'uname' in data.keys() and 'password' in data.keys():
                success = user_dal.UserDal().register(data)
            else:
                return '输入参数不完整或者不正确'
        else:
            return '输入参数不完整或者不正确'
        if success:
            return post_json(0, 'success', data='注册成功')
        else:
            return post_json(data='注册失败')
    else:
        return render_template('404.html')


@auth.route('/register_name_check', methods=['GET', 'POST'])
def register_name_check():
    if request.method == 'GET':
        return '<h1>请使用post方法</h1>'
    elif request.method == 'POST':
        if is_json(request.get_data()):
            data = json.loads(request.get_data())
            if 'uname' in data.keys():
                success = user_dal.UserDal().register_name_check(data)
            else:
                return '输入参数不完整或者不正确'
        else:
            return '输入参数不完整或者不正确'

        if success:
            return post_json(0, 'success', data='注册用户名不存在，可以注册')
        else:
            return post_json(data='注册用户名已经存在，换一个用户名试试')
    else:
        return render_template('404.html')
