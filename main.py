from flask import Flask, render_template, redirect, url_for
from database import load_stats_from_db

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
  # Handle button click logic here
  return render_template('sinin.html')


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


@app.route('/admin')
def gobackhome():
  return redirect(url_for("hallo"))


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
