# coding=utf-8
from . import home
from flask import render_template, redirect, url_for, flash, session, request
from app.home.forms import RegistForm, LoginForm, UserdetailForm
from app.models import User, Userlog

# 导入密码加密的工具
from werkzeug.security import generate_password_hash
# 引入安全的名称,用于用户页面的头像
from werkzeug.utils import secure_filename
from app import db, app
# uuid的使用
import uuid
import os
import datetime
# 进行登陆的装饰器
from functools import wraps


# 登陆装饰器
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("home.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 修改文件名称
def change_filename(filename):
    fileinfo=os.path.splitext(filename)
    filename=datetime.datetime.now().strftime("%Y%m%d%H%M%S")+str(uuid.uuid4().hex)+fileinfo[-1]
    return filename

# # 主页
# @home.route("/")
# def index():
#     # return "<h1 style='color:green'>This is home</h1>"
#     return render_template("home/index.html")


# 登陆
@home.route("/login/", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data["name"]).first()
        if not user.check_password(data["pwd"]):
            flash("密码错误！", "err")
            return redirect(url_for("home.login"))
        # 如果正确，就启动session机制,还要使用UserLog
        session["user"] = user.name
        session["user_id"] = user.id
        # 处理完毕之后一定要记得处理登陆日志
        userlog = Userlog(
            user_id=user.id,
            ip=request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        # 登陆成功之后，进行跳转
        return redirect(url_for("home.user"))
    return render_template("home/login.html", form=form)


# 退出
@home.route("/logout/")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
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
@home.route('/user/', methods=["POST", "GET"])
def user():
    form = UserdetailForm()
    # user是为了，修改用户信息的原始值
    user = User.query.get(int(session["user_id"]))
    form.face.validators = []
    if request.method == "GET":
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data
        file_face=secure_filename(form.face.data.filename)
        if not os.path.exists(app.config["FC_DIR"]):
            os.makedirs(app.config["FC_DIR"])
            os.chmod(app.config["FC_DIR"],'rw')
        user.face=change_filename(file_face)
        form.face.data.save(app.config["FC_DIR"]+user.face)

        # 前提是不能重复
        name_count=User.query.filter_by(name=data["name"]).count()
        if data["name"]!=user.name and name_count==1:
            flash("昵称已经存在","err")
            return redirect(url_for("home.user"))
        user.name=data["name"]

        email_count = User.query.filter_by(email=data["email"]).count()
        if data["email"] != user.email and email_count == 1:
            flash("邮箱已经存在", "err")
            return redirect(url_for("home.user"))
        user.email = data["email"]

        phone_count = User.query.filter_by(phone=data["phone"]).count()
        if data["phone"] != user.phone and phone_count == 1:
            flash("电话已经存在", "err")
            return redirect(url_for("home.user"))
        user.phone = data["phone"]

        user.info = data["info"]
        db.session.add(user)
        db.session.commit()
        flash("修改资料成功","ok")
        return redirect(url_for("home.user"))
    return render_template("home/user.html", form=form, user=user)


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
