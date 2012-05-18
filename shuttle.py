__author__ = 'craig.vyvial'

from flask import Flask
from flask import request
from flask import session
from flask import redirect
from flask import render_template
from flask import url_for
from flask import escape
from flask.ext.sqlalchemy import SQLAlchemy

from datetime import date


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shuttle.db'
db = SQLAlchemy(app)


class Shuttle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(60), nullable=False)

    def __init__(self,capacity,name):
        self.capacity=capacity
        self.name=name

    def __repr__(self):
        return '<Shuttle %r>' % self.name


class ShuttleLeg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    depart_time = db.Column(db.DateTime, nullable=False)
    arrive_time = db.Column(db.DateTime, nullable=False)
    week_day = db.Column(db.Integer, nullable=False)

    shuttle_id = db.Column(db.Integer, db.ForeignKey('shuttle.id'))
    shuttle = db.relationship('Shuttle',
                              backref=db.backref('shuttles', lazy='dynamic'))

    def __init__(self, origin, destination, depart_time, arrive_time, shuttle):
        self.origin=origin
        self.destination=destination
        self.depart_time=depart_time
        self.arrive_time=arrive_time
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
    shuttle_leg = db.relationship('ShuttleLeg',
                                  backref=db.backref('actual_shuttle_legs',
                                                     lazy='dynamic'))
    
    def __init__(self, date, racker_id, status, shuttle_leg):
        self.date = date
        self.racker_id = racker_id
        self.status = status
        self.shuttle_leg = shuttle_leg

@app.route('/checkins/<int:shuttle>', methods=['GET', 'POST'])
def check_ins(shuttle):
    if request.method == 'POST':
        return "(creating checkin with post data) %s - (shuttle) : %s" % (request, shuttle)
    else:
        # get list of checkins for the shuttle given
        shuttle = {'shuttle 1':'test'}
        return render_template('checkin.html', shuttle=shuttle)

@app.route('/shuttle', methods=['GET', 'POST'])
def shuttle():
    if request.method == 'POST':
        capacity = request.form['capacity']
        name = request.form['name']
        shuttle = Shuttle(capacity, name)
        db.session.add(shuttle)
        db.session.commit()
        return redirect(url_for('shuttle'))
    else:
        # get list of shuttles to signup for
        shuttles = Shuttle.query.all()
        return render_template('shuttle.html', shuttles=shuttles)


@app.route('/')
def index():
    if 'username' in session:
        username = escape(session['username'])
        dow_today = date.today().weekday()
        to_san = ShuttleLeg.query.filter_by(week_day=dow_today, destination='Castle').all()
        from_san = ShuttleLeg.query.filter_by(week_day=dow_today, origin='Castle').all()
        return render_template('shuttle.html', username=username, to_san=to_san, from_san=from_san)
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
app.secret_key = '\x0c\xe2\x83*\xe3MK\xf3\x9c\xe9\x16\xf7Bv\xe5\xf2\x17)\x05\x1a2\x91\xcc\xe8'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

