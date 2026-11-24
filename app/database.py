
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, declarative_base


# Load environment variables from the project's .env file
load_dotenv()


# Read database configuration from environment variables
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")


# Ensure all required database settings are available
if not all([POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB]):
    raise RuntimeError("Missing required PostgreSQL environment variables")


# Build the database connection URL safely
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host="postgres",
    port=5432,
    database=POSTGRES_DB,
)


# Create the SQLAlchemy database engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


# Create a factory for database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Base class for SQLAlchemy database models
Base = declarative_base()
# Provide a database session for each API request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()