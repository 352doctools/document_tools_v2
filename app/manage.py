# _*_ coding:utf-8 _*_
# Filename: .py
# Author: pang song
# python 3.6
# Date: 2018/06/16
import os
from flask import Flask,request,make_response,render_template
from flask_bootstrap import Bootstrap
import datetime
from flask import Flask, request,jsonify, url_for, send_from_directory
import deal_word
# from werkzeug import secure_filename
import json


app = Flask(__name__)
bootstrap = Bootstrap(app)


# 测试
@app.route('/index', methods=['GET', 'POST'])
def index():
    return "<h1>Hello world!</h1>"


@app.route('/sendjson2',methods=['POST'])
def sendjson2():

    # 接收前端发来的数据,转化为Json格式,我个人理解就是Python里面的字典格式
    data = json.loads(request.get_data())

    # 然后在本地对数据进行处理,再返回给前端
    name = data["name"]
    age = data["age"]
    location = data["location"]
    data["time"] = "2016"

    # Output: {u'age': 23, u'name': u'Peng Shuang', u'location': u'China'}
    # print data
    return jsonify(data)


if __name__ == '__main__':
    app.run()
