from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Define the MySQL connection URL
# Format: mysql+pymysql://user:password@host:port/database_name
SQL_ALCHEMY_DATABASE_URL = "mysql+pymysql://root:Ajay73729@localhost:3306/hyaup"

# 2. Create the engine
engine = create_engine(SQL_ALCHEMY_DATABASE_URL, pool_pre_ping=True)

# 3. Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create the Base class for all database models
Base = declarative_base()

# 5. Dependency injection function to get a DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()