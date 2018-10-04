# coding=utf-8
from . import admin
from flask import render_template, redirect, url_for, flash, session, request
# flash用于登录页面错误返回
# 登陆正确就要,进行sessiond的保存
# 处理登陆
from app.admin.forms import LoginForm, TagForm, MovieForm
from app.models import Admin, Tag, Movie
# 登陆的装饰器
from functools import wraps
from app import db, app
# 确保修改文件名称的安全可靠
from werkzeug.utils import secure_filename

import os
import uuid
import datetime


# 登陆装饰器
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 修改文件名称
def change_filename(filename):
    # 将文件名filename进行分割
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[
        -1]  # fileinfo[-1]代表后缀
    return filename


@admin.route("/")
@admin_login_req
def index():
    return render_template("admin/index.html")


# 管理员登录页面
@admin.route('/login/', methods=["GET", "POST"])
def login():
    # 实例化登陆表单
    form = LoginForm()
    # 对form表单进行验证处理
    if form.validate_on_submit():
        # 验证有值后进行获取值
        data = form.data
        admin = Admin.query.filter_by(name=data["account"]).first()
        # print(admin.check_pwd(data["pwd"]))
        if not admin.check_pwd(data["pwd"]):
            # 闪现
            flash("密码错误!", 'err')
            # 密码错误的时候,重定向到lohin页面
            return redirect(url_for("admin.login"))
        session["admin"] = data["account"]
        return redirect(request.args.get("next") or url_for("admin.index"))
    return render_template("admin/login.html", form=form)


# 管理员退出页面
@admin.route('/logout/')
@admin_login_req
def logout():
    # 退出是删除账号
    session.pop("admin", None)
    return redirect(url_for('admin.login'))


# 修改密码页面
@admin.route('/pwd/')
@admin_login_req
def pwd():
    return render_template("admin/pwd.html")


# 标签添加页面
@admin.route('/tag/add/', methods=["GET", "POST"])
@admin_login_req
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        # 获取数据
        data = form.data
        tag = Tag.query.filter_by(name=data["name"]).count()
        if tag == 1:
            flash("名称已经存在了!", "err")
            return redirect(url_for("admin.tag_add"))
        # 存入数据库
        tag = Tag(
            name=data["name"]
        )
        db.session.add(tag)
        db.session.commit()
        # 入库成功之后,出现信息
        flash("添加成功", "ok")
        # 添加成功之后,依然跳转到标签添加的页面
        redirect(url_for("admin.tag_add"))
    return render_template("admin/tag_add.html", form=form)


# 标签列表页面;<int:page>为路由规则,传入整形,分页用到
@admin.route('/tag/list/<int:page>', methods=["GET"])
@admin_login_req
def tag_list(page=None):
    # 查询,分页,显示
    if page is None:
        page = 1
    # 按照时间添加顺序进行添加
    page_data = Tag.query.order_by(
        Tag.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/tag_list.html", page_data=page_data)


# 标签删除;<int:page>为路由规则,传入整形,分页用到
@admin.route('/tag/del/<int:id>', methods=["GET", "POST"])
@admin_login_req
def tag_del(id=None):
    # 根据逐渐 进行南宁查询
    # tage = Tag.query.get(id)
    # 下面的方法啊插叙un错误字段，可以直接跳转到404页面
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    # 消息闪现
    flash("删除标签成功", 'ok')
    # 注意：一定要假return，否则会报错，说没有response
    return redirect(url_for("admin.tag_list", page=1))


# 编辑标签
@admin.route('/tag/edit/<int:id>', methods=["GET", "POST"])
@admin_login_req
def tag_edit(id=None):
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        # 获取数据
        data = form.data
        tag_count = Tag.query.filter_by(name=data["name"]).count()
        if tag.name != data["name"] and tag_count == 1:
            flash("标签已经存在了!", "err")
            # 这行代码要传入id，害的我调试了一下午
            return redirect(url_for("admin.tag_edit", id=id))
        # 直接修改即可
        tag.name = data["name"]

        db.session.add(tag)
        db.session.commit()
        # 入库成功之后,出现信息
        flash("修改标签成功", "ok")
        # 添加成功之后,依然跳转到标签添加的页面
        redirect(url_for("admin.tag_edit", id=id))
    return render_template("admin/tag_edit.html", form=form, tag=tag)


# 添加电影
@admin.route('/movie/add/', methods=["POST", "GET"])
@admin_login_req
def movie_add():
    form = MovieForm()
    # 编写验证逻辑
    if form.validate_on_submit():
        # 获取前端表单数据
        data = form.data
        file_url = secure_filename(form.url.data.filename)
        # fiel_logo=form.logo.data.filename
        # 包裹之后，安全
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config["UP_DIR"]):
            # 创建文件目录
            os.makedirs(app.config["UP_DIR"])
            # 增加读写的权限
            os.chmod(app.config["UP_DIR"], "rw")
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        # 然后进行保存操作
        form.url.data.save(app.config["UP_DIR"] + url)
        form.logo.data.save(app.config["UP_DIR"] + logo)

        movie = Movie(
            title=data['title'],
            # 文件上传保存路径
            url=url,  # 在init文件里面设设置
            info=data['info'],
            logo=logo,
            star=int(data["star"]),
            playnum=0,
            commentum=0,
            tag_id=int(data["tag_id"]),
            area=data["area"],
            release_time=data["release_time"],
            length=data["length"],
        )
        db.session.add(movie)
        db.session.commit()
        flash("添加电影成功！", "ok")
        return redirect("admin.movie_add")
    return render_template("admin/movie_add.html", form=form)


# 电影列表
@admin.route('/movie/list/')
@admin_login_req
@admin_login_req
def movie_list():
    return render_template("admin/movie_list.html")


# 预告添加
@admin.route('/preview/add/')
@admin_login_req
def preview_add():
    return render_template("admin/preview_add.html")


# 预告列表
@admin.route('/preview/list/')
@admin_login_req
def preview_list():
    return render_template("admin/preview_list.html")


# 会员列表
@admin.route('/user/list/')
@admin_login_req
def user_list():
    return render_template("admin/user_list.html")


# 查看会员
@admin.route('/user/view/')
@admin_login_req
def user_view():
    return render_template("admin/user_view.html")


# 电影评论
@admin.route('/comment/list/')
@admin_login_req
@admin_login_req
def comment_list():
    return render_template("admin/coment_list.html")


# 电影收藏
@admin.route('/moviecol/list/')
@admin_login_req
@admin_login_req
def moviecol_list():
    return render_template("admin/moviecol_list.html")


# 操作日志
@admin.route('/oplog/list/')
@admin_login_req
def oplog_list():
    return render_template("admin/oplog_list.html")


# 管理员登陆日至
@admin.route('/adminloginlog/list/')
@admin_login_req
def adminloginlog_list():
    return render_template("admin/adminloginlog_list.html")


# 会员员登陆日至
@admin.route('/userloginlog/list/')
@admin_login_req
def userloginlog_list():
    return render_template("admin/userloginlog_list.html")


# 角色添加
@admin.route('/role/add/')
@admin_login_req
def role_add():
    return render_template("admin/role_add.html")


# 角色列表
@admin.route('/role/list/')
@admin_login_req
def role_list():
    return render_template("admin/role_list.html")


# 权限添加
@admin.route('/auth/add/')
@admin_login_req
def auth_add():
    return render_template("admin/auth_add.html")


# 权限列表
@admin.route('/auth/list/')
def auth_list():
    return render_template("admin/auth_list.html")


# 权限添加
@admin.route('/admin/add/')
@admin_login_req
def admin_add():
    return render_template("admin/admin_add.html")


# 权限列表
@admin.route('/admin/list/')
@admin_login_req
def admin_list():
    return render_template("admin/admin_list.html")
