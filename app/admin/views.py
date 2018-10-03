# coding=utf-8
from . import admin
from flask import render_template, redirect, url_for, flash, session, request
# flash用于登录页面错误返回
# 登陆正确就要,进行sessiond的保存
# 处理登陆
from app.admin.forms import LoginForm
from app.models import Admin
# 登陆的装饰器
from functools import wraps


# 登陆装饰器
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session["admin"] in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


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
            flash("密码错误!",'err')
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
@admin.route('/tag/add/')
@admin_login_req
def tag_add():
    return render_template("admin/tag_add.html")


# 标签列表页面
@admin.route('/tag/list/')
@admin_login_req
def tag_list():
    return render_template("admin/tag_list.html")


# 添加电影
@admin.route('/movie/add/')
@admin_login_req
def movie_add():
    return render_template("admin/movie_add.html")


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
