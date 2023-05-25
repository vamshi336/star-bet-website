from sqlalchemy import create_engine, text

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
connection_string = "mysql+pymysql://9tclv14q8087m4kxhp3d:pscale_pw_6mnUhgP1s7Npsxfd8D7ROYa75tLWMXXlVnFVCtipLO2@aws.connect.psdb.cloud/starbetting?charset=utf8mb4"

engine = create_engine(connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})


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
