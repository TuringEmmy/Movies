# coding=utf-8
# 入口文件

from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, FileField, TextAreaField
# 导入验证的工具
from wtforms.validators import DataRequired, EqualTo, Email, Regexp, ValidationError
# 确保字段的唯一性
from app.models import User


# -------------------------------------------Register---------------------------------
class RegistForm(FlaskForm):
    name = StringField(
        label='昵称',
        validators=[
            # 验证账号不能为空
            DataRequired("请输入昵称")
        ],
        description='昵称',
        # 附加选项
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入昵称!",
        }
    )
    # 邮箱部分
    email = StringField(
        label='邮箱',
        validators=[
            # 验证账号不能为空
            DataRequired("请输入邮箱")
        ],
        description='邮箱',
        # 附加选项
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入邮箱!",
        }
    )
    # 定义手机号码
    phone = StringField(
        label='手机号码',
        validators=[
            # 验证账号不能为空
            DataRequired("请输入手机号码"),
            Regexp("1[3458]\\d{9}", message="手机号码格式不正确")
        ],
        description='手机号码',
        # 附加选项
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入手机号码!",
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
            "class": "form-control input-lg",
            "placeholder": "请输入密码!",
        }
    )
    reppwd = PasswordField(
        label="确认密码",
        validators=[
            DataRequired("请确认密码"),
            EqualTo('pwd', message="两次密码输入不同")
        ],
        description="确认密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请确认密码!",
        }
    )
    # 登陆按钮
    submit = SubmitField(
        "注册",
        render_kw={
            "class": "btn btn-lg btn-success btn-block",
        }
    )

    # 定义字段的唯一性
    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user == 1:
            raise ValidationError("昵称已经存在！")

    def validate_email(self, field):
        email = field.data
        user = User.query.filter_by(email=email).count()
        if user == 1:
            raise ValidationError("邮箱已经存在！")

    def validate_phone(self, field):
        phone = field.data
        user = User.query.filter_by(phone=phone).count()
        if user == 1:
            raise ValidationError("电话已经存在！")


class LoginForm(FlaskForm):
    name = StringField(
        label='账号',
        validators=[
            # 验证账号不能为空
            DataRequired("请输入账号")
        ],
        description='账号',
        # 附加选项
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入账号!",
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码")
        ],
        description="密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入密码!",
        }
    )
    submit = SubmitField(
        "登陆",
        render_kw={
            "class": "btn btn-lg btn-success btn-block",
        }
    )


# -------------------------------User------------------------------------------
class UserdetailForm(FlaskForm):
    name = StringField(
        label='昵称',
        validators=[
            # 验证账号不能为空
            DataRequired("请输入昵称")
        ],
        description='昵称',
        # 附加选项
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入昵称!",
        }
    )
    email = StringField(
        label='邮箱',
        validators=[
            # 验证账号不能为空
            DataRequired("请输入邮箱")
        ],
        description='邮箱',
        # 附加选项
        render_kw={
            "class": "form-control",
            "placeholder": "请输入邮箱!",
        }
    )
    # 定义手机号码
    phone = StringField(
        label='手机号码',
        validators=[
            # 验证账号不能为空
            DataRequired("请输入手机号码"),
            Regexp("1[3458]\\d{9}", message="手机号码格式不正确")
        ],
        description='手机号码',
        # 附加选项
        render_kw={
            "class": "form-control",
            "placeholder": "请输入手机号码!",
        }
    )
    face = FileField(
        label="头像",
        validators=[
            DataRequired("请上传图像")
        ],
        description="头像"
    )
    info = TextAreaField(
        label="简介",
        validators=[
            DataRequired("请输入简介！")
        ],
        description="简介",
        render_kw={
            "class": "form-control",
            "rows": 10
        }
    )
    submit = SubmitField(
        '保存修改',
        render_kw={
            "class": "btn btn-succes"
        }

    )
# ---------------------------------Password----------------------------------------
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
        "修改修改",
        render_kw={
            "class": "btn btn-succes",
        }
    )

# ----------------------------------------------CommentForm-------------------------------