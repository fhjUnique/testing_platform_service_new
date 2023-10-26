from django.http import HttpResponse
from testing_platform_service.utils.check_api import check_request
from testing_platform_service.utils.jwt_authentication import create_token
from testing_platform_service.utils.execute_sql import Exsql
from testing_platform_service.utils.config import *
import logging, json

logger = logging.getLogger('api_public')


# 登录接口
@check_request('post', ['username', 'userpassword'])
def api_login(request):
    response = {}
    code = -1
    user_info_data = {}
    param = str(request.body, 'utf-8')
    param_obj = json.loads(param)
    username = param_obj['username']
    userpassword = param_obj['userpassword']
    user_info = Exsql.query_sql_one(
        'select ui.*,ur.role from user_info as ui left join user_role as ur on ui.id=ur.user where ui.is_deleted="f" and ui.account=%s',
        [username])
    # 判断用户是否存在
    if user_info['result'] == None:
        message = '账号未找到'
    else:
        if userpassword == user_info['result']['password']:
            if user_info['result']['is_active'] == 't':
                result = {}
                token_info = {
                    'id': user_info['result']['id'],
                    'account': username,
                    'name': user_info['result']['name'],
                    'role': user_info['result']['role']
                }
                token = create_token(token_info, token_expiration_time)  # 创建token
                result['name'] = user_info['result']['name']
                result['account'] = user_info['result']['account']
                result['create_time'] = user_info['result']['create_time']
                result['email'] = user_info['result']['email']
                result['phone'] = user_info['result']['phone']
                result['sex'] = user_info['result']['sex']
                result['token'] = token
                code, message, user_info_data = 0, '登录成功', result
            else:
                message = '账号已冻结，请联系管理员处理！'
        else:
            message = '密码错误'
    response["code"] = code
    response["msg"] = message
    response['data'] = user_info_data
    return HttpResponse(json.dumps(response, ensure_ascii=False))
