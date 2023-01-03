import random
import string
from MySQLdb import connect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask import Flask, render_template, request, session, redirect, url_for
import mysqlx
from logging.config import dictConfig
from flask import has_request_context, request, logging
from flask.logging import default_handler
import requests
from datetime import datetime

app = Flask(__name__)

NO_ATTEMPT = 0

def get_location(ip_address):
    
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data['country']

#app.logger.removeHandler(default_handler)
'''
handler = dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s %(name)s %(threadName)s : %(message)s',
    }},
    'handlers': {"console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "logs.log",
                "formatter": "default",
            }},
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file']
    }
    
})


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
            record.country = get_location(request.remote_addr)
            #record.attempt = classify_attempt(request.form)
            
        else:
            record.url = None
            record.remote_addr = None
            record.country = None

        return super().format(record)

formatter = RequestFormatter(
    '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
    '%(levelname)s in %(module)s from %(country) : %(message)s'
)
handler.setFormatter(formatter)

#db_connection = connect(
  #     host='localhost',
   #    user='root',
    #   password='',
     #  database='users'
    #)
'''
app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'denizi'
app.config['MYSQL_DB'] = 'users'
  
mysql = MySQL(app)

@app.route('/', methods =['GET', 'POST'])
def login():
    global NO_ATTEMPT
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        #print(password)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #cursor = db_connection.cursor()
        #print(cursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        #print(user)
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'
            
            time = datetime.now

            ip = request.remote_addr
            country = get_location(request.remote_addr)
            attempt = 'login'
            status = 'successful'           
            
            if NO_ATTEMPT > 30:
              verdict = 'Malicious Brute-Force'
            else:
              verdict = 'Benign Successful'
            cursor.execute('SELECT COUNT(*) FROM logs')
            logid = cursor.fetchone()
            logid = logid['COUNT(*)']
            #print(userid)
            #userid = int(userid)
            NO_ATTEMPT = 0
            logid = logid + 1
            print((logid, time, ip, country, attempt, status, verdict ))
            cursor.execute('INSERT INTO logs (logid, timestamp, ip, country, attempt, status, verdict) VALUES (%s, % s, % s, % s, %s, %s, %s)', (logid, time, ip, country, attempt, status, verdict ))
            mysql.connection.commit()
            return render_template('user.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'
            time = datetime.now
            ip = request.remote_addr
            country = get_location(request.remote_addr)
            attempt = 'login'
            status = 'not successful'
            
            NO_ATTEMPT += 1
            if NO_ATTEMPT > 30:
              verdict = 'Malicious Brute-Force'
            else:
              verdict = 'Benign Failed'
            cursor.execute('SELECT COUNT(*) FROM logs')
            logid = cursor.fetchone()
            logid = logid['COUNT(*)']
            #print(userid)
            #userid = int(userid)
            logid = logid + 1
            cursor.execute('INSERT INTO logs (logid, timestamp, ip, country, attempt, status, verdict) VALUES (%s, % s, % s, % s, %s, %s, %s)', (logid, time, ip, country, attempt, status, verdict ))
            mysql.connection.commit()
            #app.logger.info('Not successful login attempt')
    return render_template('login.html', mesage = mesage)

#@app.route('/', methods=['GET', 'POST'])
#def login():
 # error = None
  #if request.method == 'POST':
    # Validate the form input
   # if request.form['username'] != 'admin' or request.form['password'] != 'admin':
    #  error = 'Invalid credentials'
    #else:
      # Login successful, set a session variable
     # session['logged_in'] = True
      #return redirect(url_for('admin'))
  #return render_template('login.html', error=error)
'''
@app.route('/admin')
def admin():
  if not session.get('logged_in'):
    return redirect(url_for('login'))
  return 'Welcome to the admin panel!'
'''
@app.route('/user/<user_id>')
def user(user_id):
  # Retrieve the user's information from the database
  cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
  if user_id == 1:
    entries = []
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # Retrieve the log entries from a database or file
    entries = 'SELECT * FROM logs'
    return render_template('log.html',entries=entries)
  else:
    cursor.execute('SELECT * FROM user WHERE userid = %s ', (user_id,  ))
    user = cursor.fetchone()
    #user = User.query.get(user_id)
    return render_template('user.html', user=user)

  

@app.route('/recover_password', methods=['GET', 'POST'])
def recover_password():
  global NO_ATTEMPT
  error = None
  cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
  if request.method == 'POST':
    # Validate the form input
    if '@' not in request.form['email']:
      error = 'Invalid email address'
      #app.logger.info('Not successful email attempt')
    elif request.form['code']== temp_password:
      email = request.form['email']
      cursor.execute('SELECT * FROM user WHERE email = % s ', (email ))
      user = cursor.fetchone()
      time = datetime.now
      ip = request.remote_addr
      country = get_location(request.remote_addr)
      attempt = 'password'
      status = 'successful'
           
      if NO_ATTEMPT > 30:
        verdict = 'Malicious Brute-Force'
      else:
        verdict = 'Benign Failed'
      cursor.execute('SELECT COUNT(*) FROM logs')
      logid = cursor.fetchone()
      logid = logid['COUNT(*)']
            #print(userid)
            #userid = int(userid)
      logid = logid + 1
      cursor.execute('INSERT INTO logs (logid, timestamp, ip, country, attempt, status, verdict) VALUES (%s, % s, % s, % s, %s, %s, %s)', (logid, time, ip, country, attempt, status, verdict ))
      return render_template('user.html', user)
    elif request.form['code']!= temp_password:
      time = datetime.now
      ip = request.remote_addr
      country = get_location(request.remote_addr)
      attempt = 'login'
      status = 'not successful'
      
      NO_ATTEMPT += 1
      if NO_ATTEMPT > 30:
        verdict = 'Malicious Brute-Force'
      else:
        verdict = 'Benign Failed'
      cursor.execute('SELECT COUNT(*) FROM logs')
      logid = cursor.fetchone()
      logid = logid['COUNT(*)']
            #print(userid)
            #userid = int(userid)
      logid = logid + 1
      
      cursor.execute('INSERT INTO logs (logid, timestamp, ip, country, attempt, status, verdict) VALUES (%s, % s, % s, % s, %s, %s, %s)', (logid, time, ip, country, attempt, status, verdict ))
      mysql.connection.commit()
    else:
      # Generate a temporary password
      temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
      # Send the temporary password to the user's email
      #send_email(request.form['email'], temp_password)
      return 'A temporary password has been sent to your email.'
  return render_template('recover_password.html', error=error)





  

@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('SELECT COUNT(*) FROM user')
            userid = cursor.fetchone()
            userid = userid['COUNT(*)']
            #print(userid)
            #userid = int(userid)
            userid = userid + 1
            cursor.execute('INSERT INTO user VALUES (%s, % s, % s, % s)', (userid, userName, email, password, ))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage = mesage)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
  app.run()

