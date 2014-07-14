from flask import Flask
from flask import render_template, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, IntegerField, validators

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
import models

@app.route('/')
@app.route('/index')
def index():
    users = models.User.query.all()
    users.sort(key=lambda x: x.time, reverse=False)
    return render_template('index.html', users = users)

class SubmitForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=64)])
    min = IntegerField('Minutes')
    sec = IntegerField('Seconds')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = SubmitForm(request.form)
    if request.method == 'POST' and form.validate():
        seconds = (int(form.min.data))*60 + int(form.sec.data)
        user=models.User.query.filter_by(name=form.name.data).first()
        if user == None:
            user = models.User(name=form.name.data,min=int(form.min.data),sec=int(form.sec.data),time=seconds)
            db.session.add(user)
            db.session.commit()
        elif user.time >= seconds:
            task = db.session.query(models.User).get(form.name.data)
            task.min = form.min.data
            task.sec = form.sec.data
            task.time = seconds
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('submit.html', form=form)

class DeleteForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=64)])

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    form = DeleteForm(request.form)
    if request.method == 'POST' and form.validate():
        user=models.User.query.filter_by(name=form.name.data).first()
        if user != None:
            task = db.session.query(models.User).get(form.name.data)
            db.session.delete(task)
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('delete.html', form=form)

if __name__ == '__main__':
    app.run()