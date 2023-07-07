from flask import Flask, render_template, redirect, url_for, request
from database import load_stats_from_db, get_stats_from_db, row_to_dict, add_betto_db, add_newuser_to_db, get_users_data
from flask import jsonify

app = Flask(__name__)

Bets = ['india', 'pak', 'sa', 'nz']


@app.route("/")
def hallo():
  RECORDS = load_stats_from_db()
  return render_template('home.html', records=RECORDS, bets=Bets)


@app.route("/wallet")
def wallet():
  return '''
  <html>
  <head>
  helo
  </head>
  </html>
'''


@app.route('/sinin', methods=['POST', 'GET'])
def button_clicked():
  return render_template('login.html')


@app.route('/signinsuccess', methods=['POST', 'GET'])
def success():
  username = request.form['username']
  password = request.form['password']

  user_data = get_users_data(username)

  if password == user_data['password']:
    return redirect('/')
  else:
    return jsonify({'message': 'Failure'})


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
