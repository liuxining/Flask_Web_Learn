from . import auth
from ..models import User
from .forms import LoginForm,RegisterForm
from .. import db
from ..mail import send_mail
from flask import current_app
from flask import render_template,redirect,request,url_for,flash
from flask.ext.login import login_user,logout_user,login_required
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask.ext.login import current_user

@auth.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(mail=form.mail.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you hava bean logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register',methods=['POST','GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        u = User(username=form.username.data,mail=form.mail.data,password=form.password.data)
        db.session.add(u)
        db.session.commit()
        token = u.general_confirmation_tolen()
        send_mail(form.mail.data,'confirm','auth/mail/confirm',user=u,token=token)

        flash('激活邮件已发送到{mail}',form.mail.data)
        return redirect(url_for('main.index'))
    return render_template('auth/register.html',form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect('main.index')
    if current_user.confirm(token):
        flash('激活成功！')
    else:
        flash('激活失败！')
    return redirect('main.index')
