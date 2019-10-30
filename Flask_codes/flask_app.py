# coding=utf-8
"""
@FileName   :  flask_app.py
@Author     : Chen Wang
@Version    : Python3.X 、Windows or Linux
@Description:
@Time       : 2019/10/29 10:11
@Software   : PyCharm
@Contact    : 1416825008@qq.com
@Blog       : https://github.com/JackMin1314/Python_Study
代 码 仅 限 学 习 ，严 禁 商 业 用 途，转 载 请 注 明 出 处

"""

# import lib

from flask import Flask, request, url_for, render_template, redirect, Response
from flask_cors import CORS
import json

# # 跨域支持,先跨域在路由
# def after_request(resp):
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp
# app.after_request(after_request)
app = Flask(__name__)
CORS(app)

# 再添加路由规则和相应的匹配action
@app.route('/')  # 注意不能函数不能重名
def index_page():
    return "Index Page"


@app.route('/hello/')  # '/hello'跟'/hello/'的区别是使用"/hello"，浏览器访问唯一允许路径http://xxx:x/hello，而http://xxx:x/hello/不允许。
# 路由使用'/hello/'则浏览器/hello,/hello/都允许。因为会自动补全/hello/。用'/hello'可以避免搜索引擎重复索引同一页面
def hello_world():
    return "Hello World Page"


@app.route('/age/<int:my_age>')
def show_age(my_age):
    return "My age is %d" % my_age


'''
转换器类型:
string（缺省值） 接受任何不包含斜杠的文本

int     接受正整数

float   接受正浮点数

path    类似 string ，但可以包含斜杠

uuid    接受 UUID 字符串
'''

# 解决重定向路径
@app.route('/login', methods=['GET', 'POST'])  # Flask 会自动添加 HEAD 方法支持，并且同时还会 按照 HTTP RFC 来处理 HEAD 请求
def login():
    if request.method == 'GET':

        return redirect('/login/')

    else:
        return redirect('/login/')

# 该action返回json格式，需要显示的设置content-type(浏览器header可以看到)认为是object-object,不然会认为是text类型，导致用户页面解析出错
@app.route('/flask_json/<username>')
def flask_json(username):
    login_name = username
    dicts = {"message": "ok", "username": login_name}
    return Response(json.dumps(dicts), mimetype='application/json')

# 返回用户请求登录的login.html页面,login_name是/login/后面的内容例如ZYM.html
@app.route('/login/<string:login_name>')
def login_return(login_name):
    # 渲染的模板。这类包含固定内容和动态部分的可重用文件称为模板（template）。
    if login_name:
        login_name = login_name[:-5]    # 去掉.html
        # Flask框架(本质上是采用jinja2模板引擎)会自动从templates文件夹找模板(login.html),并根据特殊语法标记出的变量，对页面动态修改
        return render_template('login.html', title=login_name)
    else:
        return render_template('login.html', title="")


with app.test_request_context():  # 反转函数url_for(),用于自由构建指定函数的url
    print(url_for('index_page'))
    print(url_for('hello_world'))
    # print(url_for('flask_json'))
    print(url_for('show_age', my_age=10))
    # print(url_for('login'))

# main函数，程序开始执行的位置(当本程序是主程序的时候)
if __name__ == "__main__":
    app.run(host="localhost", port=5050, debug=True)  # debug设置为True时候，程序运行时修改了代码，会自动restart
