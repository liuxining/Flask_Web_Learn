from threading import Thread
from . import mail
from flask.ext.mail import Message
from flask import render_template,current_app

def send_async_mail(app,msg):
    with app.app_context():
        mail.send(msg)

#发送邮件
def send_mail(to,subject,template,**kwargs):
    app = current_app._get_current_object()
    print('to={to},subject={subject},templat={template}'.format(to=to,subject=subject,template=template))
    msg = Message(app.config.get('FLASK_MAIL_SUBJECT_PREFIX') + subject,sender=app.config.get('FLASK_MAIL_SENDER'),recipients=[to])
    msg.body = render_template(template + '.txt',**kwargs)
    msg.html = render_template(template + '.html',**kwargs)
    print(msg.body)
    print(msg.html)
    th = Thread(target=send_async_mail,args=[app,msg])
    th.start()
    return th


