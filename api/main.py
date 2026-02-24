from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pathlib import Path
from api.routers import kpi, cohorts, demand

BASE_DIR = Path(__file__).parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

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
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
