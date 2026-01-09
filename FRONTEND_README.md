# Real Estate Analyzer - Frontend Setup Guide

## Overview
This is a modern, responsive web-based frontend for the Real Estate Analyzer application. It provides an intuitive interface with a left sidebar navigation for all customization options.

## Features

### 🎯 Dashboard
- Overview of all analyzed properties
- Key statistics (total properties, buy/rent recommendations, average prices)
- Visual charts for decision distribution and price analytics
- Quick access to all features

### 📊 Properties Browser
- Browse all analyzed properties with detailed information
- Filter by city, decision (buy/rent), and price range
- Pagination for easy navigation
- Sortable columns
- Export capabilities

### ⚙️ Analysis Parameters
- Customize all financial analysis parameters:
  - Down payment percentage
  - Loan interest rate
  - Tax rate
  - Property appreciation rate
  - Rent escalation rate
  - Investment return rate
  - Monthly savings amount
- Run analysis with custom parameters
- Parameters persist across sessions

### 🔍 Filters & Search
- Advanced filtering options
- Filter by location, BHK, and area
- Save favorite filters
- Quick search across properties

### 💬 AI Chat Assistant
- Ask questions about properties and analysis
- RAG (Retrieval-Augmented Generation) powered responses
- Get personalized recommendations
- Natural language queries

### 📥 Export Options
- Export analyzed properties as CSV
- Export as JSON for integration with other tools
- Full data export functionality

## Installation

### Prerequisites
- Python 3.11+
- Pip or conda package manager

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Prepare Data
Make sure your analyzed properties data is in:
```
data/outputs/analyzed_properties.csv
```

## Running the Application

### Start the Flask Server
```bash
python app.py
```

The application will be available at:
```
http://localhost:5000
```

## Project Structure

```
├── app.py                          # Flask application and API endpoints
├── templates/
│   └── index.html                  # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css              # Complete stylesheet
│   └── js/
│       └── main.js                # Frontend logic and interactions
├── src/
│   ├── Parameters/
│   │   ├── analyzer.py            # Analysis engine
│   │   ├── buy_vs_rent.py         # Buy vs rent comparison
│   │   ├── loan.py                # Loan calculations
│   │   ├── bank_comparison.py     # Bank comparison logic
│   │   ├── investing.py           # Investment calculations
│   │   └── tax.py                 # Tax calculations
│   ├── rag/
│   │   ├── rag_engine.py          # RAG query processing
│   │   ├── vector_store.py        # Vector embeddings
│   │   └── intent_classifier.py   # Query intent classification
│   └── playwright_scraper/        # Web scraping utilities
└── data/
    └── outputs/
        └── analyzed_properties.csv # Analysis results
```

## API Endpoints

### Dashboard
- `GET /api/dashboard` - Get dashboard statistics

### Properties
- `GET /api/properties` - Get properties with filters
- `GET /api/city-options` - Get available cities

### Analysis
- `POST /api/analyze` - Run analysis with custom parameters

### RAG
- `POST /api/rag-query` - Submit query to AI assistant

### Export
- `GET /api/export` - Export data (CSV or JSON)

## Customization

### Changing Colors
Edit the CSS variables in `static/css/style.css`:
```css
:root {
    --primary-color: #3498db;
    --secondary-color: #2c3e50;
    --success-color: #2ecc71;
    /* ... more colors ... */
}
```

### Adding New Pages
1. Add page structure in `templates/index.html`
2. Add navigation link in the sidebar
3. Add page styling in `static/css/style.css`
4. Add page logic in `static/js/main.js`

### Backend Integration
The frontend communicates with the backend through JSON APIs. To add new features:
1. Create an API endpoint in `app.py`
2. Add frontend logic in `static/js/main.js`
3. Update the template as needed

## Performance Tips

1. **Caching**: Dashboard data is loaded on page initialization
2. **Pagination**: Properties are paginated to 10 per page (configurable)
3. **Lazy Loading**: Pages only load data when needed
4. **Chart Optimization**: Charts are destroyed and recreated for memory efficiency

## Browser Support
- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change to different port
```

### Data Not Loading
1. Ensure `data/outputs/analyzed_properties.csv` exists
2. Check the file has required columns
3. Check browser console for API errors

### RAG Chat Not Working
- Ensure RAG engine is properly initialized
- Check Gemini API credentials in `.env`
- Verify vector store files exist in `data/vectorstore/`

## Development

### Hot Reload
The Flask app is set to `debug=True`, so changes to Python files will auto-reload.

### Frontend Changes
For CSS/JS changes, simply refresh the browser (browser cache may need clearing).

### Testing API Endpoints
Use curl or Postman:
```bash
curl http://localhost:5000/api/dashboard
```

## Future Enhancements

- [ ] User authentication and profiles
- [ ] Saved searches and filters
- [ ] Property comparison tool
- [ ] Advanced reporting
- [ ] Mobile app version
- [ ] Real-time data updates
- [ ] Collaborative features
- [ ] ML-based recommendations

## License
See main project README for license information

## Support
For issues or feature requests, refer to the main project documentation.
