from flask.ext.wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo,ValidationError

from ..models import User

class LoginForm(Form):
    mail = StringField('Mail',validators=[Required(),Length(1,64),Email()])
    password = PasswordField('Password',validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('log in')


class RegisterForm(Form):
    mail = StringField("Mail",validators=[Required(),Length(1,64),Email()])
    username = StringField("Username",validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'用户名格式错误')])
    password = PasswordField('password',validators=[Required(),EqualTo('password2',message='密码不一致')])
    password2 = PasswordField('confirm password',validators=[Required()])
    submit = SubmitField('Register')

    def validate_mail(self,field):
        if User.query.filter_by(mail=field.data).first():
            raise ValidationError('邮箱已被注册')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被使用')


