# coding=utf-8
from . import admin
from flask import render_template,redirect,url_for


@admin.route("/")
def index():
    return render_template("admin/index.html")

# 管理员登录页面
@admin.route('/login/')
def login():
    return render_template("admin/login.html")

# 管理员退出页面
@admin.route('/logout/')
def logout():
    return redirect(url_for('admin.login'))

# 修改密码页面
@admin.route('/pwd/')
def pwd():
    return render_template("admin/pwd.html")


# 标签添加页面
@admin.route('/tag/add')
def tag_add():
    return render_template("admin/tag_add.html")

# 标签列表页面
@admin.route('/tag/list')
def tag_list():
    return render_template("admin/tag_list.html")

# 添加电影
@admin.route('/movie/add')
def movie_add():
    return render_template("admin/movie_add.html")

# 电影列表
@admin.route('/movie/list')
def movie_list():
    return render_template("admin/movie_list.html")

# 预告添加
@admin.route('/preview/add')
def preview_add():
    return render_template("admin/preview_add.html")

# 预告列表
@admin.route('/preview/list')
def preview_list():
    return render_template("admin/preview_list.html")


# 会员列表
@admin.route('/user/list')
def user_list():
    return render_template("admin/user_list.html")

# 查看会员
@admin.route('/user/view')
def user_view():
    return render_template("admin/user_view.html")

