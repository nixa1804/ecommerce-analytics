from fastapi import APIRouter
from api.services.data_loader import load_orders, load_sessions

router = APIRouter(prefix="/kpi", tags=["KPI"])


@router.get("/revenue")
def get_revenue_kpis():
    orders = load_orders()
    completed = orders[orders["status"] == "completed"].copy()
    completed["month"] = completed["created_at"].dt.to_period("M").astype(str)

    monthly = (
        completed.groupby("month")
        .agg(
            total_revenue=("total_amount", "sum"),
            order_count=("id", "count"),
            avg_order_value=("total_amount", "mean"),
        )
        .reset_index()
    )

    monthly["total_revenue"] = monthly["total_revenue"].round(2)
    monthly["avg_order_value"] = monthly["avg_order_value"].round(2)

    return monthly.to_dict(orient="records")


@router.get("/conversion")
def get_conversion_by_source():
    sessions = load_sessions()

    result = (
        sessions.groupby("source")
        .agg(total_sessions=("id", "count"), conversions=("converted", "sum"))
        .reset_index()
    )

    result["conversion_rate_pct"] = (
        result["conversions"] / result["total_sessions"] * 100
    ).round(2)

    return result.to_dict(orient="records")


@router.get("/summary")
def get_summary():
    orders = load_orders()
    completed = orders[orders["status"] == "completed"]

    return {
        "total_revenue": round(float(completed["total_amount"].sum()), 2),
        "total_orders": int(completed["id"].count()),
        "avg_order_value": round(float(completed["total_amount"].mean()), 2),
        "completion_rate_pct": round(
            len(completed) / len(orders) * 100, 2
        ),
    }
