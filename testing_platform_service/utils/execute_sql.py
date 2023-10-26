import os, datetime

# Create your tests here.

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "old_feng_service.settings")
from django.db import connection, transaction
from testing_platform_service.utils.format_time import *
import logging

logger = logging.getLogger('django')


class Exsql():
    def query_sql_one(sql, params=None):
        result = {"code": 0, "result": ""}  # code状态0 = 执行成功，-1 = 执行失败
        with connection.cursor() as cursor:
            try:
                logger.info('query_sql_one>>>' + str(sql) + ' params=' + str(params))
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                fields_name = [desc[0] for desc in cursor.description]
                row = cursor.fetchone()
                if row:
                    exResult = dict(zip(fields_name, row))
                    values = list(exResult.values())
                    for i in range(len(values)):
                        if isinstance(values[i], datetime.datetime):
                            exResult[fields_name[i]] = values[i].strftime('%Y-%m-%d %H:%M:%S')
                    result['result'] = exResult
                else:
                    result['result'] = row
            except Exception as e:
                logger.info('error：query_sql_one>>>', str(e))
                result['code'] = -1
                result['result'] = str(e)
        return result

    # params数组
    # 最后一个参数为当前页数
    # 倒数第二个参数为一页多少条数据
    def query_sql_all(sql, params=None):
        result = {"code": 0, "result": ""}  # code状态0 = 执行成功，-1 = 执行失败
        # 分页处理
        currentPage = 0

        if params:
            extraParamCount = len(params) - str(sql).count('%s')
            if extraParamCount > 0:
                currentPage = params[-1]
                if currentPage != 0:
                    start = currentPage * 10 - 10
                    pageSize = 10
                    if extraParamCount == 2:
                        pageSize = params[-2]
                    limit = ' limit ' + str(start) + ',' + str(pageSize)
                    sql = sql + limit
                if extraParamCount == 1:
                    params = params[0:-1]
                elif extraParamCount == 2:
                    params = params[0:-2]
        logger.info('query_sql_all>>>' + str(sql) + ' params=' + str(params))
        with connection.cursor() as cursor:
            try:
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                fields_name = [desc[0] for desc in cursor.description]
                row = cursor.fetchall()
                if len(row) > 0:
                    row_list = []
                    for list in row:
                        item = dict(zip(fields_name, list))
                        item['pages_number'] = currentPage
                        row_list.append(item)
                    result['result'] = row_list
                else:
                    result['result'] = []
            except Exception as e:
                logger.info('error：query_sql_all>>>', str(e))
                result['code'] = -1
                result['result'] = str(e)
        return result

    def update_sql(sql, params=None):
        result = {"code": 0, "result": ""}  # code状态0 = 执行成功，-1 = 执行失败
        with connection.cursor() as cursor:
            try:
                logger.info('update_sql>>>' + str(sql) + ' params=' + str(params))
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                # result['result'] = cursor.lastrowid
                transaction.commit()
            except Exception as e:
                logger.info('error：update_sql>>>', str(e))
                result['code'] = -1
                result['result'] = e
                cursor.rollback()
        return result

    # db_name:表名称
    # field_set：需要修改的值，字典格式 {"name":"fenghujie"}
    # condition：条件，字典格式{"id":"10"}
    def update(db_name, field_set, condition=None):
        result = {"code": 0, "result": ""}  # code状态0 = 执行成功，-1 = 执行失败
        field_set_new = ''
        condition_new = ''
        for item in field_set:
            if str(field_set[item]) == '' or str(field_set[item]) == 'None':
                field_set_new += f"{item} = Null, "
            else:
                field_set_new += f"{item} = '{str(field_set[item])}', "
        field_set_new += f"update_time = '{get_now_time()}'"
        for item in condition:
            condition_new += f"{item} = '{str(condition[item])}' and "
        if condition:
            sql = "update %s set " + field_set_new + ' where ' + condition_new.rstrip('and ')
        else:
            sql = "update %s set " + field_set_new
        with connection.cursor() as cursor:
            try:
                logger.info('update>>>' + str(sql) % (db_name))
                cursor.execute(sql % (db_name))
                transaction.commit()
            except Exception as e:
                logger.info('error：update_sql>>>', str(e))
                result['code'] = -1
                result['result'] = e
                cursor.rollback()
        return result

    def create(dbName, data_dict):
        result = {"code": 0, "result": ""}  # code状态0 = 执行成功，-1 = 执行失败
        data_dict['create_time'] = get_now_time()
        data_dict['update_time'] = get_now_time()
        data_dict['is_deleted'] = 'f'
        data_dict = {k: None if v == '' else v for k, v in data_dict.items()}
        fields = str(tuple(data_dict.keys())).replace("'", "`")
        fields_value = tuple(data_dict.values())
        sql = """insert into %s %s values""" % (dbName, fields)
        with connection.cursor() as cursor:
            try:
                logger.info('create_sql>>>' + str(sql + '%s  ;fields_value=') + str(fields_value))
                cursor.execute(sql + '%s', [fields_value])
                result['result'] = cursor.lastrowid
                transaction.commit()
            except Exception as e:
                logger.info('error：create>>>', str(e))
                result['code'] = -1
                result['result'] = str(e)
                transaction.rollback()
        return result

    def create_s(dbName, fields, fields_value):
        result = {"code": 0, "result": ""}  # code状态0 = 执行成功，-1 = 执行失败
        value_ = []
        fields += ['is_deleted', 'create_time', 'update_time']
        new_fields_value = []
        for fv in fields_value:
            new_fields_value.append(fv + ('f', get_now_time(), get_now_time()))
        for i in range(len(fields)):
            value_.append("%s")
        value_ = str(tuple(value_)).replace("'", '')
        fields = str(tuple(fields)).replace("'", "")
        sql = """insert into %s %s values """ % (dbName, fields)
        print(sql + value_)
        with connection.cursor() as cursor:
            try:
                logger.info('create_sql>>>' + str(sql + value_) + '; fields_value=' + str(new_fields_value))
                cursor.executemany(sql + value_, new_fields_value)
                result['result'] = cursor.lastrowid
                transaction.commit()
            except Exception as e:
                logger.info('error：create_s>>>', str(e))
                result['code'] = -1
                result['result'] = str(e)
                transaction.rollback()
        return result



if __name__ == "__main__":
    # fields = ['order_id', 'product_id', 'classify_id', 'product_sum', 'price']
    # fields_type = ["%s", "%s", "%s", "%s", "%s"]
    # fields_value = [('456789123', 2,1, 1, 0.10)]
    # order_detail = Exsql.create_s('order_detail', fields, fields_value)
    # print(order_detail)
    # a = Exsql.query_sql_one("select price from order_form where shop_id = %s", ['123456'])
    # currentPage = 1
    # a = Exsql.query_sql_all('select order_id,price,is_pay,status,distribution_type,create_time from order_form where is_delete = 0 and organization = %s order by create_time desc',[43,currentPage] )
    # print(a)

    pass
