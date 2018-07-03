# _*_ coding:utf-8 _*_
# Filename: main_test.py
# Author: pang song
# python 2.7
# Date: 2018/06/24
# 352工具 服务器测试

import os
from flask import Flask, request, make_response, flash, render_template
from flask_bootstrap import Bootstrap
import json
import datetime
from flask import Flask, request, url_for, send_from_directory
from flask_cors import *

app = Flask(__name__)
CORS(app, supports_credentials=True)

bootstrap = Bootstrap(app)

# app.config.from_pyfile('config')


@app.route('/test', methods=['GET', 'POST'])
def test():
    return '<h1>Hello 3下5除2 在线小工具!</h1>'


# @app.route('/login1', methods=['GET', 'POST'])
# def login1():
#     from forms import LoginForm
#     form = LoginForm()
#     message = (
#         dict(
#             code=0,
#             msg='sucess',
#             data=u'用户名密码正确',
#          ),
#         dict(
#             code=1,
#             msg='error',
#             data=u'用户名或密码错误',
#         ),
#     )
#     if request.method == 'GET':
#         # flash(u'登陆成功')
#         return render_template('login.html', title=u'登录', form=form)
#     elif request.method == 'POST':
#         if form.username.data == 'pangsong':
#             return json.dumps(message[0], ensure_ascii=False)
#         else:
#             return json.dumps(message[1], ensure_ascii=False)
#     else:
#         return render_template('404.html')

#
# @app.route('/base')
# def base():
#     return render_template('base.html')
#

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# @app.route('/sendjson', methods=['POST'])
# def sendjson():
#     # 接收前端发来的数据,转化为Json格式,我个人理解就是Python里面的字典格式
#     data = json.loads(request.get_data())
#     # 然后在本地对数据进行处理,再返回给前端
#     name = data["name"]
#     age = data["age"]
#     location = data["location"]
#     data["time"] = "2016"
#
#     # Output: {u'age': 23, u'name': u'Peng Shuang', u'location': u'China'}
#     # print data
#     return jsonify(data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = (
        dict(
            code=0,
            msg='sucess',
            data=u'用户名密码正确',
         ),
        dict(
            code=1,
            msg='error',
            data=u'用户名或密码错误',
        ),
    )
    if request.method == 'GET':
        # flash(u'登陆成功')
        return '<h1>请使用post方法</h1>'
    elif request.method == 'POST':
        data = json.loads(request.get_data())
    
        if data["uname"] == 'pangsong':
            return json.dumps(message[0], ensure_ascii=False)
        else:
            return json.dumps(message[1], ensure_ascii=False)
    else:
        return render_template('404.html')



if __name__ == '__main__':
    # 局域网访问调试
    app.run(host='127.0.0.1', port=8090, debug=True)
    # 本机调试
    # app.run(debug=True)
