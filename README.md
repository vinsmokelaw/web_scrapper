# VacancyMail Job Scraper

This Python script scrapes the latest job listings from [VacancyMail Zimbabwe](https://vacancymail.co.zw/jobs/) and saves the data to a CSV file. It extracts job titles, company names, locations, expiry dates, and job descriptions. The script uses `requests` and `BeautifulSoup` for web scraping, and `pandas` to handle and save the data.

It also includes logging to track activity and errors, saving logs in `scraper.log`. If any jobs fail to load or parse, the issues will be logged. The script limits scraping to the latest 10 jobs to reduce strain on the website and speed up processing.

After running, the user is prompted to choose if they want to set up a daily schedule using Task Scheduler (Windows). This makes it easy to automate scraping without needing to run it manually each day.

## Requirements

- Python 3
- requests
- beautifulsoup4
- pandas

You can install the dependencies using:

```bash
pip install -r requirements.txt
