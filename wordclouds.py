import jieba
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import sqlite3


def generate_wordcloud(oid, ctime):
    database_path = "./static/comments.db"
    connect = sqlite3.connect(database_path)
    cur = connect.cursor()
    table_name = 'av%s' % oid
    sql = 'select comment_content from %s where ctime<=%s' % (table_name, ctime)
    data = cur.execute(sql)
    text = ''
    for item in data:
        text += item[0]
    cur.close()
    connect.close()

    # 处理显示不出来的表情包的符号
    text = text.replace('[', ' ')
    text = text.replace(']', ' ')
    text = text.replace('_', ' ')
    # 分词
    cut = jieba.cut(text)
    words = ' '.join(cut)

    # 绘制图片
    wc = WordCloud(
        background_color='white',
        font_path='./static/msyh.ttc'
    )
    wc.generate_from_text(words)
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0, 0)
    plt.savefig(r'./static/wordclouds/%s_%s.jpg' % (oid, ctime), dpi=500)
    return
