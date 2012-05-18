__author__ = 'craig.vyvial'


from flask import Flask
from flask import request
from flask import session
from flask import redirect
from flask import render_template
from flask import url_for
from flask import escape


app = Flask(__name__)


@app.route('/checkins', methods=['GET', 'POST'])
def check_ins():
    pass


@app.route('/shuttle', methods=['GET', 'POST'])
def shuttle():
    if request.method == 'POST':
        return "(posting data) %s" % request
    else:
#        return "GET all the shuttles [list]"
        return url_for('static', filename='bootstrap.min.css')


@app.route('/')
def index():
    if 'username' in session:
        username = escape(session['username'])
        return render_template('shuttle.html', username=username)
#        return redirect(url_for('static', filename='shuttle.html'))
#        return 'Logged in as %s' % escape(session['username'])
#    return 'You are not logged in'
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

