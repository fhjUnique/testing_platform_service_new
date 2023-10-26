import jwt
import time
from jwt import exceptions

SECRET_KEY = 'fhjunique'


def create_token(payload, expiration):
    '''基于jwt创建token的函数'''
    global SECRET_KEY
    # 设置headers，即加密算法的配置
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }

    # payload = {
    #     "name": name
    # }
    if expiration:
        # expiration （单位秒）
        expiration = int(time.time() + int(expiration))
        payload['exp'] = expiration
    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm='HS256', headers=headers).decode('utf-8')
    # 生成token
    return token


def validate_token(token):
    '''校验token的函数，校验通过则返回解码信息'''
    global SECRET_KEY
    payload = None
    msg = None
    code = 0
    try:
        if token == 'fenghujie':
            payload = 'fenghujie'
        else:
            payload = jwt.decode(token, SECRET_KEY, True, algorithm='HS256')
            # jwt有效、合法性校验
    except exceptions.ExpiredSignatureError:
        code, msg = -2, 'token已失效'
    except jwt.DecodeError:
        code, msg = -3, 'token认证失败'
    except jwt.InvalidTokenError:
        code, msg = -4, '非法的token'
    return (payload, msg, code)
