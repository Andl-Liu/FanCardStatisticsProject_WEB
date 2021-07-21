import sqlite3
import random
from time import sleep

import requests

# 存储进度数据
progress_data = {}


# 随机产生一个user_agent
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
    sleep_point = 0
    page = 0
    isOver = False
    while not isOver:
        # 更新参数
        params["next"] = page
        progress_data[uid] = page
        headers['User_Agent'] = get_ua()
        if sleep_point == 0:
            sleep_point = page
        # 每爬取500条左右的评论，休眠5s
        if sleep_point - page >= 500:
            print('休息5s')
            sleep_point = page
            sleep(5)
        # 获取评论
        response = requests.get(url=url, params=params, headers=headers)
        # 加工数据
        (isOver, page) = process_data(reps=response, cursor=cursor, table_name=table_name)
        response.close()

    # 获取最早评论的时间和最晚评论的时间
    cursor.execute(sql_find_max)
    end_time = cursor.fetchall()[0][0]
    cursor.execute(sql_find_min)
    start_time = cursor.fetchall()[0][0]
    # 将变动提交的数据库
    conn.commit()
    cursor.close()
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

        # 当获取到数据库中已经存在的评论的时候，停止查询
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
