import random
import pandas as pd
import numpy as np
from faker import Faker
from pathlib import Path

fake = Faker()
random.seed(42)
np.random.seed(42)

OUTPUT_DIR = Path(__file__).parent / "raw"
OUTPUT_DIR.mkdir(exist_ok=True)

# --- Categories ---
CATEGORIES = [
    "Electronics", "Clothing", "Home & Kitchen", "Sports & Outdoors",
    "Beauty & Health", "Books", "Toys & Games", "Automotive"
]

categories = pd.DataFrame({
    "id": range(1, len(CATEGORIES) + 1),
    "name": CATEGORIES
})

# --- Products ---
products_data = []
for i in range(1, 201):
    cat_id = random.randint(1, len(CATEGORIES))
    products_data.append({
        "id": i,
        "name": fake.catch_phrase(),
        "category_id": cat_id,
        "price": round(random.uniform(5.0, 500.0), 2)
    })

products = pd.DataFrame(products_data)

# --- Users ---
users_data = []
countries = ["Croatia", "Germany", "Austria", "Slovenia", "France", "Netherlands"]
for i in range(1, 1001):
    country = random.choice(countries)
    users_data.append({
        "id": i,
        "created_at": fake.date_time_between(start_date="-2y", end_date="now"),
        "country": country,
        "city": fake.city()
    })

users = pd.DataFrame(users_data)

# --- Orders ---
orders_data = []
for i in range(1, 5001):
    orders_data.append({
        "id": i,
        "user_id": random.randint(1, 1000),
        "created_at": fake.date_time_between(start_date="-2y", end_date="now"),
        "status": random.choices(
            ["completed", "cancelled", "pending"],
            weights=[0.75, 0.15, 0.10]
        )[0],
        "total_amount": 0.0  # calculated after order_items
    })

orders = pd.DataFrame(orders_data)

# --- Order Items ---
order_items_data = []
item_id = 1
for order_id in orders["id"]:
    num_items = random.randint(1, 5)
    order_total = 0.0
    for _ in range(num_items):
        product = products.sample(1).iloc[0]
        quantity = random.randint(1, 4)
        unit_price = float(product["price"])
        order_total += unit_price * quantity
        order_items_data.append({
            "id": item_id,
            "order_id": order_id,
            "product_id": int(product["id"]),
            "quantity": quantity,
            "unit_price": unit_price
        })
        item_id += 1
    orders.loc[orders["id"] == order_id, "total_amount"] = round(order_total, 2)

order_items = pd.DataFrame(order_items_data)

# --- Sessions ---
sessions_data = []
for i in range(1, 8001):
    sessions_data.append({
        "id": i,
        "user_id": random.choices(
            [random.randint(1, 1000), None],
            weights=[0.70, 0.30]
        )[0],
        "started_at": fake.date_time_between(start_date="-2y", end_date="now"),
        "source": random.choices(
            ["organic", "paid", "email", "direct"],
            weights=[0.40, 0.30, 0.15, 0.15]
        )[0],
        "converted": random.choices([True, False], weights=[0.25, 0.75])[0]
    })

sessions = pd.DataFrame(sessions_data)

# --- Export to CSV ---
categories.to_csv(OUTPUT_DIR / "categories.csv", index=False)
products.to_csv(OUTPUT_DIR / "products.csv", index=False)
users.to_csv(OUTPUT_DIR / "users.csv", index=False)
orders.to_csv(OUTPUT_DIR / "orders.csv", index=False)
order_items.to_csv(OUTPUT_DIR / "order_items.csv", index=False)
sessions.to_csv(OUTPUT_DIR / "sessions.csv", index=False)

print("Data generated successfully:")
print(f"  categories : {len(categories):>6} rows -> data/raw/categories.csv")
print(f"  products   : {len(products):>6} rows -> data/raw/products.csv")
print(f"  users      : {len(users):>6} rows -> data/raw/users.csv")
print(f"  orders     : {len(orders):>6} rows -> data/raw/orders.csv")
print(f"  order_items: {len(order_items):>6} rows -> data/raw/order_items.csv")
print(f"  sessions   : {len(sessions):>6} rows -> data/raw/sessions.csv")
