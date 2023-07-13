from flask import Flask, render_template, redirect, url_for, request
from database import load_stats_from_db, get_stats_from_db, row_to_dict, add_betto_db, add_newuser_to_db, get_users_data
from flask import jsonify
from flask_login import login_required, LoginManager
from flask_login import login_user

app = Flask(__name__)

import os

app = Flask(__name__)

# Generate a secret key
secret_key = os.urandom(24)
app.secret_key = secret_key


class User:

  def __init__(self, user_id, username, email, password):
    self.id = user_id
    self.username = username
    self.email = email
    self.password = password

  def get_id(self):
    return str(self.id)

  def is_active(self):
    return True  # Replace with your own logic to determine if the user account is active or not


login_manager = LoginManager()
login_manager.init_app(app)

Bets = ['india', 'pak', 'sa', 'nz']

# Rest of your code...

# Rest of your code...

# Rest of your code...


@app.route("/")
def hallo():
  RECORDS = load_stats_from_db()
  return render_template('home.html', records=RECORDS, bets=Bets)


@app.route("/wallet")
@login_required
def wallet():
  return '''
  <html>
  <head>
  helo your wallet balance is $500.
  </head>
  </html>
'''


@app.route('/sinin', methods=['POST', 'GET'])
def button_clicked():
  return render_template('login.html')


@login_manager.user_loader
@app.route('/signinsuccess', methods=['POST', 'GET'])
def success():
  username = request.form['username']
  password = request.form['password']

  user_data = get_users_data(username)

  if user_data and password == user_data['password']:
    user_id = username  # Use the username as the user ID
    user = User(user_id, user_data['username'], user_data['email'],
                user_data['password'])
    login_user(user)
    return render_template('home.html')
  else:
    return "Invalid username or password"


@app.route('/signup/s', methods=['POST', 'GET'])
def signup():
  return render_template("signup.html")


@app.route('/signup', methods=['POST'])
def signups():
  # Retrieve form data
  username = request.form['username']
  email = request.form['email']
  password = request.form['password']
  add_newuser_to_db(username, email, password)
  return "Registration successful!"


@app.route("/admin/<int:id>")
def show_stats(id):
  job = get_stats_from_db(id)
  if job is None:
    return "Job not found", 404
  else:
    job_dict = row_to_dict(job)  # Convert Row object to dictionary
    return render_template("admin.html", job_dict=job_dict)


@app.route('/admin/<int:id>/apply', methods=['POST'])
def apply_to_jobs(id):
  data = request.form.to_dict()
  total_data_of_player = get_stats_from_db(id)
  player_name = total_data_of_player[1]
  r = total_data_of_player[5]
  amount = data.get('amount')  # Extract the 'amount' value from the dictionary
  add_betto_db(amount, player_name,
               r)  # Pass the 'amount' value as an argument
  return render_template('betplaced.html', DATA=data)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
