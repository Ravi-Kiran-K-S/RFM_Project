import os
import urllib.parse
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

# Get database credentials from environment or Docker secrets
try:
    with open("/run/secrets/db-password", "r") as f:
        mysqlpass = f.readline().strip()
except FileNotFoundError:
    # Fallback to environment variable if Docker secrets not available
    mysqlpass = os.getenv("MYSQL_PASSWORD")
    if not mysqlpass:
        raise ValueError("MYSQL_PASSWORD environment variable or Docker secret is not set.")

# Get other database config from environment
mysql_user = os.getenv("MYSQL_USER", "root")
mysql_host = os.getenv("MYSQL_HOST", "mysqlhost")
mysql_database = os.getenv("MYSQL_DATABASE", "flaskapp")
mysql_port = os.getenv("MYSQL_PORT", "3306")

encoded_password = urllib.parse.quote(mysqlpass)

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(256))
    password = Column(String(256))


engine = create_engine(
    f"mysql+pymysql://{mysql_user}:{encoded_password}@{mysql_host}:{mysql_port}/{mysql_database}",
    pool_pre_ping=True,  # Check connection before use
    pool_recycle=3600,   # Recycle connections after 1 hour
)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
