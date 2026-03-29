# 📱 Used Mobile Price Tracker (Ikman.lk)

A highly efficient, automated Python tool designed to scrape, track, and analyze the used mobile phone market in Sri Lanka using Ikman.lk. This project is tailored for data analysts, e-commerce researchers, or anyone looking to find the best deals by monitoring price drops and market trends.

---

## ✨ Key Features

* **⚡ Smart Live Scraping:** If a requested phone model is missing from the local database, the system automatically triggers a background (headless) browser to fetch real-time data from Ikman.lk.
* **📦 Capacity-Based Grouping:** Intelligently detects and groups devices by their storage capacity (e.g., 64GB, 128GB, 256GB) using advanced Regex, providing precise pricing for different variants.
* **📊 Market Trend Analysis:** Compares historical data with the latest scraped data to display whether prices have increased, decreased, or remained stable.
* **⏳ Instant User Notifications:** Features forced UTF-8 output and instant console flushing to give the user immediate feedback and wait-time notifications.
* **🚫 Clean Data Only:** Filters out unrelated "Recommended Ads" on Ikman to ensure only accurate matches are saved to the CSV.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Web Scraping:** Selenium WebDriver
* **Data Manipulation:** Pandas
* **Automation:** Webdriver-Manager (Handles automated Chrome driver updates)

---

## 🚀 How to Install & Run

### 1. Clone the repository or download the files manually
```bash
git clone [https://github.com/your-username/IkmanPriceSpy.git](https://github.com/your-username/IkmanPriceSpy.git)
cd IkmanPriceSpy
