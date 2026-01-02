from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import Optional, List
from contextlib import asynccontextmanager

try:
    from backend.database import get_session, create_db_and_tables
    from backend.models import Job, Sponsor
except ImportError:
    from database import get_session, create_db_and_tables
    from models import Job, Sponsor

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="UK Visa Jobs Platform API",
    description="API for the UK International Student Recruitment Platform",
    version="0.1.0",
    lifespan=lifespan
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"], # Allow all for MVP sandbox
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the UK Visa Jobs Platform API"}

@app.get("/jobs")
def get_jobs(
    search: Optional[str] = None,
    sponsor_verified: Optional[bool] = None,
    session: Session = Depends(get_session)
):
    statement = select(Job)
    if search:
        statement = statement.where(Job.title.contains(search))
    if sponsor_verified:
        statement = statement.where(Job.is_verified_sponsor == True)

    jobs = session.exec(statement).all()
    return {"data": jobs, "total": len(jobs)}

@app.get("/employers/verify")
def verify_employer(
    name: str = Query(..., min_length=1),
    session: Session = Depends(get_session)
):
    normalized_query = name.lower().strip()
    statement = select(Sponsor).where(Sponsor.normalized_name.contains(normalized_query)).limit(10)
    results = session.exec(statement).all()

    verified = len(results) > 0
    return {
        "verified": verified,
        "query": name,
        "matches": results
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}
