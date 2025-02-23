import requests

# Base URL for World Bank API
base_url = "http://api.worldbank.org/v2/"

# Example endpoint: Get country data (list of countries)
def get_country_data():
    endpoint = "country"
    url = f"{base_url}{endpoint}?format=json"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error: ", response.status_code)
        return None

# Example endpoint: Get indicator data (e.g., GDP data for a specific country)
def get_indicator_data(country_code, indicator_code):
    endpoint = f"country/{country_code}/indicator/{indicator_code}"
    url = f"{base_url}{endpoint}?format=json"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error: ", response.status_code)
        return None

# Example Usage: Get country list
countries = get_country_data()
if countries:
    print(countries)

# Example Usage: Get GDP indicator for United States (USA)
gdp_data = get_indicator_data("USA", "NY.GDP.MKTP.CD")  # GDP indicator code
if gdp_data:
    print(gdp_data)
