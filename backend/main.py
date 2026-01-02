from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="UK Visa Jobs Platform API",
    description="API for the UK International Student Recruitment Platform",
    version="0.1.0"
)

class Job(BaseModel):
    id: str
    title: str
    employer_name: str
    verified_sponsor: bool
    location: str
    salary: Optional[int] = None

@app.get("/")
def read_root():
    return {"message": "Welcome to the UK Visa Jobs Platform API"}

@app.get("/jobs")
def get_jobs(search: Optional[str] = None):
    # Mock response for now
    return {
        "data": [
            {
                "id": "1",
                "title": "Software Engineer",
                "employer_name": "TechNova Ltd",
                "verified_sponsor": True,
                "location": "London",
                "salary": 45000
            }
        ],
        "total": 1
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}
