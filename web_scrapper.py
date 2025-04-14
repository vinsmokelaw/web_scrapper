import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

URL = "https://vacancymail.co.zw/jobs/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_jobs():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch the page: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    print("Page title:", soup.title.text if soup.title else "No title found")
    job_cards = soup.select("a.job-listing")
    print(f"Found {len(job_cards)} job cards")

    with open("debug_page.html", "w", encoding="utf-8") as f:
        f.write(soup.prettify())

    jobs = []
    for job in job_cards[:10]:  # top 10 jobs
        try:
            title = job.select_one("h3.job-listing-title").text.strip()
            description_snippet = job.select_one("p.job-listing-text").text.strip()

            location = "Not specified"
            expiry_date = "Not specified"

            # Extract footer info
            footer_items = job.select("div.job-listing-footer li")
            for item in footer_items:
                text = item.get_text(strip=True)
                if "Expires" in text:
                    expiry_date = text.replace("Expires", "").strip()
                elif item.select_one("i.icon-material-outline-location-on"):
                    location = text

            link = "https://vacancymail.co.zw" + job["href"]

            # Optional: fetch full job description from job detail page
            description = fetch_description(link)

            jobs.append({
                "Title": title,
                "Location": location,
                "Expiry Date": expiry_date,
                "Snippet": description_snippet,
                "Description": description,
                "Link": link
            })

        except Exception as e:
            logging.warning(f"Failed to parse a job card: {e}")
            continue

    return jobs

def fetch_description(job_url):
    try:
        res = requests.get(job_url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        desc = soup.select_one("div.description")
        return desc.get_text(separator="\n").strip() if desc else "No description available"
    except Exception as e:
        logging.warning(f"Could not fetch job description from {job_url}: {e}")
        return "Failed to load description"

def save_to_csv(jobs, filename="scraped_data.csv"):
    try:
        df = pd.DataFrame(jobs)
        df.drop_duplicates(inplace=True)
        df.to_csv(filename, index=False)
        logging.info(f"Saved {len(df)} jobs to {filename}")
    except Exception as e:
        logging.error(f"Failed to save data: {e}")

def main():
    logging.info("Job scraping started.")
    jobs = fetch_jobs()
    if jobs:
        save_to_csv(jobs)
    else:
        logging.warning("No jobs were scraped.")
    logging.info("Job scraping finished.")

if __name__ == "__main__":
    main()
