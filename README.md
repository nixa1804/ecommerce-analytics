# E-commerce Analytics

E-commerce Analytics combines transactional and behavioral data into one analytical layer. The project delivers cohort views, conversion and retention funnels, and demand indicators that support planning and growth decisions.

**Live demo:** [ecommerce-analytics-nmev.onrender.com](https://ecommerce-analytics-nmev.onrender.com/)

## Tech Stack

- **Python** — data processing, metric preparation, synthetic data generation
- **SQL** — schema definition, KPI queries, cohort and demand analysis
- **FastAPI** — REST API for analytics queries and third-party integrations
- **Chart.js** — interactive web dashboard served directly from the API
- **Docker** — containerized local and production environment

## Project Goals

- Create clear KPI dashboards for revenue and conversion
- Analyze user cohorts and repeat purchase behavior
- Support demand forecasting with data-backed indicators

## Architecture

```
data/raw/ (CSV or PostgreSQL)
     ↓
Python ETL (data/generate_data.py)
     ↓
FastAPI REST API (api/)
     ↓
Web Dashboard (templates/dashboard.html)
```

- Data layer supports both CSV files and PostgreSQL via `DATABASE_URL` environment variable
- On startup, the app auto-generates synthetic data if no data source is configured
- All analytics endpoints are publicly accessible via REST API for third-party integrations
- Dashboard is responsive and works on desktop and mobile

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web dashboard |
| GET | `/docs` | Interactive API documentation |
| GET | `/kpi/summary` | Total revenue, orders, AOV, completion rate |
| GET | `/kpi/revenue` | Monthly revenue breakdown |
| GET | `/kpi/conversion` | Conversion rate by traffic source |
| GET | `/cohorts/retention` | Cohort retention rates (first 12 months) |
| GET | `/cohorts/repeat-purchase` | Repeat purchase rate by cohort |
| GET | `/demand/growth` | Monthly revenue growth rate |
| GET | `/demand/top-products` | Top N products by units sold |
| GET | `/demand/by-category` | Units sold by category per month |

## Local Setup

**Requirements:** Python 3.13+, Docker

```bash
git clone https://github.com/nixa1804/ecommerce-analytics.git
cd ecommerce-analytics

python -m venv venv
venv/Scripts/activate       # Windows
source venv/bin/activate    # macOS/Linux

pip install -r requirements.txt
uvicorn api.main:app --reload
```

Open `http://localhost:8000` for the dashboard and `http://localhost:8000/docs` for the API.

**With Docker:**

```bash
docker-compose up -d
```

## Integration

To connect your own data source, set the `DATABASE_URL` environment variable pointing to a PostgreSQL database with the schema defined in `sql/schema.sql`:

```bash
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

Without `DATABASE_URL`, the app runs on auto-generated synthetic data.

## Project Structure

```
ecommerce-analytics/
├── api/
│   ├── main.py               # FastAPI app entry point
│   ├── routers/              # KPI, cohort, demand endpoints
│   └── services/             # Data loading (CSV or PostgreSQL)
├── data/
│   ├── raw/                  # CSV data (auto-generated)
│   └── generate_data.py      # Synthetic data generator
├── notebooks/                # Jupyter notebooks for analysis
├── sql/                      # Schema and analytical queries
├── templates/                # Web dashboard HTML
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Outcomes

- Single source of truth for sales and conversion KPIs
- Clear cohort insights for retention and repeat purchase strategy
- Better planning quality through demand signal tracking
