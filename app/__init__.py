# _*_ coding:utf-8 _*_
# Filename: main_test.py
# Author: pang song
# python 2.7
# Date: 2018/06/24
# 352工具 服务器测试


from flask_bootstrap import Bootstrap
from flask import Flask, request, redirect, g, session
from flask_cors import CORS
from flask_login import LoginManager
from utils import jwt_utils, post_json
from auth import user_dal

bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


# 用户鉴权
def identify(request):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_tokenArr = auth_header.split(" ")
        if not auth_tokenArr or auth_tokenArr[0] != 'JWT' or len(auth_tokenArr) != 2:
            result = False
        else:
            auth_token = auth_tokenArr[1]
            payload = jwt_utils.decode_auth_token(auth_token)
            if not isinstance(payload, str):
                # user = user_dal.UserDal().check_uid({'uid': payload['data']['id']})
                # if user is None:
                #     result = False
                # else:
                #     if payload['data']['id'] not in session:
                #         return False
                #     else:
                #         if user.login_time == payload['data']['login_time']:
                #             result = True
                #         else:
                #             result = False
                user = user_dal.UserDal().check_uid({'uid': payload['data']['id']})
                if user is None:
                    result = False
                else:
                    if payload['data']['id'] not in session:
                        return False
                    else:
                        if session[payload['data']['id']] != auth_token:
                            return False
                        else:
                            if user.login_time == payload['data']['login_time']:  # 防止浏览器重新发送请求token仍然有效， session二义性
                                result = True
                            else:
                                result = False
            else:
                result = False
    else:
        result = False
    return result

def create_app():
    app = Flask(__name__)
    app.secret_key = "secret"
    # 解决跨域问题
    # CORS(app, resources={r"/*": {"origins": "*"}}, send_wildcard=True)
    CORS(app, supports_credentials=True)
    # app.config["SESSION_COOKIE_PATH"] = None
    # app.config["SESSION_COOKIE_HTTPONLY"] = False



    @app.before_request
    def before_request():
        if request.path == '/login' or request.path == '/register' \
                or request.path == '/register_name_check' or request.path == '/doc_save' \
                or request.path == '/doc_keywords':
            return None
        if not identify(request):
            g.string = 'token认证失败'
        else:
            g.string = ''



    @app.after_request
    def after_request(response):
        # 服务器端
        # Access - Control - Allow - Credentials = true时，参数Access - Control - Allow - Origin
        # 的值不能为
        # '*' 。
        # response.headers.add('Access-Control-Allow-Origin', '*')
        origin = request.headers.get('Origin')
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers
        return response
    bootstrap.init_app(app)
    login_manager.init_app(app)

    from auth import auth as auth_blueprint
    from main import main as main_blueprint
    from doc import doc as doc_blueprint
    from other import other as other_blueprint

    app.register_blueprint(auth_blueprint)
    # app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint)
    app.register_blueprint(doc_blueprint)
    app.register_blueprint(other_blueprint)

    return app
