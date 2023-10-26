from django.http import HttpResponse
from testing_platform_service.utils.check_api import check_request
from testing_platform_service.utils.execute_sql import Exsql
from testing_platform_service.utils.format_time import *
import json, logging

logger = logging.getLogger('api_role_manage')

"""
    获取用户菜单（根据配置的菜单权限来获取）
    无需传参
"""


@check_request('post')
def api_get_user_permission(request):
    response = {}
    code = -1
    user_info = request.META['userInfo']
    role_id = user_info.get('role')
    if user_info.get('account') == 'admin1':
        menu = Exsql.query_sql_all('select * from permission where is_deleted="f" and type="menu" order by sort desc')
    else:
        menu = Exsql.query_sql_all(
            'select pe.id,pe.name,pe.code,pe.parent_id,rp.is_operation from permission as pe left join role_permission as rp on pe.id=rp.permission where pe.is_deleted="f" and pe.type="menu" and rp.role=%s order by pe.sort desc',
            [role_id])
    menu_data = format_menu_data(menu.get('result'))
    response["code"] = code
    response["msg"] = '成功'
    response['data'] = menu_data
    return HttpResponse(json.dumps(response, ensure_ascii=False))


"""
    获取所有菜单权限列表
    无需传参
"""


@check_request('post')
def api_get_permission(request):
    response = {}
    code = -1
    menu = Exsql.query_sql_all('select * from permission where is_deleted="f" and type="menu" order by sort desc')
    menu_data = format_menu_data(menu.get('result'))
    response["code"] = code
    response["msg"] = '成功'
    response['data'] = menu_data
    return HttpResponse(json.dumps(response, ensure_ascii=False))


"""
    新增权限
    （必填参数）'name','code','type','sort','parent_id'
"""


@check_request('post', ['name', 'code', 'type', 'parent_id'])
def api_add_permission(request):
    response = {}
    code = -1
    param = str(request.body, 'utf-8')
    param_obj = json.loads(param)
    permission_dict = {
        'name': param_obj['name'],
        'code': param_obj.get('code'),
        'type': param_obj.get('type'),
        'sort': param_obj.get('sort'),
        'parent_id': param_obj.get('parent_id')
    }
    role = Exsql.create('permission', permission_dict)
    if role['code'] == 0:
        code, message = 0, '新增权限成功'
    else:
        message = '新增权限失败'
    response["code"] = code
    response["msg"] = message
    response['data'] = {}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


"""
    编辑权限
    （必填参数）'id'
"""


@check_request('post', ['id'])
def api_update_permission(request):
    response = {}
    code = -1
    param = str(request.body, 'utf-8')
    param_obj = json.loads(param)
    permission = Exsql.update('permission', param_obj, {'id': param_obj.get('id')})
    if permission['code'] == 0:
        code, message = 0, '编辑权限成功'
    else:
        message = '编辑权限失败'
    response["code"] = code
    response["msg"] = message
    response['data'] = {}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


"""
    删除权限
    id:必填 int
"""


@check_request('post', ['id'])
def api_delete_permission(request):
    response = {}
    code = -1
    param = str(request.body, 'utf-8')
    param_obj = json.loads(param)
    permission = Exsql.update_sql('update permission set is_deleted="t" where id=%s', param_obj.get('id'))
    if permission['code'] == 0:
        code, message = 0, '删除成功'
    else:
        message = '删除失败'
    response["code"] = code
    response["msg"] = message
    response['data'] = {}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


"""
    获取角色列表
"""


@check_request('post')
def api_get_role_list(request):
    response = {}
    code = -1
    role = Exsql.query_sql_all('select * from role where is_deleted="f" order by create_time desc')
    if role['code'] == 0:
        code, message = 0, '查询成功'
    else:
        message = '查询失败'
    response["code"] = code
    response["msg"] = message
    response['data'] = role.get('result')
    return HttpResponse(json.dumps(response, ensure_ascii=False))


"""
    获取角色详情
"""


@check_request('post', ['id'])
def api_get_role_detail(request):
    response = {}
    code = -1
    param = str(request.body, 'utf-8')
    param_obj = json.loads(param)
    role = Exsql.query_sql_one('select * from role where is_deleted="f" order by create_time desc')
    result = role.get('result')
    if role['code'] == 0:
        code, message = 0, '查询成功'
        # 获取自己拥有的菜单
        own_menu = Exsql.query_sql_all(
            'select pe.id,pe.name,pe.code,pe.parent_id,rp.is_operation from permission as pe left join role_permission as rp on pe.id=rp.permission where pe.is_deleted="f" and pe.type="menu" and rp.role=%s order by pe.sort desc',
            [param_obj.get('id')])
        result['permission'] = own_menu['result']
    else:
        message = '查询失败'
    response["code"] = code
    response["msg"] = message
    response['data'] = result
    return HttpResponse(json.dumps(response, ensure_ascii=False))


"""
    新增角色
    name:必填 文本
    describe：非必填 文本
    permission：非必填，格式为[{"id":1,"is_operation":"t"}]
"""


@check_request('post', ['name'])
def api_add_role(request):
    user_info = request.META['userInfo']
    user_id = user_info.get('id')
    response = {}
    code = -1
    param = str(request.body, 'utf-8')
    param_obj = json.loads(param)
    role_dict = {
        'name': param_obj['name'],
        'describe': param_obj.get('describe'),
        'create_by': str(user_id)
    }
    role = Exsql.create('role', role_dict)
    if role['code'] == 0:
        code, message = 0, '新增角色成功'
        # 角色关联菜单权限
        role_id = role['result']
        permission = param_obj.get('permission')
        if permission and len(permission) > 0:
            field_values = []
            for item in permission:
                field_values.append((role_id, item['id'], item['is_operation']))
            Exsql.create_s('role_permission', ['role', 'permission', 'is_operation'], field_values)
    else:
        message = '新增角色失败'
    response["code"] = code
    response["msg"] = message
    response['data'] = {}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


"""
    编辑角色
    id:必填 int
    name:必填 文本
    describe：非必填 文本
    permission：非必填，格式为[{"id":1,"is_operation":"t"}]
"""


@check_request('post', ['id', 'name'])
def api_update_role(request):
    response = {}
    code = -1
    param = str(request.body, 'utf-8')
    param_obj = json.loads(param)
    role_param = [
        param_obj.get('name'),
        param_obj.get('describe'),
        get_now_time(),
        param_obj.get('id'),
    ]
    role = Exsql.update_sql('update role set `name`=%s,`describe`=%s,`update_time`=%s where id=%s', role_param)
    if role['code'] == 0:
        code, message = 0, '编辑角色成功'
        # 角色关联菜单权限

        permission = param_obj.get('permission')
        Exsql.update_sql('update role_permission set is_deleted="t" where role=%s', [param_obj.get('id')])
        if permission and len(permission) > 0:
            field_values = []
            for item in permission:
                field_values.append((param_obj.get('id'), item['id'], item['is_operation']))
            Exsql.create_s('role_permission', ['role', 'permission', 'is_operation'], field_values)
    else:
        message = '编辑角色失败'
    response["code"] = code
    response["msg"] = message
    response['data'] = {}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


"""
    删除角色
    id:必填 int
"""


@check_request('post', ['id'])
def api_delete_role(request):
    response = {}
    code = -1
    param = str(request.body, 'utf-8')
    param_obj = json.loads(param)
    role = Exsql.update_sql('update role set is_deleted="t" where id=%s', param_obj.get('id'))
    if role['code'] == 0:
        code, message = 0, '删除成功'
        Exsql.update_sql('delete from role_permission where role=%s', param_obj.get('id'))
    else:
        message = '删除失败'
    response["code"] = code
    response["msg"] = message
    response['data'] = {}
    return HttpResponse(json.dumps(response, ensure_ascii=False))


# 将菜单转换为树状格式
def format_menu_data(menu_result):
    menu_data = []
    menu_children = []
    for item in menu_result:
        if item.get('parent_id') == 0:
            item['children'] = []
            menu_data.append(item)
        else:
            menu_children.append(item)

    for children_item in menu_children:
        for index, item1 in enumerate(menu_data):
            if children_item.get('parent_id') == item1.get('id'):
                menu_data[index]['children'].append(children_item)
    return menu_data
