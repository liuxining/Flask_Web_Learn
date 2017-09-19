from datetime import datetime
from flask import render_template,url_for,session,redirect

from . import main
from .forms import NameForm
from .. import db
from ..models import User

@main.route('/',methods=['POST','GET'])
def index():
    print('进入index')
    #print('admin : ' + app.config['FLASK_ADMIN'])
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

        else:
            print('user is not none')
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        redirect(url_for('.index'))
    return render_template('index.html',form=form,name=session.get('name')\
                           ,known = session.get('known',False),current_time=datetime.utcnow())
