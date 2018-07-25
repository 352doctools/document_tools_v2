# _*_ coding:utf-8 _*_
# Filename: main_test.py
# Author: pang song
# python 2.7
# Date: 2018/06/24
# 352工具 服务器测试

from __init__ import create_app

if __name__ == '__main__':
    # 局域网访问调试
    create_app().run()
    # 本机调试
    # app.run(debug=True)

