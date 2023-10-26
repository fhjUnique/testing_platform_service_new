# coding=utf-8
from django.http import HttpResponse
import json,base64
import logging
logger = logging.getLogger('django')
class Md1:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print('校验用户信息')
        try:
            token = request.headers['token']
            userInfo = token.split('.')[1]
            userInfo = userInfo + '=' * (4 - len(userInfo) % 4) if len(userInfo) % 4 != 0 else userInfo
            userInfo = json.loads(str(base64.b64decode(userInfo), 'utf-8'))
            request.META['userInfo'] = userInfo
            print('=====',userInfo)
        except:
            pass
        # 校验用户信息
        # try:
        #     token = request.headers['token']
        #     userInfo = token.split('.')[1]
        #     userInfo = userInfo + '=' * (4 - len(userInfo) % 4) if len(userInfo) % 4 != 0 else userInfo
        #     userInfo = json.loads(str(base64.b64decode(userInfo), 'utf-8'))
        #     logger.info(userInfo)
        #     # 用户信息添加至请求头中
        #     request.META['userInfo'] = userInfo
        #     id = userInfo['id']
        #     account = userInfo['account']
        #     user_info = Exsql.query_sql_one(
        #         'select count(*) as count from user_info where is_delete=0 and id = %s and account = %s', [id, account])
        #     if user_info['code'] == 0:
        #         if user_info['result']['count'] == 0:
        #             response = {'code': -1, 'msg': '未找到用户信息'}
        #             return HttpResponse(json.dumps(response, ensure_ascii=False))
        #         else:
        #             # 校验用户权限
        #             url = request.path
        #             adminPermissionPath = ['/addOrg', '/updateOrg', '/delOrg', '/queryOrg', '/addUserInfo',
        #                                    '/updateUserInfo', '/delUserInfo', '/queryUserInfo']
        #             if account != 'admin' and url in adminPermissionPath:
        #                 response = {'code': -1, 'msg': '您无权限！'}
        #                 return HttpResponse(json.dumps(response, ensure_ascii=False))
        # except Exception as e:
        #     logger.error(str(e))
            # response = {'code': -1, 'msg': '用户校验失败', 'data': str(e)}
            # return HttpResponse(json.dumps(response, ensure_ascii=False))

        response = self.get_response(request)
        return response

    # 执行完所有中间件的process_request方法
    def process_view(self, request, view_func, view_args, view_kwargs):
        pass

    # 中间件在收到request请求之后执行
    def process_request(self,request):
        print('process_request====')
        print('process_request====', request.body)

        print(request.body)
        print(request.method)

    # 执行视图函数的过程中如果引发异常，则按照settings.py中MIDDLEWARE_CLASSES的顺序，倒序执行process_exception方法
    def process_exception(self,request,exception):
        # response = {'code':-1,'msg':'系统异常，请联系管理员！'}
        # return HttpResponse(json.dumps(response, ensure_ascii=False))
        pass


    # 在视图函数执行结束之后执行
    def process_template_response(self,request, response):
        print("process_template_response在视图函数执行结束之后执行...")


    # 在视图函数执行结束之后执行
    def process_response(self, request, response):
        print("process_response在视图函数执行结束之后执行...")
