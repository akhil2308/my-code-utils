from sqlalchemy import create_engine
from sqlalchemy.pool import Pool

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# CONFIG (can be moved to .env file)
DB_USER='root'
DB_PASSWORD='root'
DB_HOST='localhost'
DB_PORT=3306
DB_NAME='test'
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10


SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

#  connect_args={"check_same_thread": False}
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_size=DB_POOL_SIZE, max_overflow=DB_MAX_OVERFLOW, pool_recycle=300
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()