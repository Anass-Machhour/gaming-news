from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_size=10,          # Number of connections to maintain in the pool
    max_overflow=20,       # Additional connections allowed beyond pool_size
    pool_timeout=30,       # Timeout in seconds for getting a connection
    pool_pre_ping=True     # Automatically test connections before using them
)

#  Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
