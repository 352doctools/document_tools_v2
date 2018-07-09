# _*_ coding:utf-8 _*_
# Filename: main_test.py
# Author: pang song
# python 2.7
# Date: 2018/06/24
# 352工具 服务器测试


from flask_bootstrap import Bootstrap
from flask import Flask
from flask_cors import *
from flask_login import LoginManager

bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    from auth import auth as auth_blueprint
    from main import main as main_blueprint
    from other import other as other_blueprint

    app.register_blueprint(auth_blueprint)
    # app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint)
    app.register_blueprint(other_blueprint)

    return app
