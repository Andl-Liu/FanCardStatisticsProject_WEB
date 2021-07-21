import os

from flask import Flask, render_template, request, jsonify
from crawler import *
from data import *
from wordclouds import *

app = Flask(__name__)


# 首页
@app.route('/')
def index():
    return render_template("index.html", uid=guid())


# 爬取数据，显示页面
@app.route('/process')
def process():
    # 将bv号转化为对应的av号的后缀
    bv = request.args.get("bv")
    uid = request.args.get("uid")
    oid = BvToAv(bv)
    # 爬取评论数据并将数据储存在数据库
    start_time, end_time = crawl(oid=oid, uid=uid)

    return render_template("show.html", oid=oid, start_time=start_time, end_time=end_time)


# 接受请求，查找数据并返回至页面
@app.route('/get_data', methods=['GET', 'POST'])
def get_data_web():
    obj = request.args.get('obj')
    oid = request.args.get('oid')
    ctime = request.args.get('ctime')
    json = jsonify(get_data(obj=obj, oid=oid, ctime=ctime))
    return json


# 展示加载的进度
@app.route('/show_process')
def show_process():
    uid = request.args.get('uid')
    floor = get_process(uid=uid)
    print(floor)
    return jsonify({'floor': floor})


# 获取词云
@app.route('/get_wordcloud')
def get_wordcloud():
    oid = request.args.get('oid')
    ctime = request.args.get('ctime')
    last_time = request.args.get('last_time')
    # 删除掉不需要的文件
    file_list = os.listdir('./static/wordclouds')
    for file in file_list:
        if '%s_%s' % (oid, last_time) in file:
            os.remove('./static/wordclouds/' + file)
            break
    # 生成词云
    generate_wordcloud(oid=oid, ctime=ctime)
    return jsonify({'img_url': '../static/wordclouds/%s_%s.jpg' % (oid, ctime)})


if __name__ == '__main__':
    app.run()
