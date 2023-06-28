from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLACHEMY_DATABASE_URL = 'postgres://postgresql_nkap_user:BP3opO8zdrhc90R1Wlf2vwfiEVRO7ZQA@dpg-cidur7h5rnukltljcieg-a.singapore-postgres.render.com/postgresql_nkap'

engine = create_engine(SQLACHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
