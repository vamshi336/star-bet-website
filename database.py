from sqlalchemy import create_engine, text

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
import os

my_secret = os.environ['DB_CONNECTION_STRING']

engine = create_engine(my_secret,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def get_bal_from_wallet(username):
  with engine.connect() as conn:
    query = text("SELECT balance FROM Users WHERE Username=:val")
    result = conn.execute(query, {'val': username})
    row = result.fetchone()
    if row is not None:
      balance = row[0]  # Access the balance column of the retrieved row
      return balance
    else:
      return None  # Return None if the user is not found or balance is not available


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


def add_betto_db(username, amount, player_name, r):
  query = "INSERT INTO bettable (username,amount, P_name,ratio) VALUES (:u_name,:b_amount, :p_name,:b_ratio)"
  with engine.connect() as conn:
    conn.execute(
      text(query).params(u_name=username,
                         b_amount=amount,
                         p_name=player_name,
                         b_ratio=r))


def add_newuser_to_db(username, email, password):
  query = "INSERT INTO Users (Username, Email, Password) VALUES (:b_username, :b_email, :b_password)"
  with engine.connect() as conn:
    conn.execute(
      text(query).params(b_username=username,
                         b_email=email,
                         b_password=password))


def add_new_user_to_db(username, email, password):
  query = "INSERT INTO Users (Username, Email, Password) VALUES (:b_username, :b_email, :b_password)"
  with engine.connect() as conn:
    result = conn.execute(
      text(query).params(b_username=username,
                         b_email=email,
                         b_password=password))
    user_id = result.lastrowid

    # Update the inserted row with the generated user_id
    update_query = "UPDATE Users SET user_id = :b_user_id WHERE ID = :b_id"
    conn.execute(text(update_query).params(b_user_id=user_id, b_id=user_id))

    return user_id


def get_users_data(username):
  with engine.connect() as conn:
    query = text(
      "SELECT username, email, password FROM Users WHERE username=:val")
    result = conn.execute(query, {"val": username})
    row = result.fetchone()

  if row is not None:
    username = row[0]
    email = row[1]
    password = row[2]
    return {'username': username, 'email': email, 'password': password}

  return None


def user_bets(username):
  print("Username:", username)
  with engine.connect() as conn:
    query = text('select * from bettable where username=:val')
    result = conn.execute(query, {'val': username})
    row = result.fetchone()
    print("Query Result:", row)  # Check the query result
  return row
