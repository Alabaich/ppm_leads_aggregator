from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import database
from app.api.endpoints import webhooks, leads

# 1. Initialize Database
database.init_db()

app = FastAPI(title="Lead Ingestion System")

# 2. Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Include Modular Routers
app.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
app.include_router(leads.router, prefix="/leads", tags=["Leads"])

# 4. Health Check
@app.get("/")
def read_root():
    return {
        "status": "System is online",
        "database": "Connected",
        "table": "Leads table ready"
    }