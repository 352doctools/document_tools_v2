# _*_ coding:utf-8 _*_
# Filename: main_v2.py
# Author: pang song
# python 2.7
# Date: 2018/06/24
# 352工具 服务器测试

from __init__ import create_app

if __name__ == '__main__':
    # 局域网访问调试
    create_app().run(host='0.0.0.0', port=8190, debug=True)

    # 本机调试
    # app.run(debug=True)
