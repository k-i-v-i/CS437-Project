import random
import string
from MySQLdb import connect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask import Flask, render_template, request, session, redirect, url_for
import mysqlx

app = Flask(__name__)


#db_connection = connect(
  #     host='localhost',
   #    user='root',
    #   password='',
     #  database='users'
    #)
USERID = 3

app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'users'
  
mysql = MySQL(app)

@app.route('/', methods =['GET', 'POST'])
def login():
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
            return render_template('user.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'
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

@app.route('/admin')
def admin():
  if not session.get('logged_in'):
    return redirect(url_for('login'))
  return 'Welcome to the admin panel!'

@app.route('/user/<user_id>')
def user(user_id):
  # Retrieve the user's information from the database
  cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
  cursor.execute('SELECT * FROM user WHERE userid = %s ', (user_id,  ))
  user = cursor.fetchone()
  #user = User.query.get(user_id)
  return render_template('user.html', user=user)

@app.route('/recover_password', methods=['GET', 'POST'])
def recover_password():
  error = None
  if request.method == 'POST':
    # Validate the form input
    if '@' not in request.form['email']:
      error = 'Invalid email address'
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
            userid = USERID+1
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

