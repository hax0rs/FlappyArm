from flask import Flask, session, redirect, url_for, escape, request
from flask_socketio import SocketIO
import subprocess
import os
import players
import json

# External test script with absolute path
full_path = os.path.abspath('external_test_script.py')


app = Flask(__name__)
socketio = SocketIO(app)

test_list = []

@app.route("/")
def root():
    return ("<a>go to /play/</a>")

@app.route("/play/")
def play():
    
    os.system("say hello world")
    subprocess.call(full_path)
    return "Hello World!"



@socketio.on('joint_control')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    print ("actual text: " + str(json['data']))



@app.route("/leaderboard/")
def leaderboard():
    return ("<ol><li>UQ hax0rs</li></ol>")



@app.route('/user/')
def index():
    if 'username' in session:
        # return 'Logged in as %s' % escape(session['username'])
        return 'You are controlling joint %s' % escape(session['id'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['id'] = 1
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/in/')
def inchecker():
    users = []
    if session['username']:
        for user in session:
            users.append(session['username'])
        prepped = ','.join(users)
        return (prepped)   
    else:
        return ("no users logged in")
 

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return ("logged out")
    # return redirect(url_for('index'))


@app.route('/clear/')
def clear():
    app.secret_key = os.urandom(32)
    # session.clear()
    # return redirect(url_for('index'))



if __name__ == "__main__":
    app.debug = True
    app.secret_key = 'such_secret_very_secure'
    app.run(host='192.168.0.9')
    socketio.run(app)


