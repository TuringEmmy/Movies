from datetime import datetime
from app import db


# 会员
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(11), unique=True)
    info = db.Column(db.Text)  # 个性简介
    face = db.Column(db.String(255), unique=True)  # 头像
    # 注册时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    uuid = db.Column(db.String(255), unique=True)  # 唯一标识符

    # 会员日志外交按关联
    userlogs = db.relationship("Userlog", backref='user')
    # 评论外键关联
    comments = db.relationship("Comment", backref="user")

    moviecols = db.relationship("Moviecol", backref='user')

    def __repr__(self):
        return "<User %r >" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 会员登陆日志
class Userlog(db.Model):
    __tablename__ = "userlog"
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 所属编号
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # 登陆ip的字段
    ip = db.Column(db.String(100))
    # 登陆时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Userlog %r>" % self.id


# 标签
class Tag(db.Model):
    __tablename__ = "tag"
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 标签
    name = db.Column(db.String(100), unique=True)
    # 添加时间按
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    # 电影外检的关联
    movies = db.relationship("Movie", backref="tag")

    def __repr__(self):
        return "<Tag %r>" % self.name


# 电影
class Movie(db.Model):
    __tablename__ = "movie"
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 标题
    title = db.Column(db.String(255), unique=True)
    # 地址
    url = db.Column(db.String(255), unique=True)
    # 简介
    info = db.Column(db.String(255), unique=True)
    # 封面
    logo = db.Column(db.Text)
    # 星际
    star = db.Column(db.SmallInteger)
    # 播放量
    playnum = db.Column(db.BigInteger)
    # 评论量
    commentum = db.Column(db.BigInteger)
    # 所属标签
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"))
    # 上映地区
    area = db.Column(db.String(255))
    # 上映时间
    release_time = db.Column(db.Date)
    # 播放量
    length = db.Column(db.String(100))
    # 添加时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # 评论外键关联
    conmments = db.relationship("Comment", backref="movie")

    # 收藏外交按关联
    moviecols = db.relationship("Moviecol", backref="movie")

    def __repr__(self):
        return "< Movie %r>" % self.title


# 上映预告
class Preview(db.Model):
    __tablename__ = "preview"
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 标题
    title = db.Column(db.String(255), unique=True)
    # 地址
    url = db.Column(db.String(255), unique=True)
    # 封面
    logo = db.Column(db.Text)
    # 添加时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "< Preview %r>" % self.title


# 评论
class Comment(db.Model):
    __tablename__ = "comment"
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # [评论的内容]
    content = db.Column(db.Text)
    # 所属的电影
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    # 所属的用户
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # 添加时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Comment %r>" % self.id


# 收藏
class Moviecol(db.Model):
    __tablename__ = "moviecol"
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # [评论的内容]
    content = db.Column(db.Text)
    # 所属的电影
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    # 所属的用户
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # 添加时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Moviecol %r>" % self.id


# 权限
class Auth(db.Model):
    __tablename__ = "auth"
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 标题
    title = db.Column(db.String(255), unique=True)
    # 地址
    url = db.Column(db.String(255), unique=True)
    # 添加时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Auth %r>" % self.name


# 角色
class Role(db.Model):
    __tablename__ = "role"
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 名称
    name = db.Column(db.String(100), unique=True)
    # 添加时间
    auths = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    # 管理员外键关系管理链
    admins = db.relationship("Admin", backref="role")

    def __repr__(self):
        return "Role %r" % self.name


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    # 是否为超级管理，0表示超级管理员
    is_super = db.Column(db.SmallInteger)
    # 所属角色
    role_id = db.Column(db.ForeignKey("role.id"))
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # 管理员登陆日志外键关联
    adminlogs = db.relationship("Adminlog", backref="admin")
    # 管理员操作体质外键关联
    oplogs = db.relationship("Oplog", backref="admin")

    def __repr__(self):
        return "<Admin %r" % self.name

    # 验证密码啊正确返回True,错误返回False
    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        # print(self.pwd, pwd)
        return check_password_hash(self.pwd, pwd)


# 管理员登陆日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 所属编号
    admin_id = db.Column(db.ForeignKey("admin.id"))
    # 登陆ip的字段
    ip = db.Column(db.String(100))
    # 登陆时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Adminlog %r>" % self.id


# 操作日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 所属编号
    admin_id = db.Column(db.ForeignKey("admin.id"))
    # 登陆ip的字段
    ip = db.Column(db.String(100))
    # 登陆时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    # 操作的原因
    reason = db.Column(db.String(600))

    def __repr__(self):
        return "<Oplog %r>" % self.id


# if __name__ == '__main__':
    # db.create_all()
    #
    # role = Role(
    #     name="admin",
    #     auths=""
    # )
    # db.session.add(role)
    # db.session.commit()
    # from werkzeug.security import generate_password_hash
    #
    # admin = Admin(
    #     name="turing",
    #     pwd=generate_password_hash("turingemmy"),
    #     is_super=0,
    #     role_id=1
    # )
    # db.session.add(admin)
    # db.session.commit()
