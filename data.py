import random
import sqlite3


# 获取数据
def get_data(obj, oid, ctime):
    database_path = "./static/comments.db"
    connect = sqlite3.connect(database_path)
    cur = connect.cursor()
    sql = 'select %s,count(%s) from av%s where av%s.ctime<=%s group by %s' % (obj, obj, oid, oid, ctime, obj)

    datalist = cur.execute(sql)
    data = []
    scroll = []
    for item in datalist:
        scroll.append(item[0])
        data.append({'value': item[1], 'name': item[0]})

    cur.close()
    connect.close()
    return {'scroll': scroll, 'data': data}


# 随机生成访问id
def guid():
    model = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
    pool = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    uid = ''
    for i in range(len(model)):
        if model[i] == '-':
            uid += '-'
            continue
        uid += pool[random.randint(0, len(pool) - 1)]
    return uid
