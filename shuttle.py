__author__ = 'craig.vyvial'
from flask import Flask
from flask import request
from flask import session
from flask import redirect
from flask import render_template
from flask import url_for
from flask import escape
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////shuttle.db'
db = SQLAlchemy(app)

class Shuttle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(60), nullable=False)

    def __init__(self,cpacity,name):
        self.capacity=capacity
        self.name=name

    def __repr__(self):
        return '<Shuttle %r>' % self.name

class ShuttleLeg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    departtime = db.Column(db.DateTime, nullable=False) 
    arrivetime = db.Column(db.DateTime, nullable=False)

    shuttle_id = db.Column(db.Integer, db.ForeignKey('shuttle.id'))
    shuttle = db.relationship('Shuttle', backref=db.backref('shuttles', lazy='dynamic'))

    def __init__(self,origin,destination,departtime,arrivetime, shuttle):
        self.origin=origin
        self.destination=destination
        self.departtime=departtime
        self.arrivetime=arrivetime
        self.shuttle=shuttle

class Racker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    
    def __init__(self,name,phone):
        self.name=name
        self.phone=phone

class ActualShuttleLeg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    racker_id = db.Column(db.Integer, db.ForeignKey('racker.id'))
    status = db.Column(db.String(20))

    shuttle_leg_id = db.Column(db.Integer, db.ForeignKey('shuttle_leg.id'))
    shuttle_leg = db.relationship('ShuttleLeg', backref=db.backref('actual_shuttle_legs', lazy='dynamic'))
    
    def __init__(self, date, racker_id, status, shuttle_leg):
        self.date = date
        self.racker_id = racker_id
        self.status = status
        self.shuttle_leg = shuttle_leg


@app.route('/checkins', methods=['GET', 'POST'])
def check_ins():
    pass

@app.route('/shuttle', methods=['GET', 'POST'])
def shuttle():
    if request.method == 'POST':
        return "(posting data) %s" % request
    else:
        return url_for('static', filename='bootstrap.min.css')


@app.route('/')
def index():
    if 'username' in session:
        username = escape(session['username'])
        return render_template('shuttle.html', username=username)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "admin" and password == "admin":
            session['username'] = username
            session['password'] = password
        return redirect(url_for('index'))
    return redirect(url_for('static', filename='login.html'))

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

