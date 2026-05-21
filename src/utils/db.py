import os
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()


def get_db_url() -> str:
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "sales_dwh")
    user = os.getenv("POSTGRES_USER", "dwh_user")
    password = os.getenv("POSTGRES_PASSWORD", "dwh_password")

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


def get_engine():
    return create_engine(get_db_url())