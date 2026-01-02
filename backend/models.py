from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class Sponsor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    organisation_name: str = Field(index=True)
    town_city: Optional[str] = None
    county: Optional[str] = None
    type_rating: Optional[str] = None
    route: Optional[str] = None

    # Normalized fields for search
    normalized_name: str = Field(index=True)

class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    employer_name: str = Field(index=True)
    is_verified_sponsor: bool = Field(default=False)
    location: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    soc_code: Optional[str] = None
    apply_url: str
    posted_date: datetime = Field(default_factory=datetime.utcnow)
