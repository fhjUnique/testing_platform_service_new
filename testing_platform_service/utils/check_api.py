import json

from django.http import HttpResponse
from .jwt_authentication import validate_token


# 装饰器：接口参数校验
def check_request(method, *check_request_args):
    def wrapper(func):
        def decorate(*wrapper_args, **kw):
            request = wrapper_args[0]
            code = 0
            message = '请求失败'
            data = ''
            print('request.path===',request.path)
            if request.method.lower() != method.lower():  # 校验请求类型
                code = -1
                data = '请求类型应为' + method.upper()
            if code == 0 and request.path not in ['/login','/wipeWatermarkLogin','/wxPreview','/receiveMessage']:
                if request.path == '/preview':
                    preview_token = request.GET.get('token')
                    if preview_token:
                        payload, msg, token_err_code = validate_token(preview_token)
                        if not payload:
                            code, message = token_err_code, msg
                    else:
                        code, data = -5, '当前请求需要用户认证'
                else:
                    if not 'Token' in request.headers.keys():  # 校验token是否失效
                        code, data = -5, '当前请求需要用户认证'
                    else:
                        payload, msg, token_err_code = validate_token(request.headers['token'])
                        if not payload:
                            code, message = token_err_code, msg
            if code == 0 and len(check_request_args) > 0 and request.path not in ['/api_users_manage','/imgMatting']:  # 校验参数
                not_param = []  # 未传递的参数
                require_fields = check_request_args[0]  # 需要接受的参数
                request_param = str(request.body, 'utf-8')
                if request_param:
                    try:
                        json.loads(request_param)  # 传递过来的参数
                    except Exception:
                        code, data = -1, '参数传递有误'
                    param_obj = json.loads(request_param)
                    param_keys = list(param_obj.keys())
                    for require_field in require_fields:
                        if not require_field in param_keys:
                            not_param.append(require_field)
                    if len(not_param) > 0:
                        code, data = -1, '缺少必需参数 ' + str(not_param)

                else:
                    code, data = -1, '未传递参数'
            if code in (-1, -2, -3,-4,-5):
                response = {'code': code, 'msg': message, 'data': data}
                return HttpResponse(json.dumps(response, ensure_ascii=False))
            return func(*wrapper_args, **kw)

        return decorate

    return wrapper
