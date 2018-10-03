# coding=utf-8
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:mysql@127.0.0.1:3306/movies"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = "turingemmmytyuringemmy"

app.debug = True
db = SQLAlchemy(app)

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")


# 对应蓝图的文件,不能放到蓝图里面,因为这个要程序一执行就得运行,时刻见识有可能出售错的文件
# 同时home修改未app
@app.errorhandler(404)
def page_not_found(error):
    return render_template("home/404.html"), 404
