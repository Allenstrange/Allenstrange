import requests
import pandas as pd
import io
import re
import sys
import os

# Add backend directory to sys.path so we can import models
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sqlmodel import Session, select
from backend.database import engine, create_db_and_tables
from backend.models import Sponsor

GOV_UK_PAGE = "https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers"

def get_csv_url():
    """
    Fetches the Gov.uk page and finds the link to the CSV file.
    Looking specifically for the "Worker" register.
    """
    print(f"Fetching page: {GOV_UK_PAGE}")
    try:
        response = requests.get(GOV_UK_PAGE)
        response.raise_for_status()

        links = re.findall(r'href="([^"]+\.csv)"', response.text)

        worker_link = None
        for link in links:
            if "Worker" in link:
                worker_link = link
                break

        if not worker_link and links:
            worker_link = links[0]

        if worker_link:
            url = worker_link
            if not url.startswith("http"):
                url = "https://www.gov.uk" + url
            print(f"Found CSV URL: {url}")
            return url
        else:
            print("Could not find CSV link on the page.")
            return None
    except Exception as e:
        print(f"Error fetching page: {e}")
        return None

def fetch_and_parse_csv(url):
    print("Downloading CSV data...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(io.StringIO(response.text))
        return df
    except Exception as e:
        print(f"Error downloading or parsing CSV: {e}")
        return None

def ingest_to_db(df):
    """
    Iterates through the DataFrame and upserts sponsors into the SQLite DB.
    """
    print("Ingesting into database...")
    create_db_and_tables()

    with Session(engine) as session:
        # For MVP, we'll just wipe and reload or simple insert.
        # A full production ingestion would handle diffs.
        # Let's check count first.
        existing_count = session.exec(select(Sponsor)).all()
        if len(existing_count) > 0:
            print(f"Database already has {len(existing_count)} records. Truncating for fresh load...")
            session.exec(Sponsor.__table__.delete())
            session.commit()

        # Bulk insert is faster
        sponsors_to_add = []
        # Expected columns: ['Organisation Name', 'Town/City', 'County', 'Type & Rating', 'Route']

        for _, row in df.iterrows():
            org_name = str(row.get('Organisation Name', ''))
            sponsor = Sponsor(
                organisation_name=org_name,
                town_city=str(row.get('Town/City', '')),
                county=str(row.get('County', '')),
                type_rating=str(row.get('Type & Rating', '')),
                route=str(row.get('Route', '')),
                normalized_name=org_name.lower().strip()
            )
            sponsors_to_add.append(sponsor)

            # Batch commit every 1000
            if len(sponsors_to_add) >= 1000:
                session.add_all(sponsors_to_add)
                session.commit()
                sponsors_to_add = []

        if sponsors_to_add:
            session.add_all(sponsors_to_add)
            session.commit()

        print("Ingestion complete.")

def main():
    csv_url = get_csv_url()
    if not csv_url:
        print("Aborting ingestion.")
        return

    df = fetch_and_parse_csv(csv_url)
    if df is not None:
        print(f"Successfully loaded {len(df)} rows.")
        ingest_to_db(df)

if __name__ == "__main__":
    main()
