import math
import sqlite3
import random

import requests

# 存储进度数据
progress_data = {}


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


def get_ua():
    user_agents = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
        'Opera/8.0 (Windows NT 5.1; U; en)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) ',
    ]
    user_agent = user_agents[random.randint(0, len(user_agents) - 1)]
    return user_agent


def crawl(oid, uid):
    url = "https://api.bilibili.com/x/v2/reply/main"
    database_path = "./static/comments.db"

    headers = {
        "User_Agent": get_ua()
    }

    params = {
        "next": 0,
        "type": 1,
        "oid": oid,
        "mode": 2,
        "plat": 1
    }

    # 连接数据库
    conn = sqlite3.connect(database_path)
    # 获取游标
    cursor = conn.cursor()

    # sql语句
    table_name = f"av{oid}"
    sql_create_table = '''
        create table IF not exists %s
        (
        id integer primary key autoincrement ,
        floor integer ,
        ctime integer ,
        user_name text,
        user_sex text,
        user_level integer ,
        vip_level text,
        card_name text,
        card_number text,
        up_name text,
        comment_content text
        )
    ''' % table_name
    sql_find_max = 'select MAX(ctime) from %s' % table_name
    sql_find_min = 'select MIN(ctime) from %s' % table_name

    cursor.execute(sql_create_table)
    page = 0
    isOver = False
    while not isOver:
        # 更新参数
        params["next"] = page
        progress_data[uid] = page
        # 获取评论
        response = requests.get(url=url, params=params, headers=headers)
        # 加工数据
        (isOver, page) = process_data(reps=response, cursor=cursor, table_name=table_name)
        response.close()

    cursor.execute(sql_find_max)
    end_time = cursor.fetchall()[0][0]
    cursor.execute(sql_find_min)
    start_time = cursor.fetchall()[0][0]
    conn.commit()
    conn.close()
    return start_time, end_time


# 处理数据
def process_data(reps, cursor, table_name, floor=0):
    # print(reps.url)
    # json数据
    comments_json = reps.json()
    # print(comments_json)

    # 当"replies"对应的值为空值时，到达评论区底部停止爬取
    if not comments_json["data"].get("replies", 0):
        return True, floor

    comments_json = comments_json["data"]["replies"]
    # 用于储存需要的评论数据
    dic = {}

    for comment in comments_json:
        # print(comment["floor"])
        # 楼层
        dic["floor"] = comment["floor"]
        floor = comment["floor"]
        # 评论时间
        dic["ctime"] = comment["ctime"]

        member = comment["member"]
        # 用户名称
        dic["user_name"] = member["uname"]
        # 用户性别
        dic["user_sex"] = member["sex"]
        # 用户等级
        dic["user_level"] = member["level_info"]["current_level"]
        # 用户会员等级
        vip = "普通会员"
        if member["vip"]["vipType"] == 1:
            vip = "大会员"
        elif member["vip"]["vipType"] == 2:
            vip = "年度大会员"
        dic["vip_level"] = vip

        # 装扮名称
        dic["fanCard_name"] = "无"
        # 装扮编号
        dic["fanCard_id"] = "000000"
        # 装扮所属up主
        dic["fanCard_up"] = "无"
        # 当该用户有个性粉丝装扮的时候
        if member["user_sailing"].get("cardbg", 0) and member["user_sailing"]["cardbg"]["fan"]["is_fan"] == 1:
            cardbg = member["user_sailing"]["cardbg"]
            dic["fanCard_name"] = cardbg["name"]
            dic["fanCard_id"] = cardbg["fan"]["num_desc"]
            dic["fanCard_up"] = cardbg["fan"]["name"]

        # 评论内容
        dic["content"] = comment["content"]["message"].replace('\'', '‘')

        sql_find_floor = 'select count(*) from %s where floor=%d' % (table_name, dic["floor"])
        cursor.execute(sql_find_floor)
        if cursor.fetchall()[0][0] != 0:
            return True, floor

        sql_insert = '''
            insert into %s(floor, ctime, user_name, user_sex, user_level, vip_level, card_name, card_number, up_name, comment_content)
            values(%d, %d, '%s', '%s', %d, '%s', '%s', '%s', '%s', '%s')
        ''' % (
        table_name, dic["floor"], dic["ctime"], dic["user_name"], dic["user_sex"], dic["user_level"], dic["vip_level"],
        dic["fanCard_name"], dic["fanCard_id"], dic["fanCard_up"], dic["content"])
        # print(sql_insert)
        cursor.execute(sql_insert)

    print(f"已处理至{floor}")
    return False, floor


# 获取进度
def get_process(uid):
    return progress_data[uid]
