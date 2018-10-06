# coding=utf-8
from . import home
from flask import render_template, redirect, url_for, flash
from app.home.forms import RegistForm
from app.models import User

# 导入密码加密的工具
from werkzeug.security import generate_password_hash
from app import db
# uuid的使用
import uuid


# # 主页
# @home.route("/")
# def index():
#     # return "<h1 style='color:green'>This is home</h1>"
#     return render_template("home/index.html")


# 登陆
@home.route("/login/")
def login():
    return render_template("home/login.html")


# 退出
@home.route("/logout/")
def logout():
    return redirect(url_for("home.login"))


# 会员注册
@home.route('/regist/', methods=["POST", "GET"])
def regist():
    form = RegistForm()
    # 获取前段数据
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            pwd=generate_password_hash(data["pwd"]),
            uuid=uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功", "ok")
    return render_template("home/regist.html", form=form)


# 用户
@home.route('/user/')
def user():
    return render_template("home/user.html")


# 修改密码
@home.route('/pwd/')
def pwd():
    return render_template("home/pwd.html")


# 评论记录
@home.route('/comments/')
def comments():
    return render_template("home/comments.html")


# 登陆日志
@home.route('/loginlog/')
def loginlog():
    return render_template("home/loginlog.html")


# 电影收藏
@home.route('/moviecol/')
def moviecol():
    return render_template("home/moviecol.html")


# 列表
@home.route("/")
def index():
    # return "<h1 style='color:green'>This is home</h1>"
    return render_template("home/index.html")


# 动画
@home.route('/animation/')
def animation():
    return render_template("home/animation.html")


# 搜索页面
@home.route('/search/')
def search():
    return render_template("home/search.html")


# 电影详情
@home.route('/play/')
def play():
    return render_template("home/play.html")

# 404页面
# 注意这个页面不是在蓝图的页面进行的,而是初始化文件当中进行的
# @home.errorhandler(404)
# def page_not_found(error):
#     return render_template("home/404.html"), 404
