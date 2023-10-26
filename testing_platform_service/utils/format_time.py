import datetime, time

def get_now_time(strftime='%Y-%m-%d %H:%M:%S'):
    now_time = datetime.datetime.now().strftime(strftime)
    return now_time

def get_now_timestamp():
    now_time =  time.time() * 1000
    return now_time

# 获取前1天或N天的日期，beforeOfDay=1：前1天；beforeOfDay=N：前N天
def getBeforeDay(beforeOfDay):
    today = datetime.datetime.now()
    # 计算偏移量
    offset = datetime.timedelta(days=-beforeOfDay)
    # 获取想要的日期的时间
    re_date = (today + offset).strftime('%Y-%m-%d')
    return re_date

