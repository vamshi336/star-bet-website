from flask import Flask, render_template
from database import load_stats_from_db

app = Flask(__name__)
RECORDS = [{
  'player': 'kholi',
  'runs': 200,
  'mtches': 240
}, {
  'player': 'rohith',
  'runs': 400,
  'mtches': 240
}]
Bets = ['india', 'pak', 'sa', 'nz']


@app.route("/")
def hallo():
  RECORDS = load_stats_from_db()
  return render_template('home.html', records=RECORDS, bets=Bets)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
