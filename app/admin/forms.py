# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
# 调用验证器
from wtforms.validators import DataRequired, ValidationError
# 登陆表单验证,使用Admin数据模型
from app.models import Admin


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


# -------------------------标签管理----------------------------
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
            "placeholder": "请输入管理员名称！"
        }
    )
    submit = SubmitField(
        label="添加",
        validators=[
            DataRequired("请输入标签!")
        ],
        description='添加',
        render_kw={
            "class": "btn btn-primary"
        }
    )
