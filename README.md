# 🏠 Real Estate Analyzer – MagicBricks Scraper

A Playwright-based web scraping project that collects **real estate listing data across multiple Indian cities** from MagicBricks and computes **derived metrics like total property price**.

This project is designed to be:
- Reliable (avoids aggressive anti-bot issues)
- Scalable (multi-city support)
- Analysis-ready (clean numeric fields)

---

## 📌 Features

- Scrapes **property listings from MagicBricks**
- Supports **multiple Indian cities**
- Extracts:
  - Property title
  - City & locality
  - Price per sqft
  - Area (sqft)
  - Bedrooms
  - Property link
- Calculates:
  - **Total price (INR)** = price per sqft × area
- Saves data into **CSV files**
- Uses **Playwright (real browser automation)** for reliability

---

## 🗂 Project Structure

REALESTATEANALYZER/
│
├── src/
│ └── playwright_scraper/
│ └── magicbricks_playwright.py
│
├── data/
│ └── outputs/
│ └── magicbricks_india_properties_<timestamp>.csv
│
├── requirements.txt
└── README.md

---

## ⚙️ Tech Stack

- **Python 3.10+**
- **Playwright**
- **CSV (for data storage)**
- **Regex (data cleaning & parsing)**

---

## 🚀 Setup Instructions

### 1️⃣ Clone / Open Project
Open the project root folder in VS Code:

### 2️⃣ Install Dependencies
Run once in terminal:
```bash
pip install playwright
playwright install

