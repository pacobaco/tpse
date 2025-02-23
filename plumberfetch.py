import requests
import pdfplumber
import pandas as pd
from io import BytesIO
import os
from urllib.parse import urlparse
import re

# List of URLs (subset for demonstration; replace with full list as needed)
pdf_urls = [
    "https://apps.bea.gov/scb/pdf/2007/07%20July/0707_ita_annual.pdf",
    "https://home.treasury.gov/system/files/131/FATCA-Agreement-Australia-4-28-2014.pdf",
    "https://home.treasury.gov/system/files/206/shc2021_fullreport.pdf",
    # Add more URLs from your list here
]

# Headers to mimic browser request
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# Function to fetch PDF from URL
def fetch_pdf(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BytesIO(response.content)
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return None

# Function to clean filename from URL
def get_filename_from_url(url):
    path = urlparse(url).path
    filename = os.path.basename(path)
    # Remove invalid characters for filenames
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    return filename

# Function to parse PDF and dump data
def parse_and_dump_pdf(pdf_content, url, output_dir="pdf_dumps"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filename_base = get_filename_from_url(url)
    text_output = f"{output_dir}/{filename_base}_text.txt"
    csv_output = f"{output_dir}/{filename_base}_tables.csv"
    
    all_text = []
    all_tables = []
    
    try:
        with pdfplumber.open(pdf_content) as pdf:
            # Extract text and tables from each page
            for page_num, page in enumerate(pdf.pages, 1):
                # Extract raw text
                text = page.extract_text()
                if text:
                    all_text.append(f"Page {page_num}:\n{text}\n{'='*50}")
                
                # Extract tables
                tables = page.extract_tables()
                for table_num, table in enumerate(tables, 1):
                    if table:
                        # Convert table to DataFrame
                        df = pd.DataFrame(table[1:], columns=table[0] if table[0] else None)
                        all_tables.append({
                            "Page": page_num,
                            "Table": table_num,
                            "Data": df
                        })
        
        # Dump raw text to file
        if all_text:
            with open(text_output, "w", encoding="utf-8") as f:
                f.write("\n".join(all_text))
            print(f"Dumped text to {text_output}")
        
        # Dump tables to CSV
        if all_tables:
            # Combine all tables into one DataFrame with metadata
            combined_df = pd.concat(
                [t["Data"].assign(Page=t["Page"], Table=t["Table"]) for t in all_tables],
                ignore_index=True
            )
            combined_df.to_csv(csv_output, index=False)
            print(f"Dumped tables to {csv_output}")
        else:
            print(f"No tables found in {url}")
            
    except Exception as e:
        print(f"Error parsing {url}: {e}")

# Main execution
for url in pdf_urls:
    print(f"Processing {url}")
    pdf_content = fetch_pdf(url)
    if pdf_content:
        parse_and_dump_pdf(pdf_content, url)
    else:
        print(f"Skipping {url} due to fetch failure")

# Summary
print(f"\nProcessed {len(pdf_urls)} URLs. Check 'pdf_dumps' directory for output.")