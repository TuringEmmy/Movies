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