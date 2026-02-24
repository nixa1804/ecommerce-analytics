from fastapi import APIRouter
from api.services.data_loader import (
    load_orders,
    load_order_items,
    load_products,
    load_categories,
)

router = APIRouter(prefix="/demand", tags=["Demand"])


def _build_items_df():
    orders = load_orders()
    order_items = load_order_items()
    products = load_products()
    categories = load_categories()

    completed = orders[orders["status"] == "completed"].copy()
    completed["month"] = completed["created_at"].dt.to_period("M").astype(str)

    items = order_items.merge(
        products[["id", "name", "category_id"]].rename(
            columns={"id": "product_id_ref", "name": "product_name"}
        ),
        left_on="product_id",
        right_on="product_id_ref",
    ).drop(columns="product_id_ref")

    items = items.merge(
        categories.rename(
            columns={"id": "category_id_ref", "name": "category_name"}
        ),
        left_on="category_id",
        right_on="category_id_ref",
    ).drop(columns="category_id_ref")

    items = items.merge(
        completed[["id", "month", "user_id"]].rename(columns={"id": "order_id_ref"}),
        left_on="order_id",
        right_on="order_id_ref",
    ).drop(columns="order_id_ref")

    return items


@router.get("/by-category")
def get_demand_by_category():
    items = _build_items_df()

    result = (
        items.groupby(["month", "category_name"])
        .agg(units_sold=("quantity", "sum"))
        .reset_index()
    )

    return result.to_dict(orient="records")


@router.get("/growth")
def get_revenue_growth():
    orders = load_orders()
    completed = orders[orders["status"] == "completed"].copy()
    completed["month"] = completed["created_at"].dt.to_period("M").astype(str)

    monthly = (
        completed.groupby("month")["total_amount"].sum().reset_index()
    )
    monthly.columns = ["month", "revenue"]
    monthly["prev_revenue"] = monthly["revenue"].shift(1)
    monthly["growth_rate_pct"] = (
        (monthly["revenue"] - monthly["prev_revenue"])
        / monthly["prev_revenue"]
        * 100
    ).round(2)

    return monthly.dropna(subset=["growth_rate_pct"]).iloc[1:].to_dict(
        orient="records"
    )


@router.get("/top-products")
def get_top_products(limit: int = 20):
    items = _build_items_df()

    result = (
        items.groupby(["product_name", "category_name"])
        .agg(
            total_units=("quantity", "sum"),
            total_revenue=("unit_price", lambda x: (x * items.loc[x.index, "quantity"]).sum()),
            unique_buyers=("user_id", "nunique"),
        )
        .reset_index()
        .sort_values("total_units", ascending=False)
        .head(limit)
    )

    result["total_revenue"] = result["total_revenue"].round(2)

    return result.to_dict(orient="records")
