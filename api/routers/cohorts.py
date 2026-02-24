from fastapi import APIRouter
from api.services.data_loader import load_orders, load_users

router = APIRouter(prefix="/cohorts", tags=["Cohorts"])


@router.get("/retention")
def get_cohort_retention():
    users = load_users()
    orders = load_orders()

    users["cohort_month"] = users["created_at"].dt.to_period("M")
    completed = orders[orders["status"] == "completed"].copy()
    completed["order_month"] = completed["created_at"].dt.to_period("M")

    merged = completed.merge(
        users[["id", "cohort_month"]], left_on="user_id", right_on="id"
    )
    merged["period_number"] = (
        merged["order_month"] - merged["cohort_month"]
    ).apply(lambda x: x.n)
    merged = merged[merged["period_number"].between(0, 11)]

    cohort_sizes = users.groupby("cohort_month")["id"].count().rename("cohort_size")

    cohort_data = (
        merged.groupby(["cohort_month", "period_number"])["user_id"]
        .nunique()
        .reset_index()
    )
    cohort_data = cohort_data.merge(cohort_sizes, on="cohort_month")
    cohort_data["retention_rate_pct"] = (
        cohort_data["user_id"] / cohort_data["cohort_size"] * 100
    ).round(2)
    cohort_data["cohort_month"] = cohort_data["cohort_month"].astype(str)

    return cohort_data[
        ["cohort_month", "period_number", "cohort_size", "retention_rate_pct"]
    ].to_dict(orient="records")


@router.get("/repeat-purchase")
def get_repeat_purchase_rate():
    orders = load_orders()
    completed = orders[orders["status"] == "completed"].copy()

    first_orders = (
        completed.groupby("user_id")["created_at"].min().reset_index()
    )
    first_orders.columns = ["user_id", "first_order_date"]
    first_orders["cohort_month"] = (
        first_orders["first_order_date"].dt.to_period("M").astype(str)
    )

    order_counts = (
        completed.groupby("user_id")["id"].count().reset_index()
    )
    order_counts.columns = ["user_id", "total_orders"]

    buyer_data = first_orders.merge(order_counts, on="user_id")
    buyer_data["is_repeat"] = buyer_data["total_orders"] > 1

    result = (
        buyer_data.groupby("cohort_month")
        .agg(total_buyers=("user_id", "count"), repeat_buyers=("is_repeat", "sum"))
        .reset_index()
    )
    result["repeat_rate_pct"] = (
        result["repeat_buyers"] / result["total_buyers"] * 100
    ).round(2)

    return result.to_dict(orient="records")
