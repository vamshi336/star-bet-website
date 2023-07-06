from flask import Flask, render_template, redirect, url_for, request
from database import load_stats_from_db, get_stats_from_db, row_to_dict, add_betto_db
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
  return render_template('sinin.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
  return render_template("login.html")


@app.route('/sinup', methods=['POST', 'GET'])
def sinup():
  # Handle button click logic here
  return render_template('sinup.html')


@app.route('/sinup/s', methods=['POST'])
def signup():
  # Retrieve form data
  username = request.form['username']
  email = request.form['email']
  password = request.form['password']

  # Create a cursor object to execute queries
  cursor = db.cursor()

  # Execute the query to insert user data into the database
  query = "INSERT INTO Users (username, email, password) VALUES (%s, %s, %s)"
  values = (username, email, password)
  cursor.execute(query, values)

  # Commit the changes to the database
  db.commit()

  # Close the cursor
  cursor.close()

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
