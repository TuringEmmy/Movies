# coding=utf-8
from . import home
from flask import render_template,redirect,url_for

# 主页
@home.route("/")
def index():
    # return "<h1 style='color:green'>This is home</h1>"
    return render_template("home/index.html")

# 登陆
@home.route("/login/")
def login():
    return render_template("home/login.html")
# 退出
@home.route("/logout/")
def logout():
    return redirect(url_for("home.login"))