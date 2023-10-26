from django.http import HttpResponse
from testing_platform_service.utils.check_api import check_request
from testing_platform_service.utils.execute_sql import Exsql
import json, logging

logger = logging.getLogger('api_users_manage')

"""
    新增用户
    name、account、password、email、phone、sex、role、project
"""


@check_request('post', ['name', 'account', 'password', 'confirm_password'])
def api_add_user(request):
    user_info = request.META['userInfo']
    user_id = user_info.get('id')
    response = {}
    code = -1
    param = str(request.body, 'utf-8')
    param_obj = json.loads(param)
    name = param_obj['name']
    account = param_obj.get('account')
    password = param_obj.get('password')
    confirm_password = param_obj.get('confirm_password')
    email = param_obj.get('email')
    phone = param_obj.get('phone')
    sex = param_obj.get('sex')
    role_id = param_obj.get('role')
    project_ids = param_obj.get('project')
    check_role_result = check_role(role_id)
    if password == confirm_password:
        user_dict = {
            'name': name,
            'account': account,
            'password': password,
            'email': email,
            'phone': phone,
            'sex': sex,
            'is_active': 't',
            'create_by': str(user_id)
        }
        if check_role_result:
            user_info = Exsql.create('user_info', user_dict)
            if user_info['code'] == 0:
                code, message = 0, '添加成功'
                # 用户角色关联
                user_id = user_info['result']
                Exsql.create('user_role', {"role": role_id, "user": user_id})
                if project_ids and len(project_ids) > 0:
                    fields_value = []
                    for project_id in project_ids:
                        fields_value.append((project_id, user_id))
                    Exsql.create_s('user_project', ['project', 'user'], fields_value)
            else:
                message = '添加失败'
        else:
            message = '未查询到角色！'
    else:
        message = '两次密码输入不一致！'
    response["code"] = code
    response["msg"] = message
    response['data'] = {}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


"""
    编辑用户
"""


@check_request('post', ['id', 'name', 'account'])
def api_update_user(request):
    response = {}
    code = -1
    param = str(request.body, 'utf-8')
    param_obj = json.loads(param)
    user_id = param_obj.get('id')
    role_id = param_obj.get('role')
    project_ids = param_obj.get('project')
    field_set = {
        'name': param_obj.get('name'),
        'account': param_obj.get('account'),
        'email': param_obj.get('email'),
        'phone': param_obj.get('phone'),
        'sex': param_obj.get('sex'),
    }
    user_info = Exsql.update('user_info', field_set, {"id": user_id})
    if user_info['code'] == 0:
        code, message = 0, '编辑成功'
        Exsql.update('user_role', {"is_deleted": "t"}, {"user": user_id, "is_deleted": "f"})
        Exsql.update('user_project', {"is_deleted": "t"}, {"user": user_id, "is_deleted": "f"})
        check_role_result = check_role(role_id)
        if check_role_result:
            Exsql.create('user_role', {"role": role_id, "user": user_id})
            if project_ids and len(project_ids) > 0:
                fields_value = []
                for project_id in project_ids:
                    fields_value.append((project_id, user_id))
                Exsql.create_s('user_project', ['project', 'user'], fields_value)
    else:
        message = '编辑失败'
    response["code"] = code
    response["msg"] = message
    response['data'] = {}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


"""
    启用/禁用用户
"""


@check_request('post', ['id', 'is_active'])
def api_operation_user(request):
    response = {}
    code = -1
    param = str(request.body, 'utf-8')
    param_obj = json.loads(param)
    user_id = param_obj.get('id')
    is_active = param_obj.get('is_active')
    field_set = {
        'is_active': is_active
    }
    user_info = Exsql.update('user_info', field_set, {"id": user_id, "is_deleted": "f"})
    if user_info['code'] == 0:
        code = 0
        if is_active == "t":
            message = '启用成功'
        else:
            message = '禁用成功'
    else:
        message = '操作失败'
    response["code"] = code
    response["msg"] = message
    response['data'] = {}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


"""
    删除用户
"""


@check_request('post', ['id'])
def api_delete_user(request):
    response = {}
    code = -1
    param = str(request.body, 'utf-8')
    param_obj = json.loads(param)
    user_id = param_obj.get('id')
    field_set = {
        'is_deleted': "t"
    }
    user_info = Exsql.update('user_info', field_set, {"id": user_id, "is_deleted": "f"})
    if user_info['code'] == 0:
        code, message = 0, '删除成功'
        Exsql.update_sql('delete from user_role where user=%s', [user_id])
        Exsql.update_sql('delete from user_project where user=%s', [user_id])
    else:
        message = '删除失败'
    response["code"] = code
    response["msg"] = message
    response['data'] = {}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


"""
    查询用户
"""


@check_request('post', )
def api_get_user(request):
    response = {}
    code = -1
    user_info = Exsql.query_sql_all(
        'select DISTINCT ui.*,role.id as role_id,role.name as role_name from user_info as ui left join user_role as ur on ui.id=ur.user left join (select * from role where is_deleted="f") as role on ur.role=role.id where ui.is_deleted="f" order by ui.create_time desc')
    if user_info['code'] == 0:
        code, message = 0, '查询成功'
        user_project = Exsql.query_sql_all(
            'select p.id,p.name,up.user from project as p left join user_project as up on p.id=up.project where p.is_deleted="f"')
        for item in user_info['result']:
            del item['password']
            item['project'] = []
            for item1 in user_project['result']:
                if item['id'] == item1['user']:
                    item['project'].append({"project": item1['id'], "name": item1['name']})
    else:
        message = '查询失败'
    response["code"] = code
    response["msg"] = message
    response['data'] = user_info['result']
    return HttpResponse(json.dumps(response, ensure_ascii=False))


# 校验角色是否存在
def check_role(role_id):
    is_exist = True
    if role_id:
        role = Exsql.query_sql_one('select count(*) as count from role where is_deleted="f" and id=%s', [role_id])
        if role['result'].get('count') == 0:
            is_exist = False
    return is_exist
