import math
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
    print(uid)
    return uid


# 将bv号转化为对应的av号的后缀
# 代码来自：https://blog.csdn.net/qq_42306041/article/details/109067461
# 以及：   https://www.bilibili.com/video/BV1R7411y7kw
def BvToAv(bv):
    # 1.去除Bv号前的"Bv"字符
    BvNo1 = bv[2:]
    keys = {
        '1': '13', '2': '12', '3': '46', '4': '31', '5': '43', '6': '18', '7': '40', '8': '28', '9': '5',
        'A': '54', 'B': '20', 'C': '15', 'D': '8', 'E': '39', 'F': '57', 'G': '45', 'H': '36', 'J': '38', 'K': '51',
        'L': '42', 'M': '49', 'N': '52', 'P': '53', 'Q': '7', 'R': '4', 'S': '9', 'T': '50', 'U': '10', 'V': '44',
        'W': '34', 'X': '6', 'Y': '25', 'Z': '1',
        'a': '26', 'b': '29', 'c': '56', 'd': '3', 'e': '24', 'f': '0', 'g': '47', 'h': '27', 'i': '22', 'j': '41',
        'k': '16', 'm': '11', 'n': '37', 'o': '2',
        'p': '35', 'q': '21', 'r': '17', 's': '33', 't': '30', 'u': '48', 'v': '23', 'w': '55', 'x': '32', 'y': '14',
        'z': '19'

    }
    # 2. 将key对应的value存入一个列表
    BvNo2 = []
    for index, ch in enumerate(BvNo1):
        BvNo2.append(int(str(keys[ch])))

    # 3. 对列表中不同位置的数进行*58的x次方的操作

    BvNo2[0] = int(BvNo2[0] * math.pow(58, 6))
    BvNo2[1] = int(BvNo2[1] * math.pow(58, 2))
    BvNo2[2] = int(BvNo2[2] * math.pow(58, 4))
    BvNo2[3] = int(BvNo2[3] * math.pow(58, 8))
    BvNo2[4] = int(BvNo2[4] * math.pow(58, 5))
    BvNo2[5] = int(BvNo2[5] * math.pow(58, 9))
    BvNo2[6] = int(BvNo2[6] * math.pow(58, 3))
    BvNo2[7] = int(BvNo2[7] * math.pow(58, 7))
    BvNo2[8] = int(BvNo2[8] * math.pow(58, 1))
    BvNo2[9] = int(BvNo2[9] * math.pow(58, 0))

    # 4.求出这10个数的合
    sum = 0
    for i in BvNo2:
        sum += i
    # 5. 将和减去100618342136696320
    sum -= 100618342136696320
    # 6. 将sum 与177451812进行异或
    temp = 177451812

    return sum ^ temp