import urllib.parse

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

with open("/run/secrets/db-password", "r") as f:
    mysqlpass = f.readline().strip()
encoded_password = urllib.parse.quote(mysqlpass)
Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(256))
    password = Column(String(256))


engine = create_engine(f"mysql+pymysql://root:{encoded_password}@mysqlhost/flaskapp")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
