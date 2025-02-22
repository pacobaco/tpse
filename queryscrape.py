import requests
from bs4 import BeautifulSoup

# Define all the individual functions (same as before)

def scrape_contact_info(soup):
    phone_number = soup.find("a", href=lambda x: x and x.startswith("tel:"))
    email = soup.find("a", href=lambda x: x and x.startswith("mailto:"))
    address = soup.find("address")
    social_links = soup.find_all("a", href=lambda x: x and ("facebook" in x or "twitter" in x))
    
    return {
        "Phone": phone_number.get_text() if phone_number else None,
        "Email": email.get_text() if email else None,
        "Address": address.get_text() if address else None,
        "Social Media Links": [link['href'] for link in social_links]
    }

def scrape_reports_and_publications(soup):
    report_links = soup.find_all("a", href=lambda x: x and x.endswith(".pdf"))
    return [link['href'] for link in report_links]

def scrape_statistical_data(soup):
    tables = soup.find_all("table")
    data = []
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if cols:
                data.append([col.get_text().strip() for col in cols])
    return data

def scrape_legislative_info(soup):
    law_links = soup.find_all("a", href=lambda x: x and ("law" in x or "regulation" in x))
    return [link['href'] for link in law_links]

def scrape_tools_and_apis(soup):
    tools = soup.find_all("a", href=lambda x: x and ("api" in x or "tool" in x))
    return [link['href'] for link in tools]

def scrape_news_and_events(soup):
    news_items = soup.find_all("a", href=lambda x: x and "news" in x)
    events = soup.find_all("div", class_="event-date")
    return {
        "News Articles": [link['href'] for link in news_items],
        "Upcoming Events": [event.get_text() for event in events]
    }

def scrape_key_personnel(soup):
    personnel = soup.find_all("div", class_="personnel-list")
    key_personnel = []
    for person in personnel:
        name = person.find("h2")
        role = person.find("p", class_="role")
        if name and role:
            key_personnel.append({"Name": name.get_text(), "Role": role.get_text()})
    return key_personnel

def scrape_licensing_info(soup):
    license_info = soup.find_all("a", href=lambda x: x and "license" in x)
    return [link['href'] for link in license_info]

def scrape_public_databases(soup):
    db_links = soup.find_all("a", href=lambda x: x and ("database" in x or "registry" in x))
    return [link['href'] for link in db_links]

def scrape_documents_and_forms(soup):
    form_links = soup.find_all("a", href=lambda x: x and (".pdf" in x or ".doc" in x))
    return [link['href'] for link in form_links]

def scrape_treasury_data(url):
    # Send GET request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Call each scraping function
    return {
        "Contact Information": scrape_contact_info(soup),
        "Reports and Publications": scrape_reports_and_publications(soup),
        "Statistical Data": scrape_statistical_data(soup),
        "Legislative and Regulatory Information": scrape_legislative_info(soup),
        "Tools and APIs": scrape_tools_and_apis(soup),
        "News and Events": scrape_news_and_events(soup),
        "Key Personnel": scrape_key_personnel(soup),
        "Licensing and Certifications": scrape_licensing_info(soup),
        "Public Databases": scrape_public_databases(soup),
        "Documents and Forms": scrape_documents_and_forms(soup)
    }

# Function to scrape data from a list of URLs
def scrape_multiple_urls(urls):
    results = {}
    for url in urls:
        print(f"Scraping data from: {url}")
        try:
            data = scrape_treasury_data(url)
            results[url] = data
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            results[url] = None
    return results

# List of URLs to scrape
urls_to_scrape = [
    "https://home.treasury.gov/data/treasury-international-capital-tic-system",
    "https://www.gov.uk/government/organisations/hm-treasury",
    "https://www.mof.go.jp/english",
    "https://www.bundesfinanzministerium.de/",
    "http://www.mof.gov.cn/en/",
    "https://treasury.gov.au/",
    "https://www.canada.ca/en/department-finance.html",
    "https://www.finmin.nic.in/",
    "https://www.gov.br/economia/",
    "http://www.treasury.gov.za/",
    "https://minfin.ru/en/",
    "https://www.economie.gouv.fr/",
    "https://www.mef.gov.it/",
    "https://english.moef.go.kr/",
    "https://www.gob.mx/shcp",
    "https://www.mineco.gob.es/",
    "https://www.government.nl/ministries/ministry-of-finance",
    "https://www.efd.admin.ch/",
    "https://www.mof.gov.sg/",
    "https://www.government.se/government-of-sweden/ministry-of-finance/",
    "https://www.regjeringen.no/en/dep/fin/",
    "https://www.argentina.gob.ar/economia",
    "https://en.hmb.gov.tr/",
    "https://www.mof.gov.sa/",
    "https://ec.europa.eu/eurostat",
    "https://data.imf.org/",
    "https://data.worldbank.org/",
    "https://data.oecd.org/",
    "https://www.bis.org/",
    "https://www.spglobal.com/marketintelligence/",
    "https://www.refinitiv.com/",
    "https://www.federalreserve.gov/",
    "https://www.ecb.europa.eu/stats/html/index.en.html",
    "https://data.worldbank.org/topic/financial-sector",
    "https://www.world-exchanges.org/",
    "https://www.ftserussell.com/",
    "https://www.oecd.org/investment/statistics.htm",
    "https://unctad.org/statistics",
    "https://fred.stlouisfed.org/",
    "https://www.bankofengland.co.uk/statistics",
    "http://www.stats.gov.cn/",
    "https://www.bcb.gov.br/",
    "https://www.boj.or.jp/en/statistics/index.htm/",
    "https://www.afdb.org/",
    "https://www.adb.org/data",
    "https://www.iadb.org/en/"
]

# Scrape all URLs
scraped_data = scrape_multiple_urls(urls_to_scrape)

# Print or process the scraped data
for url, data in scraped_data.items():
    print(f"Data for {url}:")
    if data:
        for category, items in data.items():
            print(f"{category}: {items}")
    else:
        print("No data available")
