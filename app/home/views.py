# coding=utf-8
from . import home
from flask import render_template, redirect, url_for, flash, session, request
from app.home.forms import RegistForm, LoginForm, UserdetailForm, PwdForm
from app.models import User, Userlog, Preview, Tag, Movie

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
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
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
        return redirect(url_for("home.login"))
    return render_template("home/regist.html", form=form)


# --------------------------------------User--------------------------------------
# 用户
@home.route('/user/', methods=["POST", "GET"])
@user_login_req
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
        file_face = secure_filename(form.face.data.filename)
        if not os.path.exists(app.config["FC_DIR"]):
            os.makedirs(app.config["FC_DIR"])
            os.chmod(app.config["FC_DIR"], 'rw')
        user.face = change_filename(file_face)
        form.face.data.save(app.config["FC_DIR"] + user.face)

        # 前提是不能重复
        name_count = User.query.filter_by(name=data["name"]).count()
        if data["name"] != user.name and name_count == 1:
            flash("昵称已经存在", "err")
            return redirect(url_for("home.user"))
        user.name = data["name"]

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
        flash("修改资料成功", "ok")
        return redirect(url_for("home.user"))
    return render_template("home/user.html", form=form, user=user)


# -------------------------------------password-------------------------------------
# 修改密码
@home.route('/pwd/', methods=["GET", "POST"])
@user_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        # 查询admin
        user = User.query.filter_by(name=session['user']).first()
        if not user.check_password(data["old_pwd"]):
            flash("旧密码错误！请重新登录!", "err")
            return redirect(url_for("home.pwd"))
        user.pwd = generate_password_hash(data["new_pwd"])
        db.session.add(user)
        db.session.commit()
        flash("修改密码成功！请重新登录!", "ok")
        return redirect(url_for("home.logout"))
    return render_template("home/pwd.html", form=form)


# -------------------------------comment------------------------------------
# 评论记录
@home.route('/comments/')
@user_login_req
def comments():
    return render_template("home/comments.html")


# ----------------------------------------loginlog------------------------------------------
# 会员登陆日志
@home.route('/loginlog/<int:page>', methods=["GET"])
@user_login_req
def loginlog(page=None):
    if page is None:
        page = 1
    page_data = Userlog.query.filter_by(
        user_id=int(session["user_id"])
    ).join(
        User
    ).order_by(
        Userlog.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("home/loginlog.html", page_data=page_data)


# ---------------------------------------------moviecol------------------------------------------
# 电影收藏
@home.route('/moviecol/')
@user_login_req
def moviecol():
    return render_template("home/moviecol.html")


# 首页对标签进行筛选
@home.route("/<int:page>/",methods=["GET"])
def index(page=None):
    tags = Tag.query.all()
    page_data = Movie.query
    # 标签
    tag_id = request.args.get("tag_id", 0)
    if int(tag_id) != 0:
        page_data = page_data.filter_by(tag_id=int(tag_id))
    # 星际
    star = request.args.get("star", 0)
    if int(star) != 0:
        page_data = page_data.filter_by(star=int(star))
    # 时间
    time = request.args.get("time", 0)
    if int(time) != 0:
        if int(time) == 1:
            # 升序
            page_data = page_data.order_by(
                Movie.addtime.desc()
            )
            # 降序
        else:
            page_data = page_data.order_by(
                Movie.addtime.asc()
            )
    # 播放量
    play_num = request.args.get("play_num", 0)
    if int(play_num) != 0:
        if int(play_num) == 1:
            page_data = page_data.order_by(
                Movie.playnum.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.playnum.asc()
            )
    # 评论量
    comment_num = request.args.get("comment_num", 0)
    if comment_num != 0:
        if int(comment_num) == 1:
            page_data = page_data.order_by(
                Movie.commentum.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.commentum.asc()
            )
    if page is None:
        page=1
    page_data = page_data.paginate(page=page, per_page=10)
    choice = dict(
        tag_id=tag_id,
        star=star,
        time=time,
        play_num=play_num,
        comment_num=comment_num
    )
    return render_template("home/index.html", tags=tags, choice=choice, page_data=page_data)


# 动画:上映预告
@home.route('/animation/')
@user_login_req
def animation():
    data = Preview.query.all()
    return render_template("home/animation.html", data=data)


# 搜索页面
@home.route('/search/')
@user_login_req
def search():
    
    return render_template("home/search.html")


# 电影详情
@home.route('/play/')
@user_login_req
def play():
    return render_template("home/play.html")

# 404页面
# 注意这个页面不是在蓝图的页面进行的,而是初始化文件当中进行的
# @home.errorhandler(404)
# def page_not_found(error):
#     return render_template("home/404.html"), 404
