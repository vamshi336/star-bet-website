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
  
@login_manager.user_loader
def load_user(user_id):
    user_data = get_users_data(user_id)
    if user_data:
        # Create a User object using the retrieved data from the database
        user = User(user_data['id'], user_data['username'], user_data['email'], user_data['password'])
        return user
    else:
        return None



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


def add_betto_db(amount, player_name, r):
  query = "INSERT INTO bettable (amount, P_name,ratio) VALUES (:b_amount, :p_name,:b_ratio)"
  with engine.connect() as conn:
    conn.execute(
      text(query).params(b_amount=amount, p_name=player_name, b_ratio=r))


def add_newuser_to_db(username, email, password):
  query = "INSERT INTO Users (Username, Email, Password) VALUES (:b_username, :b_email, :b_password)"
  with engine.connect() as conn:
    conn.execute(
      text(query).params(b_username=username,
                         b_email=email,
                         b_password=password))


def add_newuser_to_db(username, email, password):
  query = "insert into Users(Username,Email,Password) VALUES(:b_username,:b_email,:b_password)"
  with engine.connect() as conn:
    conn.execute(
      text(query).params(b_username=username,
                         b_email=email,
                         b_password=password))


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


def load_user(user_id):
  # Implement the logic to load the user object based on user_id
  # Return the user object associated with the user_id
  return User.query.get(int(user_id))  # Replace with your own implementation
