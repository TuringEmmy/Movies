# coding=utf-8
from flask_wtf import FlaskForm
# FileField用于电影管理的url,TextAreaField文本框,星际选择SelectField
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, SelectMultipleField
# 调用验证器
from wtforms.validators import DataRequired, ValidationError
# 登陆表单验证,使用Admin数据模型
from app.models import Admin, Tag, Preview

tags = Tag.query.all()


# -----------------------------loginManager----------------------------
class LoginForm(FlaskForm):
    """管理员登陆表单"""
    account = StringField(
        label='账号',
        validators=[
            # 验证账号不能为空
            DataRequired("请输入账号")
        ],
        description='账号',
        # 附加选项
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号!",
            # "required": "required"     # 这是htm5的,我这里使用了自定义的,代码下方
        }

    )
    # 定义密码框
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码!",
            # "required": "required"
        }
    )
    # 登陆按钮
    submit = SubmitField(
        "登陆",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
    )

    # 自定义表单验证器
    def validata_account(self, field):
        account = field.data
        # 查询出来需要进行统计
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError("账号不存在!")


# -----------------------------tagManager------------------------------
class TagForm(FlaskForm):
    name = StringField(
        label="名称",
        validators=[
            DataRequired("请输入标签!")
        ],
        description='标签',
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入标签名称！"
        }
    )
    submit = SubmitField(
        label="编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )


# -----------------------------movieManager----------------------------
class MovieForm(FlaskForm):
    title = StringField(
        label="片名",
        validators=[
            DataRequired("请输入片名!")
        ],
        description='片名',
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "placeholder": "请输入片名！"
        }
    )
    url = FileField(
        label="文件",
        validators=[
            DataRequired("请上传文件！")
        ],
        description="文件",
    )
    info = TextAreaField(
        label="简介",
        validators=[
            DataRequired("请输入简介!")
        ],
        description='片名',
        render_kw={
            "class": "form-control",
            "row": 10
        }
    )
    logo = FileField(
        label="封面",
        validators=[
            DataRequired("请上传封面！")
        ],
        description="封面",
    )
    star = SelectField(
        label="星级",
        validators=[
            DataRequired("请选择星级！")
        ],
        # 下面两个，第一个设置类型，第二个列举选择框内容，用列表
        coerce=int,
        choices=[(1, '1星'), (2, '2星'), (3, '3星'), (4, '4星'), (5, '5星')],
        description="星级",
        render_kw={
            "class": "form-control",
        }
    )
    tag_id = SelectField(
        label="标签",
        validators=[
            DataRequired("请选择星级！")
        ],
        # 下面两个，第一个设置类型，第二个列举选择框内容，用列表
        coerce=int,
        choices=[(v.id, v.name) for v in tags],
        description="星级",
        render_kw={
            "class": "form-control",
        }
    )
    area = StringField(
        label="地区",
        validators=[
            DataRequired("请输入地区!")
        ],
        description='地区',
        render_kw={
            "class": "form-control",
            "placeholder": "请输入地区！"
        }
    )
    length = StringField(
        label="片长",
        validators=[
            DataRequired("请输入片长!")
        ],
        description='片长',
        render_kw={
            "class": "form-control",
            "placeholder": "请输入片长！"
        }
    )
    release_time = StringField(
        label="上映时间",
        validators=[
            DataRequired("请选择上映时间!")
        ],
        description='上映时间',
        render_kw={
            "class": "form-control",
            "placeholder": "请选择上映时间！",
            "id": "input_release_time"
        }
    )
    submit = SubmitField(
        label="提交",
        render_kw={
            "class": "btn btn-primary"
        }
    )


# -----------------------------Preview---------------------------
class PreviewForm(FlaskForm):
    title = StringField(
        label="预告标题",
        validators=[
            DataRequired("请输入预告标题!")
        ],
        description='片名',
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "placeholder": "请输入预告标题！"
        }
    )
    logo = FileField(
        label="预告封面",
        validators=[
            DataRequired("请上传封面！")
        ],
        description="预告封面",
    )
    submit = SubmitField(
        label="添加",
        render_kw={
            "class": "btn btn-primary"
        }
    )


# -----------------------------PssswordModify--------------------------
class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label="旧密码",
        validators=[
            DataRequired("请输入旧密码")
        ],
        description="旧密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入旧密码!",
        }
    )
    new_pwd = PasswordField(
        label="新密码",
        validators=[
            DataRequired("请输入新密码")
        ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入新密码!",
        }
    )
    submit = SubmitField(
        "确认修改",
        render_kw={
            "class": "btn btn-primary",
        }
    )

    def validata_old_pwd(self, field):
        # 获取密码
        from flask import session
        pwd = field.data
        # 获取管理员
        name = session["admin"]
        admin = Admin.query.filter_by(
            name=name
        ).first()
        if not admin.check_pwd(pwd):
            raise ValidationError("旧密码错误！")


# -------------------------------AuthForm--------------------------------
class AuthForm(FlaskForm):
    name = StringField(
        label="权限名称",
        validators=[
            DataRequired("请输入权限名称!")
        ],
        description='权限名称',
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入权限名称！"
        }
    )
    url = StringField(
        label="权限地址",
        validators=[
            DataRequired("请输入权限地址！")
        ],
        description="权限地址",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入权限地址！"
        }
    )
    submit = SubmitField(
        "编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )


# ---------------------------------RoleForm---------------------------------
class RoleForm(FlaskForm):
    name = StringField(
        label="角色名称",
        validators=[
            DataRequired("请输入角色名称!")
        ],
        description='角色名称',
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入角色名称！"
        }
    )
    auths = SelectMultipleField(
        label="权限列表",
        validators=[
            DataRequired("请选择权限列表")
        ],
        description="权限列表",
        render_kw={
            "class": "form-control"
        },
        submit=SubmitField(
            "编辑",
            render_kw={
                "class": "btn btn-primary"
            }
        )
    )
