import random
import string
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    # Validate the form input
    if request.form['username'] != 'admin' or request.form['password'] != 'admin':
      error = 'Invalid credentials'
    else:
      # Login successful, set a session variable
      session['logged_in'] = True
      return redirect(url_for('admin'))
  return render_template('login.html', error=error)

@app.route('/admin')
def admin():
  if not session.get('logged_in'):
    return redirect(url_for('login'))
  return 'Welcome to the admin panel!'

@app.route('/user/<user_id>')
def user(user_id):
  # Retrieve the user's information from the database
  user = User.query.get(user_id)
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

if __name__ == '__main__':
  app.run()

