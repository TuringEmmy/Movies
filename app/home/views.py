# coding=utf-8
from . import home
from flask import render_template

@home.route("/")
def index():
    # return "<h1 style='color:green'>This is home</h1>"
    return render_template("home/index.html")