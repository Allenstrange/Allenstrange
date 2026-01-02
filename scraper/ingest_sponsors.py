import requests
import pandas as pd
import io
import re

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

        # Looking for <a href="..."> that ends in .csv and likely contains "Worker" in the filename or link text context
        # The Gov.uk links often look like: .../2023-10-04_-_Worker_and_Temporary_Worker.csv

        # Find all CSV links
        links = re.findall(r'href="([^"]+\.csv)"', response.text)

        worker_link = None
        for link in links:
            if "Worker" in link:
                worker_link = link
                break

        # Fallback: if no link has "Worker", just take the first one (risky but better than nothing)
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
    """
    Downloads the CSV and loads it into a Pandas DataFrame.
    """
    print("Downloading CSV data...")
    try:
        response = requests.get(url)
        response.raise_for_status()

        # The Gov.uk CSV is usually utf-8 or latin-1. Let's try loading it.
        # It often has headers like 'Organisation Name', 'Town/City', 'County', 'Type & Rating', 'Route'
        df = pd.read_csv(io.StringIO(response.text))
        return df
    except Exception as e:
        print(f"Error downloading or parsing CSV: {e}")
        return None

def main():
    csv_url = get_csv_url()
    if not csv_url:
        print("Aborting ingestion.")
        return

    df = fetch_and_parse_csv(csv_url)
    if df is not None:
        print(f"Successfully loaded sponsor data.")
        print(f"Total rows: {len(df)}")
        print("Columns:", df.columns.tolist())
        print("\nFirst 5 rows:")
        print(df.head())

        # Basic normalization for the 'canonical' schema mentioned in the spec
        # We want to map this to our 'employers' concept eventually.
        # For now, just saving a sample to disk for inspection (this file is gitignored).
        df.to_csv("scraper/sponsors_dump.csv", index=False)
        print("Saved dump to scraper/sponsors_dump.csv")

if __name__ == "__main__":
    main()
