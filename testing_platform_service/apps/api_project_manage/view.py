from django.http import HttpResponse
from testing_platform_service.utils.check_api import check_request
from testing_platform_service.utils.execute_sql import Exsql
import json, logging

logger = logging.getLogger('api_project_manage')

"""
    查询所有项目
"""


@check_request('post')
def api_get_project(request):
    response = {}
    code = -1
    project = Exsql.query_sql_all('select * from project where is_deleted="f" order by create_time desc')
    if project['code'] == 0:
        code, message = 0, '查询成功'
    else:
        message = '查询失败'
    response["code"] = code
    response["msg"] = message
    response['data'] = project.get('result')
    return HttpResponse(json.dumps(response, ensure_ascii=False))


"""
    新增项目
    name:必填 文本
    describe：非必填 文本
"""


@check_request('post', ['name'])
def api_add_project(request):
    user_info = request.META['userInfo']
    user_id = user_info.get('id')
    response = {}
    code = -1
    param = str(request.body, 'utf-8')
    param_obj = json.loads(param)
    project_dict = {
        'name': param_obj['name'],
        'describe': param_obj.get('describe'),
        'create_by': str(user_id)
    }
    project = Exsql.create('project', project_dict)
    if project['code'] == 0:
        code, message = 0, '新增成功'
    else:
        message = '新增失败'
    response["code"] = code
    response["msg"] = message
    response['data'] = {}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


"""
    编辑项目
"""


@check_request('post', ['id'])
def api_update_project(request):
    response = {}
    code = -1
    param = str(request.body, 'utf-8')
    param_obj = json.loads(param)
    field_set = {
        'name': param_obj.get('name'),
        'describe': param_obj.get('describe'),
    }
    project = Exsql.update('project', field_set, {"id": param_obj.get('id')})
    if project['code'] == 0:
        code, message = 0, '编辑成功'
    else:
        message = '编辑失败'
    response["code"] = code
    response["msg"] = message
    response['data'] = {}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


"""
    删除项目
    id:必填 int
"""


@check_request('post', ['id'])
def api_delete_project(request):
    response = {}
    code = -1
    param = str(request.body, 'utf-8')
    param_obj = json.loads(param)
    project = Exsql.update('project', {"is_deleted": "t"}, {"id": param_obj.get('id')})
    if project['code'] == 0:
        code, message = 0, '删除成功'
    else:
        message = '删除失败'
    response["code"] = code
    response["msg"] = message
    response['data'] = {}
    return HttpResponse(json.dumps(response, ensure_ascii=False))
