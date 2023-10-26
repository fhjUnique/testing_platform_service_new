import json


# 转为json类型
def dumps(data):
    if data is None:
        return data
    try:
        if type(data) == str:
            new_data = data.replace('\'', '"')
            json.loads(new_data)
        else:
            new_data = json.dumps(data, ensure_ascii=False)
    except Exception as e:
        try:
            new_data = str(data, 'utf-8')
        except Exception as e:
            new_data = str(data)
            print(repr(e))
    return new_data


# json类型转为对象
def loads(data):
    if data is None:
        return data
    try:
        if type(data) == str:
            new_data = data.replace('\'', '"')
            new_data = json.loads(new_data)
        else:
            try:
                new_data = str(data, 'utf-8')
            except:
                new_data = str(data)
            new_data = new_data.replace('\'', '"')
            new_data = json.loads(new_data)
    except Exception as e:
        print(repr(e))
        new_data = str(data, 'utf-8')
    return new_data
