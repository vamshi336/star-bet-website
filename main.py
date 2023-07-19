from flask import Flask, render_template, redirect, url_for, request
from database import load_stats_from_db, get_stats_from_db, row_to_dict, add_betto_db, add_newuser_to_db, get_users_data,get_bal_from_wallet
from flask import jsonify
from flask_login import login_required, LoginManager
from flask_login import login_user
from flask_login import current_user
from flask_login import logout_user
import os
from flask import session

port = int(os.environ.get('PORT', 5000))

app = Flask(__name__)

# Generate a secret key
secret_key = os.urandom(24)
app.secret_key = secret_key


class User:

  def __init__(self, user_id, username, email, password):
    self.user_id = user_id
    self.username = username
    self.email = email
    self.password = password

  def is_authenticated(self):
    return True  # Modify this according to your authentication logic

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    return str(self.user_id)


login_manager = LoginManager()
login_manager.init_app(app



@app.route("/home")
def hallo():
  RECORDS = load_stats_from_db()
  return render_template('home.html',
                         records=RECORDS,
                         username=current_user.username)


@app.route("/wallet")
def wallet():
  balance = get_bal_from_wallet(current_user.username) 
  return render_template("wallet.html", balance=balance)


@app.route('/', methods=['POST', 'GET'])
def button_clicked():
  return render_template('login.html')


@login_manager.user_loader
def load_user(user_id):
  # Load the user from the user_id (username in your case)
  user_data = get_users_data(user_id)
  if user_data:
    return User(user_id, user_data['username'], user_data['email'],
                user_data['password'])
  return None


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
    return redirect(url_for('hallo'))

  else:
    return "Invalid username or password"


@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('hallo'))


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
  app.run(host='0.0.0.0', port=port, debug=True)
