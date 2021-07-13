from flask import Flask, render_template, request
from crawler import *

app = Flask(__name__)


# 首页
@app.route('/')
def index():
    return render_template("index.html")


# 爬取数据，并显示
@app.route('/process')
def process():
    # 将bv号转化为对应的av号的后缀
    bv = request.args.get("bv")
    oid = BvToAv(bv)

    # 爬取评论数据并将数据储存在数据库
    crawl(oid)

    # 从数据库中查询需要的数据

    return "Hello"


if __name__ == '__main__':
    app.run()
