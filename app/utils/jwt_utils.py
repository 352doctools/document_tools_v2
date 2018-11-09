# _*_ coding:utf-8 _*_
import jwt
import datetime
import hashlib
import post_json

SECRET_KEY = 'secret'


# 生成jwt 信息
def encode_auth_token(user_id, login_time):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=3600),
            'iat': datetime.datetime.utcnow(),
            'iss': 'ken',
            'data': {
                'id': user_id,
                'login_time': login_time
            }
        }
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        return e


# # 注销jwt 信息
# def destroy_auth_token(user_id, login_time):
#     try:
#         payload = {
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=0),
#             'iat': datetime.datetime.utcnow(),
#             'iss': 'ken',
#             'data': {
#                 'id': user_id,
#                 'login_time': login_time
#             }
#         }
#         return jwt.encode(
#             payload,
#             SECRET_KEY,
#             algorithm='HS256'
#         )
#     except Exception as e:
#         return e


# 解析jwt 信息
def decode_auth_token(auth_token):
    try:
        # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
        # 取消过期时间验证
        payload = jwt.decode(auth_token, SECRET_KEY, leeway=datetime.timedelta(seconds=3600))
        if 'data' in payload and 'id' in payload['data']:
            return payload
        else:
            raise jwt.InvalidTokenError
    except jwt.ExpiredSignatureError:
        return 'Token过期'
    except jwt.InvalidTokenError:
        return '无效Token'


# 获取uid
def get_uid_token(request):
    auth_header = request.headers.get('Authorization')
    auth_tokenArr = auth_header.split(" ")
    auth_token = auth_tokenArr[1]
    payload = decode_auth_token(auth_token)
    uid = payload['data']['id']
    return uid, auth_token
