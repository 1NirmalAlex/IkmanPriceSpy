import pandas as pd
import sys
import io
import warnings

# Suppress unnecessary pandas and requests warnings
warnings.filterwarnings("ignore")

# Ensure the output supports emojis and clean formatting across all terminals
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def analyze_price(search_query):
    try:
        df = pd.read_csv('phone_market_data.csv')
    except FileNotFoundError:
        print("\n[!] Error: 'phone_market_data.csv' not found!")
        print(" -> Please run 'ikman_cleaner.py' first to build your database.")
        return

    # Filter data based on user search query
    results = df[df['Name'].str.contains(search_query, case=False, na=False)]

    if results.empty:
        print(f"\n[?] Notice: No previous data found for '{search_query}'.")
        print(" -> Suggestion: Run the scraper to collect new data from the market.")
        return

    # Separate data by dates
    latest_date = results['Date'].max()
    oldest_date = results['Date'].min()

    # Calculate average prices
    latest_avg_price = results[results['Date'] == latest_date]['Price'].mean()
    old_avg_price = results[results['Date'] == oldest_date]['Price'].mean()

    # --- BEAUTIFIED OUTPUT ---
    print("\n" + "="*45)
    print(f" 📊 MARKET ANALYSIS: {search_query.upper()} ")
    print("="*45)
    print(f" 📅 Data Span       : {oldest_date} to {latest_date}")
    print(f" 💰 Current Avg Price: Rs. {latest_avg_price:,.2f}")

    if latest_date != oldest_date:
        diff = latest_avg_price - old_avg_price
        percentage = (diff / old_avg_price) * 100

        print("-"*45)
        if diff < 0:
            print(f" 📉 Market Status   : Price Decreased by Rs. {abs(diff):,.2f} ({abs(percentage):.1f}%)")
        elif diff > 0:
            print(f" 📈 Market Status   : Price Increased by Rs. {diff:,.2f} ({percentage:.1f}%)")
        else:
            print(" ⚖️ Market Status   : Stable (No price change observed)")
    else:
        print("-"*45)
        print(" ℹ️ Market Status   : Not enough historical data to compare.")
        print("                      (Please wait a few days for new data updates)")
    
    print("="*45)

# --- MAIN USER INTERFACE ---
print("\n" + "*"*50)
print("       USED MOBILE PRICE TRACKER (IKMAN)        ")
print("*"*50)

# එක දිගටම රන් වීමට Loop එකක් ඇතුළත් කිරීම
while True:
    print("\n" + "-"*45)
    user_input = input("Enter phone models (or type 'exit' to quit): ").strip()
    
    # යූසර් exit කියා ගැසුවහොත් ලූප් එකෙන් ඉවත් වීම
    if user_input.lower() in ['exit', 'quit', 'e']:
        print("\nThank you for using Ikman Price Tracker! Have a great day.\n")
        break
        
    if not user_input:
        continue
        
    # කොමා වලින් වෙන් කරලා නම් කිහිපයක් දුන්නොත් ඒවත් වෙන වෙනම බලනවා
    models = [m.strip() for m in user_input.split(",")]
    
    for model in models:
        analyze_price(model)