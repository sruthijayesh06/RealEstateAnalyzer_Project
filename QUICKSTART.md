# Quick Start Guide - Real Estate Analyzer Frontend

## 🚀 Get Started in 3 Steps

### Step 1: Install Flask
```bash
pip install Flask
```

### Step 2: Run the Application
```bash
python app.py
```

You should see:
```
 * Running on http://localhost:5000
```

### Step 3: Open in Browser
Navigate to:
```
http://localhost:5000
```

---

## 📖 What You'll See

### Left Sidebar Navigation
- **Dashboard** - Overview and statistics
- **Properties** - Browse all analyzed properties
- **Chat with AI** - Ask questions about properties
- **Analysis Parameters** - Customize financial calculations
- **Filters & Search** - Advanced filtering
- **Export** - Download data as CSV or JSON

### Main Content Area
- **Top Bar** - Search and breadcrumb navigation
- **Content Pages** - Change based on sidebar selection
- **Tables & Charts** - Data visualization

---

## 🎮 Common Tasks

### View Property Recommendations
1. Click "Properties" in sidebar
2. Use filters to narrow down results
3. Check the "Decision" column for Buy/Rent recommendations

### Customize Analysis
1. Click "Analysis Parameters" in sidebar
2. Adjust parameters like loan rate, tax rate, etc.
3. Click "Run Analysis with New Parameters"
4. Wait for analysis to complete
5. Refresh dashboard to see new results

### Export Data
1. Click "Export as CSV" or "Export as JSON" in sidebar
2. File will download to your Downloads folder

### Ask AI Questions
1. Click "Chat with AI" in sidebar
2. Type your question in the chat box
3. Press Enter or click Send button

---

## 📊 Dashboard Statistics

The dashboard shows:
- **Total Properties** - Total number of analyzed properties
- **Buy Recommendations** - Properties where buying is better financially
- **Rent Recommendations** - Properties where renting is better financially
- **Average Price** - Average property price in the dataset
- **Buy vs Rent Chart** - Visual distribution
- **Price Distribution** - Average pricing overview

---

## 🔧 Customization Parameters

### Loan Parameters
- **Down Payment (%)** - Percentage of property price as down payment (default: 20%)
- **Loan Interest Rate (%)** - Annual home loan interest (default: 8.5%)
- **Tax Rate (%)** - Income tax rate (default: 20%)
- **Property Appreciation (%/year)** - Annual property price growth (default: 5%)

### Rent Parameters
- **Rent Escalation (%/year)** - Annual rent increase (default: 5%)
- **Investment Return Rate (%/year)** - Annual return on investments (default: 10%)
- **Monthly Savings (₹)** - Monthly amount saved while renting (default: ₹15,000)

---

## 🐛 Troubleshooting

### "Connection refused" error
- Make sure Flask app is running: `python app.py`
- Check if port 5000 is not blocked by firewall

### "No properties found" message
- Ensure analysis has been run: `python run.py`
- Check if data file exists: `data/outputs/analyzed_properties.csv`

### Browser showing blank page
- Clear browser cache: Ctrl+Shift+Delete (Chrome/Firefox)
- Try in Incognito/Private window
- Check browser console for errors: F12 → Console

### Charts not showing
- Ensure JavaScript is enabled in browser
- Clear browser cache
- Reload the page

---

## 📱 Features Overview

| Feature | Location | Purpose |
|---------|----------|---------|
| Dashboard | Sidebar → Dashboard | Overview and statistics |
| Property Browser | Sidebar → Properties | View all properties |
| Smart Filtering | Sidebar → Filters & Search | Filter by criteria |
| Parameters | Sidebar → Analysis Parameters | Customize calculations |
| AI Chat | Sidebar → Chat with AI | Ask questions |
| CSV Export | Sidebar → Export as CSV | Download as spreadsheet |
| JSON Export | Sidebar → Export as JSON | Download as JSON |

---

## 💡 Pro Tips

1. **Bulk Operations**: Use filters + export to get specific property sets
2. **What-If Analysis**: Try different parameters to see impact on decisions
3. **Comparison**: Export results and compare with your own spreadsheet
4. **Chat Assistant**: Use natural language to query the data
5. **Mobile**: Works on tablets for on-the-go analysis

---

## 🔐 Data Privacy

- All data processing happens locally
- No data is sent to external servers (except for AI features with proper API keys)
- Your analysis parameters are stored locally

---

## 📞 Need Help?

Check the detailed documentation:
- Full Guide: [FRONTEND_README.md](FRONTEND_README.md)
- Main Project: [README.md](README.md)

---

**Happy Analyzing! 🏠📊**
