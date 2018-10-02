# coding=utf-8
from . import admin
from flask import render_template,redirect,url_for


@admin.route("/")
def index():
    return "<h1 style='color:red'>This is admin</h1>"

# 管理员登录页面
@admin.route('/login/')
def login():
    return render_template("admin/login.html")

# 管理员退出页面
@admin.route('/logout/')
def logout():
    return redirect(url_for('admin.login'))