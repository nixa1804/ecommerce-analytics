import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent / "data" / "raw"


def load_orders() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "orders.csv", parse_dates=["created_at"])


def load_order_items() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "order_items.csv")


def load_products() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "products.csv")


def load_categories() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "categories.csv")


def load_users() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "users.csv", parse_dates=["created_at"])


def load_sessions() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "sessions.csv")
