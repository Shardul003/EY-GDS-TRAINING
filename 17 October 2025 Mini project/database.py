from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Correctly encoded password
DATABASE_URL = "mysql+pymysql://root:The%40lphs987@localhost/COURSES_MANAGEMENT"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()