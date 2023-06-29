from sqlalchemy import create_engine, text

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
import os

my_secret = os.environ['DB_CONNECTION_STRING']

engine = create_engine(my_secret,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})
with engine.connect() as conn:
  result = conn.execute(text("select * from stats"))
  xyz = result.all()
  print(xyz)


def load_stats_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from stats"))
    xyz = result.all()
    stats = []
    for row in xyz:
      row_as_dict = row._mapping
      z = dict(row_as_dict)
      stats.append(z)
    return stats


def row_to_dict(row):
  return dict(row._asdict())


def get_stats_from_db(id=None):
  with engine.connect() as conn:
    query = text("select * from stats where id=:val")
    result = conn.execute(query, {"val": id})
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      return rows[0]


def add_betto_db(amount):
  query = "INSERT INTO bettable (amount) VALUES (:b_amount)"
  with engine.connect() as conn:
    conn.execute(text(query).params(b_amount=amount))
