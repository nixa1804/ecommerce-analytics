import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = Path(__file__).parent.parent.parent / "data" / "raw"
DATABASE_URL = os.getenv("DATABASE_URL")


def _engine():
    from sqlalchemy import create_engine
    return create_engine(DATABASE_URL)


def load_orders() -> pd.DataFrame:
    if DATABASE_URL:
        return pd.read_sql("SELECT * FROM orders", _engine(), parse_dates=["created_at"])
    return pd.read_csv(DATA_DIR / "orders.csv", parse_dates=["created_at"])


def load_order_items() -> pd.DataFrame:
    if DATABASE_URL:
        return pd.read_sql("SELECT * FROM order_items", _engine())
    return pd.read_csv(DATA_DIR / "order_items.csv")


def load_products() -> pd.DataFrame:
    if DATABASE_URL:
        return pd.read_sql("SELECT * FROM products", _engine())
    return pd.read_csv(DATA_DIR / "products.csv")


def load_categories() -> pd.DataFrame:
    if DATABASE_URL:
        return pd.read_sql("SELECT * FROM categories", _engine())
    return pd.read_csv(DATA_DIR / "categories.csv")


def load_users() -> pd.DataFrame:
    if DATABASE_URL:
        return pd.read_sql("SELECT * FROM users", _engine(), parse_dates=["created_at"])
    return pd.read_csv(DATA_DIR / "users.csv", parse_dates=["created_at"])


def load_sessions() -> pd.DataFrame:
    if DATABASE_URL:
        return pd.read_sql("SELECT * FROM sessions", _engine())
    return pd.read_csv(DATA_DIR / "sessions.csv")
