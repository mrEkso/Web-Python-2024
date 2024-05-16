import os

from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg_pool import ConnectionPool
from sqlalchemy import create_engine

from app.models.models import Base

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

# Create a connection pool
conn_pool = ConnectionPool(DATABASE_URL)

engine = create_engine(DATABASE_URL, echo=True)


def create_database():
    connection_params = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "root",
        "host": "localhost"
    }

    import psycopg2
    conn = psycopg2.connect(**connection_params)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = conn.cursor()
    try:
        cursor.execute("CREATE DATABASE financial_exchange")
    except psycopg2.errors.DuplicateDatabase:
        print("Database already exists")
    cursor.close()
    conn.close()


def init_db():
    """Create database tables."""
    create_database()
    Base.metadata.create_all(bind=engine)
