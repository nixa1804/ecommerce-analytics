from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import kpi, cohorts, demand

app = FastAPI(
    title="E-commerce Analytics API",
    description="Analytics API for revenue KPIs, cohort analysis, and demand indicators.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(kpi.router)
app.include_router(cohorts.router)
app.include_router(demand.router)


@app.get("/")
def root():
    return {"status": "ok", "docs": "/docs"}
