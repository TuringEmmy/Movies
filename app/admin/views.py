# coding=utf-8
from . import admin
from flask import render_template, redirect, url_for, flash, session, request
# flash用于登录页面错误返回
# 登陆正确就要,进行sessiond的保存
# 处理登陆
from app.admin.forms import LoginForm, TagForm, MovieForm, PreviewForm
from app.models import Admin, Tag, Movie, Preview, User, Comment, Moviecol
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


# --------------------------------------电影模块--------------------------
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
            commentnum=0,
            tag_id=int(data["tag_id"]),
            area=data["area"],
            release_time=data["release_time"],
            length=data["length"],
        )
        db.session.add(movie)
        db.session.commit()
        flash("添加电影成功！", "ok")
        return redirect(url_for("admin.movie_add"))
    return render_template("admin/movie_add.html", form=form)


# 电影列表
@admin.route('/movie/list/<int:page>', methods=["GET"])
@admin_login_req
def movie_list(page=None):
    if page is None:
        page = 1
    # join(Tag)这个是关联标签
    # filter_by是单表查询
    # filter是多表关联
    page_data = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id
    ).order_by(
        Movie.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/movie_list.html", page_data=page_data)


# 删除电影
@admin.route('/movie/del/<int:id>', methods=["GET"])
@admin_login_req
def movie_del(id=None):
    # 获取电影的id
    movie = Movie.query.get_or_404(int(id))
    db.session.delete(movie)
    db.session.commit()
    # 注意：电影删除后，相关的评论要消失
    # 闪现，提示删除成功
    flash("删除电影成功", "ok")
    return redirect(url_for("admin.movie_list", page=1))


# 编辑修改电影
@admin.route('/movie/edit/<int:id>', methods=["POST", "GET"])
@admin_login_req
def movie_edit(id=None):
    form = MovieForm()
    # 这个是编辑的，所以url和logo肯定有的，所以不用查询
    form.url.validators = []
    form.logo.validators = []
    movie = Movie.query.get_or_404(int(id))
    # 编写验证逻辑

    if request.method == "GET":
        form.info.data = movie.info
        form.tag_id.data = movie.tag_id
        form.star.data = movie.star
    if form.validate_on_submit():
        data = form.data
        # 注意Movie，是大写的
        movie_count = Movie.query.filter_by(title=data["title"]).count()
        if movie_count == 1 and movie.title != data["title"]:
            flash("片名已经存在！", "err")
            return redirect(url_for("admin.movie_edit", id=id))

        if not os.path.exists(app.config["UP_DIR"]):
            # 创建文件目录
            os.makedirs(app.config["UP_DIR"])
            # 增加读写的权限
            os.chmod(app.config["UP_DIR"], "rw")
            # --------------url
        if form.url.data.filename != "":  # 不为空，说明更改过了图片
            file_url = secure_filename(form.url.data.filename)
            movie.url = change_filename(file_url)
            form.url.data.save(app.config["UP_DIR"] + movie.url)

            # --------------logo
        if form.logo.data.filename != "":  # 不为空，说明更改过了logo
            file_logo = secure_filename(form.logo.data.filename)
            movie.logo = change_filename(file_logo)
            form.logo.data.save(app.config["UP_DIR"] + movie.logo)

        movie.star = data["star"]
        movie.tag_id = data["tag_id"]
        movie.info = data["info"]
        movie.title = data["title"]
        movie.area = data["area"]
        movie.length = data["length"]
        movie.release_time = data["release_time"]
        db.session.add(movie)
        db.session.commit()
        flash("修改电影成功！", "ok")
        return redirect(url_for("admin.movie_edit", id=id))
    return render_template("admin/movie_edit.html", form=form, movie=movie)


# -------------------------------Preview-------------------------------------
# 预告添加
@admin.route('/preview/add/', methods=["GET", "POST"])
@admin_login_req
def preview_add():
    # 实例化form表单
    form = PreviewForm()
    if form.validate_on_submit():
        data = form.data
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")
        logo = change_filename(file_logo)
        form.logo.data.save(app.config["UP_DIR"] + logo)
        preview = Preview(
            title=data["title"],
            logo=logo
        )
        # 保存数据
        db.session.add(preview)
        db.session.commit()
        flash("添加预告成功", "ok")
        return redirect(url_for("admin.preview_add"))
    return render_template("admin/preview_add.html", form=form)


# 预告列表
@admin.route('/preview/list/<int:page>/', methods=["PPOST", "GET"])
@admin_login_req
def preview_list(page=None):
    if page is None:
        page = 1
    page_data = Preview.query.order_by(
        Preview.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/preview_list.html", page_data=page_data)


# 预告列表<delete Button>
@admin.route('/preview/del/<int:id>/', methods=["PPOST", "GET"])
@admin_login_req
def preview_del(id=None):
    preview = Preview.query.get_or_404(int(id))
    db.session.delete(preview)
    db.session.commit()
    flash("删除预告成功", "ok")
    return redirect(url_for("admin.preview_list", page=1))


# 预告列表<修改>
@admin.route('/preview/edit/<int:id>', methods=["GET", "POST"])
@admin_login_req
def preview_edit(id):
    # 实例化form表单
    form = PreviewForm()
    form.logo.validators = []
    preview = Preview.query.get_or_404(int(id))
    if request.method == "GET":
        form.title.data = preview.title
    if form.validate_on_submit():
        data = form.data

        # -----logo
        if form.logo.data.filename != "":  # 不为空，说明更改过了logo
            file_logo = secure_filename(form.logo.data.filename)
            preview.logo = change_filename(file_logo)
            form.logo.data.save(app.config["UP_DIR"] + preview.logo)
        # -------logo

        preview.title = data["title"]
        db.session.add(preview)
        db.session.commit()
        flash("修改预告成功", "ok")
        return redirect(url_for("admin.preview_edit", id=id))
    return render_template("admin/preview_edit.html", form=form, preview=preview)


# -----------------------------------User---------------------------------------
# 会员列表
@admin.route('/user/list/<int:page>', methods=["GET"])
@admin_login_req
def user_list(page=None):
    if page is None:
        page = 1
    page_data = User.query.order_by(
        User.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/user_list.html", page_data=page_data)


# 查看会员
@admin.route('/user/view/<int:id>', methods=["GET"])
@admin_login_req
def user_view(id=None):
    user = User.query.get_or_404(int(id))
    return render_template("admin/user_view.html", user=user)


# 用户列表<delete Button>
@admin.route('/user/del/<int:id>/', methods=["GET"])
@admin_login_req
def user_del(id=None):
    user = User.query.get_or_404(int(id))
    db.session.delete(user)
    db.session.commit()
    flash("删除会员成功", "ok")
    return redirect(url_for("admin.user_list", page=1))


# ----------------------------------Comment--------------------------------------------
# 电影评论
@admin.route('/comment/list/<int:page>/', methods=["GET"])
@admin_login_req
def comment_list(page=None):
    if page is None:
        page = 1
    page_data = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Comment.movie_id,
        User.id == Comment.user_id
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/comment_list.html", page_data=page_data)


# 评论列表<delete Button>
@admin.route('/comment/del/<int:id>/', methods=["GET"])
@admin_login_req
def comment_del(id=None):
    comment = Comment.query.get_or_404(int(id))
    db.session.delete(comment)
    db.session.commit()
    flash("删除评论成功", "ok")
    return redirect(url_for("admin.comment_list", page=1))


# 电影收藏
@admin.route('/moviecol/list/<int:page>/', methods=["GET"])
@admin_login_req
@admin_login_req
def moviecol_list(page=None):
    if page is None:
        page = 1
    page_data = Moviecol.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Moviecol.movie_id,
        User.id == Moviecol.user_id
    ).order_by(
        Moviecol.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/moviecol_list.html", page_data=page_data)



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
