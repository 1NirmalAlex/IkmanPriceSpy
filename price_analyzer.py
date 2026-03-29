import pandas as pd
import sys
import io
import time
import csv
import re
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import warnings

# Suppress warnings and force UTF-8
warnings.filterwarnings("ignore")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CSV_FILE = 'phone_market_data.csv'

def live_scrape_ikman(query):
    """Performs live scrape with INSTANT notification to the user."""
    
    # --- THIS SECTION NOW APPEARS INSTANTLY ---
    print("\n" + "!"*55, flush=True)
    print(" SYSTEM NOTIFICATION: DATA NOT FOUND IN LOCAL DATABASE ", flush=True)
    print(" ACTION: INITIALIZING LIVE MARKET SCRAPER ", flush=True)
    print(f" TARGET: Searching for '{query}' on Ikman.lk", flush=True)
    print(" PLEASE WAIT: This process takes approx. 15-20 seconds...", flush=True)
    print("!"*55, flush=True)
    
    # Now start the heavy process (Browser loading)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--log-level=3")
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        search_url = f"https://ikman.lk/en/ads/sri-lanka/mobile-phones?query={query.replace(' ', '+')}"
        driver.get(search_url)
        
        print(" -> Connecting to server...", flush=True)
        time.sleep(4) 
        
        scraped_data = []
        ads = driver.find_elements(By.CLASS_NAME, "gtm-normal-ad")
        
        print(f" -> Extracting market listings for '{query}'...", flush=True)
        for ad in ads:
            try:
                name = ad.find_element(By.CSS_SELECTOR, "span.heading--2Z_2A, h2").text
                price_str = ad.find_element(By.CSS_SELECTOR, "div.price--3_mQu, span").text
                
                if all(word in name.lower() for word in query.lower().split()):
                    clean_price = int(price_str.replace("Rs", "").replace(",", "").strip())
                    scraped_data.append([name, clean_price, str(date.today())])
            except:
                continue
                
        driver.quit()

        if scraped_data:
            with open(CSV_FILE, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if file.tell() == 0:
                    writer.writerow(["Name", "Price", "Date"])
                writer.writerows(scraped_data)
            print(f" -> SUCCESS: {len(scraped_data)} records added to database.", flush=True)
            return True
        else:
            print(f" -> NOTICE: No live listings found for '{query}'.", flush=True)
            return False
    except Exception as e:
        print(f" -> ERROR during live scrape: {e}", flush=True)
        return False

def extract_capacity(name):
    """Extracts storage capacity from the phone name."""
    match = re.search(r'(\d+)\s*(GB|TB|gb|tb)', name)
    return match.group(0).upper() if match else "Standard/Misc"

def analyze_price(search_query):
    try:
        df = pd.read_csv(CSV_FILE)
        results = df[df['Name'].str.contains(search_query, case=False, na=False)]
    except FileNotFoundError:
        results = pd.DataFrame()

    if results.empty:
        # Scraper starts here and notification shows immediately
        if live_scrape_ikman(search_query):
            df = pd.read_csv(CSV_FILE)
            results = df[df['Name'].str.contains(search_query, case=False, na=False)]
        else:
            return

    results['Capacity'] = results['Name'].apply(extract_capacity)
    
    latest_date = results['Date'].max()
    oldest_date = results['Date'].min()

    print("\n" + "="*55, flush=True)
    print(f" 📊 MARKET ANALYSIS: {search_query.upper()} ", flush=True)
    print("="*55, flush=True)
    print(f" 📅 Tracking Period : {oldest_date} to {latest_date}", flush=True)
    
    capacities = results['Capacity'].unique()
    for cap in sorted(capacities):
        cap_data = results[results['Capacity'] == cap]
        latest_avg = cap_data[cap_data['Date'] == latest_date]['Price'].mean()
        old_avg = cap_data[cap_data['Date'] == oldest_date]['Price'].mean()
        
        if pd.isna(latest_avg): continue

        print(f"\n STORAGE: {cap}", flush=True)
        print(f" -> Current Avg Price: Rs. {latest_avg:,.2f}", flush=True)

        if latest_date != oldest_date and not pd.isna(old_avg):
            diff = latest_avg - old_avg
            perc = (diff / old_avg) * 100
            status = f"📉 Down Rs. {abs(diff):,.0f} ({abs(perc):.1f}%)" if diff < 0 else \
                     f"📈 Up Rs. {diff:,.0f} ({perc:.1f}%)" if diff > 0 else "⚖️ Stable"
            print(f" -> Market Trend     : {status}", flush=True)
    
    print("="*55, flush=True)

# --- CONTINUOUS MAIN LOOP ---
print("\n" + "*"*60, flush=True)
print("       PROFESSIONAL USED MOBILE PRICE TRACKER (IKMAN)        ", flush=True)
print("*"*60, flush=True)

while True:
    print("\n" + "-"*55, flush=True)
    user_input = input("Enter phone model to analyze (or type 'exit' to quit): ").strip()
    
    if user_input.lower() in ['exit', 'quit', 'e']:
        print("\nSession ended. Database updated. Have a productive day!\n", flush=True)
        break
        
    if not user_input:
        continue
        
    models = [m.strip() for m in user_input.split(",")]
    for model in models:
        analyze_price(model)