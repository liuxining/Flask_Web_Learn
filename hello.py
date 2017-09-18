#2017年09月17日13:09:56
#liuxining

import os
from flask import Flask,render_template
from flask import request
from flask import session
from flask import redirect,url_for,flash
from flask import make_response
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime

from flask.ext.wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

#数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'lalala po jie bu le ba'
#邮件服务器配置
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

app.config['FLASK_MAIL_SUBJECT_PREFIX'] = '[Flask]'
app.config['FLASK_MAIL_SENDER'] = os.environ.get('MAIL_USERNAME')
app.config['FLASK_ADMIN'] = os.environ.get('FLASK_ADMIN')


bootstrap = Bootstrap(app)
moment = Moment(app)
manager = Manager(app)

db = SQLAlchemy(app)


from flask.ext.script import Shell

def make_shell_context():
    return dict(app = app,db = db,User = User,Role = Role)

manager.add_command("shell",Shell(make_context=make_shell_context))

from flask.ext.migrate import Migrate,MigrateCommand

migrate = Migrate(app,db)

manager.add_command('db',MigrateCommand)

from flask.ext.mail import Mail,Message

mail = Mail(app)

from threading import Thread

def send_async_mail(app,msg):
    with app.app_context():
        mail.send(msg)

#发送邮件
def send_mail(to,subject,template,**kwargs):
    print('to={to},subject={subject},templat={template}'.format(to=to,subject=subject,template=template))
    msg = Message(app.config.get('FLASK_MAIL_SUBJECT_PREFIX') + subject,sender=app.config.get('FLASK_MAIL_SENDER'),recipients=[to])
    msg.body = render_template(template + '.txt',**kwargs)
    msg.html = render_template(template + '.html',**kwargs)
    print(msg.body)
    print(msg.html)
    th = Thread(target=send_async_mail,args=[app,msg])
    th.start()
    return th




class NameForm(Form):
    name = StringField('What is your name?',validators=[Required()])
    submit = SubmitField('Submit')

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User',backref='role',lazy='dynamic')


    def __repr__(self):
        return '<Role %s>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))



    def __repr__(self):
        return '<User %s>' % self.username




@app.route('/',methods=['POST','GET'])
def index():
    print('进入index')
    print('admin : ' + app.config['FLASK_ADMIN'])
    name = None
    form = NameForm()
    if form.validate_on_submit():
        print('username = ' + form.name.data)

        user = User.query.filter_by(username = form.name.data).first()

        if user is None:
            print('user is None')
            session['known'] = False
            user = User(username=form.name.data)
            db.session.add(user)
            if app.config['FLASK_ADMIN']:

                print('send mail')

                send_mail(app.config['FLASK_ADMIN'],'NEW USER','mail/new_user',user=user)
            else:
                print('no send mail')

        else:
            print('user is not none')
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        redirect(url_for('index'))
    return render_template('index.html',form=form,name=session.get('name')\
                           ,known = session.get('known',False))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

@app.errorhandler(404)
def page_not_find(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

if __name__ == "__main__":
    # app.run(debug=True)
    manager.run()