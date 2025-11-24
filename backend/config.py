import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DB_URI = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:ducan06112004@localhost:5432/cinema_db"
)

# Tách ra database name
db_name = DB_URI.rsplit("/", 1)[-1]
db_user_pass_host = DB_URI.split("://")[1].rsplit("/", 1)[0]

# Kết nối tới PostgreSQL (không chỉ định DB, mặc định là 'postgres')
conn = psycopg2.connect(f"postgres://{db_user_pass_host}")
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

# Tạo DB nếu chưa tồn tại
cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
exists = cur.fetchone()
if not exists:
    cur.execute(f'CREATE DATABASE "{db_name}"')
    print(f"Database {db_name} created.")

cur.close()
conn.close()

# ================= Config SQLAlchemy =================
class Config:
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "changeme")
