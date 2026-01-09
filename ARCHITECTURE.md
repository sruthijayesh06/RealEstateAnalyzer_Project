# Real Estate Analyzer - Frontend Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      USER'S BROWSER                             │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    HTML Interface                          │ │
│  │  (templates/index.html - 15 KB)                           │ │
│  │                                                            │ │
│  │  ┌────────────────────────────────────────────────────┐   │ │
│  │  │  Left Sidebar Navigation                           │   │ │
│  │  │  • Dashboard                                       │   │ │
│  │  │  • Properties                                      │   │ │
│  │  │  • Chat with AI                                   │   │ │
│  │  │  • Analysis Parameters                            │   │ │
│  │  │  • Filters & Search                               │   │ │
│  │  │  • Export Options                                 │   │ │
│  │  └────────────────────────────────────────────────────┘   │ │
│  │                                                            │ │
│  │  ┌────────────────────────────────────────────────────┐   │ │
│  │  │  Main Content Area (Dynamic)                       │   │ │
│  │  │  • Dashboard Page                                  │   │ │
│  │  │  • Properties Page                                 │   │ │
│  │  │  • Parameters Page                                 │   │ │
│  │  │  • Filters Page                                    │   │ │
│  │  │  • Chat Page                                       │   │ │
│  │  └────────────────────────────────────────────────────┘   │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                 │                               │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  CSS Styling                                              │ │
│  │  (static/css/style.css - 20 KB)                          │ │
│  │  • Layout & Grid System                                 │ │
│  │  • Responsive Design                                    │ │
│  │  • Animations & Transitions                            │ │
│  │  • Component Styling                                   │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                 │                               │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  JavaScript Logic                                         │ │
│  │  (static/js/main.js - 18 KB)                             │ │
│  │  • Page Navigation                                      │ │
│  │  • API Communication                                   │ │
│  │  • Event Handling                                      │ │
│  │  • Data Processing                                    │ │
│  │  • Chart Management                                   │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                 │                               │
└─────────────────────────────────────────────────────────────────┘
                                  │
                    HTTP/HTTPS API Calls
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FLASK BACKEND                              │
│                      (app.py - 8 KB)                            │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Route: GET /                                             │ │
│  │  Returns: index.html                                      │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  API Endpoints                                            │ │
│  │                                                            │ │
│  │  GET /api/dashboard                                       │ │
│  │  ├─ Returns: statistics, metrics                          │ │
│  │  ├─ Data: total, buy, rent, avg price                     │ │
│  │  └─ Used by: Dashboard page                              │ │
│  │                                                            │ │
│  │  GET /api/properties                                      │ │
│  │  ├─ Params: page, city, decision, price range            │ │
│  │  ├─ Returns: paginated property list                      │ │
│  │  └─ Used by: Properties page                             │ │
│  │                                                            │ │
│  │  GET /api/city-options                                    │ │
│  │  ├─ Returns: list of cities                               │ │
│  │  └─ Used by: Filter dropdown                             │ │
│  │                                                            │ │
│  │  POST /api/analyze                                        │ │
│  │  ├─ Params: 7 financial parameters                        │ │
│  │  ├─ Process: Run analysis with custom parameters          │ │
│  │  ├─ Returns: analysis results                             │ │
│  │  └─ Used by: Analysis Parameters page                    │ │
│  │                                                            │ │
│  │  POST /api/rag-query                                      │ │
│  │  ├─ Params: user question                                 │ │
│  │  ├─ Process: RAG engine query processing                  │ │
│  │  ├─ Returns: AI response                                  │ │
│  │  └─ Used by: Chat page                                   │ │
│  │                                                            │ │
│  │  GET /api/export                                          │ │
│  │  ├─ Params: format (csv/json)                             │ │
│  │  ├─ Returns: data file                                    │ │
│  │  └─ Used by: Export options                              │ │
│  │                                                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                                  │
                        File System Access
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATA & MODELS                                │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  data/outputs/                                            │ │
│  │  • analyzed_properties.csv  (Main data source)            │ │
│  │  • magicbricks_india_final.csv  (Raw data)                │ │
│  │  • magicbricks_india_properties_cleaned.csv (Cleaned)     │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  src/Parameters/                                          │ │
│  │  • analyzer.py       (Main analysis logic)                 │ │
│  │  • buy_vs_rent.py    (Comparison algorithm)                │ │
│  │  • loan.py           (Loan calculations)                   │ │
│  │  • bank_comparison.py (Bank comparison)                   │ │
│  │  • investing.py      (Investment calculations)            │ │
│  │  • tax.py            (Tax calculations)                    │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  src/rag/                                                 │ │
│  │  • rag_engine.py     (RAG query processing)                │ │
│  │  • vector_store.py   (Embeddings)                         │ │
│  │  • intent_classifier.py (Query understanding)             │ │
│  │  • sql_retriever.py  (Data retrieval)                      │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  data/vectorstore/                                        │ │
│  │  • index.faiss       (Vector store for RAG)                │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

### Dashboard Load Flow
```
User Opens App
      │
      ▼
   index.html loads
      │
      ├─ Load CSS (style.css)
      ├─ Load JS (main.js)
      └─ Load icons (Font Awesome CDN)
      │
      ▼
   JavaScript initializes
      │
      ├─ Setup navigation listeners
      ├─ Setup event listeners
      └─ Load city options
      │
      ▼
   Dashboard page loads
      │
      ├─ Fetch /api/dashboard
      │  │
      │  ▼
      │  [Flask Backend]
      │  ├─ Read analyzed_properties.csv
      │  ├─ Calculate statistics
      │  └─ Return JSON
      │
      ├─ Update stat cards
      ├─ Initialize charts (Chart.js)
      ├─ Render dashboard
      └─ Display to user
```

### Property Search Flow
```
User clicks "Properties"
      │
      ▼
Properties page loads
      │
      ├─ Fetch /api/city-options
      │  └─ Populate city dropdown
      │
      └─ Wait for user interaction
      │
      ▼
User applies filters
      │
      ├─ Fetch /api/properties?filters
      │  │
      │  ▼
      │  [Flask Backend]
      │  ├─ Read CSV file
      │  ├─ Apply filters
      │  ├─ Paginate results
      │  └─ Return JSON
      │
      ├─ Render table
      ├─ Update pagination
      └─ Display results
```

### Analysis Parameters Flow
```
User navigates to Parameters page
      │
      ▼
Parameters form loads
      │
      ├─ Display current values
      └─ Wait for user input
      │
      ▼
User adjusts values
      │
      ├─ Collect all parameters
      └─ Click "Run Analysis"
      │
      ▼
      POST /api/analyze
      │
      ▼
   [Flask Backend]
   ├─ Extract parameters
   ├─ Load raw data
   ├─ Run analysis.py
   │  ├─ For each property:
   │  │  ├─ buying_case()
   │  │  ├─ renting_case()
   │  │  └─ compare_results()
   ├─ Save results to CSV
   └─ Return JSON response
      │
      ▼
Show success message
      │
      ▼
Update dashboard
```

### AI Chat Flow
```
User opens Chat page
      │
      ▼
Chat interface loads
      │
      ├─ Display greeting
      └─ Focus input field
      │
      ▼
User types question
      │
      └─ Press Enter or click Send
      │
      ▼
Client adds user message to chat
      │
      ├─ POST /api/rag-query
      │
      ▼
   [Flask Backend]
   ├─ Extract query
   ├─ Initialize RAG engine
   │  ├─ Load vector store
   │  ├─ Query embeddings
   │  ├─ Retrieve relevant docs
   │  └─ Format context
   ├─ Call LLM (Gemini)
   ├─ Process response
   └─ Return answer
      │
      ▼
Client adds bot message to chat
      │
      └─ Display answer to user
```

---

## Component Hierarchy

```
App (Main Container)
│
├── Sidebar Navigation
│   ├── Header (Logo)
│   ├── Nav Sections
│   │   ├── Main
│   │   │   ├── Dashboard Link
│   │   │   ├── Properties Link
│   │   │   └── Chat Link
│   │   ├── Customization
│   │   │   ├── Parameters Link
│   │   │   └── Filters Link
│   │   └── Export
│   │       ├── CSV Export
│   │       └── JSON Export
│   └── Footer (Settings)
│
├── Main Content Area
│   ├── Top Bar
│   │   ├── Breadcrumb Navigation
│   │   ├── Search Box
│   │   └── User Profile
│   │
│   └── Pages (Dynamic)
│       ├── Dashboard Page
│       │   ├── Page Header
│       │   ├── Stats Grid (4 cards)
│       │   └── Charts Section
│       │
│       ├── Properties Page
│       │   ├── Page Header
│       │   ├── Filters Bar
│       │   ├── Data Table
│       │   └── Pagination
│       │
│       ├── Analysis Parameters Page
│       │   ├── Page Header
│       │   ├── Loan Parameters Card
│       │   ├── Rent Parameters Card
│       │   ├── Action Buttons
│       │   └── Status Display
│       │
│       ├── Filters Page
│       │   ├── Page Header
│       │   ├── Location Filter
│       │   ├── BHK Filter
│       │   └── Area Filter
│       │
│       └── Chat Page
│           ├── Page Header
│           ├── Chat Messages Container
│           └── Chat Input Area
│
└── CSS & JavaScript
    ├── Global Styles
    ├── Component Styles
    ├── Responsive Styles
    ├── Animations
    └── Event Handlers
```

---

## Frontend Dependencies

```
HTML5
├── CSS3
│   └── Responsive Design
├── JavaScript (Vanilla)
│   ├── Chart.js (for charts)
│   ├── Font Awesome 6 (for icons)
│   └── Internal Utilities
└── Flask (Backend)
    ├── Pandas (data processing)
    ├── LangChain (RAG)
    └── Analysis Modules
```

---

## File Communication Map

```
Frontend                           Backend
────────────────────────────────────────────
                  
index.html ────────────────────▶ app.py
    │                              │
    ├─ Requests CSS ────────────▶ style.css
    ├─ Requests JS ────────────▶ main.js
    └─ Makes API Calls:
       │
       ├─ GET /           ────────▶ return index.html
       ├─ GET /api/dashboard       └─ Query analyzed_properties.csv
       │                           └─ Return statistics JSON
       ├─ GET /api/properties      └─ Filter & paginate data
       │                           └─ Return properties JSON
       ├─ POST /api/analyze        └─ Run analysis.py
       │                           └─ Save results
       │                           └─ Return status JSON
       ├─ POST /api/rag-query      └─ Process with RAG engine
       │                           └─ Query LLM
       │                           └─ Return answer JSON
       └─ GET /api/export          └─ Export data
                                    └─ Return CSV/JSON file
```

---

## Technology Stack Layers

```
┌─────────────────────────────────────────────────┐
│  User Interface Layer                           │
│  (HTML5 + CSS3 + Vanilla JavaScript)            │
│  • DOM Manipulation                             │
│  • Event Handling                               │
│  • Form Processing                              │
├─────────────────────────────────────────────────┤
│  Presentation Layer                             │
│  (CSS3 Styling)                                 │
│  • Layout (Flexbox, Grid)                       │
│  • Animations                                   │
│  • Responsive Design                            │
├─────────────────────────────────────────────────┤
│  Visualization Layer                            │
│  (Chart.js)                                     │
│  • Chart Rendering                              │
│  • Data Visualization                           │
├─────────────────────────────────────────────────┤
│  Communication Layer                            │
│  (Fetch API)                                    │
│  • HTTP Requests                                │
│  • JSON Processing                              │
├─────────────────────────────────────────────────┤
│  API Layer                                      │
│  (Flask)                                        │
│  • Route Handling                               │
│  • Request Processing                           │
│  • Response Generation                          │
├─────────────────────────────────────────────────┤
│  Business Logic Layer                           │
│  (Python Analysis Modules)                      │
│  • buy_vs_rent.py                               │
│  • loan.py                                      │
│  • analyzer.py                                  │
├─────────────────────────────────────────────────┤
│  Data Layer                                     │
│  (CSV Files + RAG Engine)                       │
│  • analyzed_properties.csv                      │
│  • Vector Store                                 │
├─────────────────────────────────────────────────┤
│  External Services                              │
│  (Optional)                                     │
│  • Google Gemini API (AI Chat)                  │
│  • FAISS Vector Store                           │
└─────────────────────────────────────────────────┘
```

---

## Request/Response Flow Example

### Example 1: Get Dashboard Data
```
REQUEST (Client → Server):
─────────────────────────
GET /api/dashboard HTTP/1.1
Host: localhost:5000
Accept: application/json

RESPONSE (Server → Client):
──────────────────────────
HTTP/1.1 200 OK
Content-Type: application/json

{
  "success": true,
  "total_properties": 450,
  "buy_recommendations": 245,
  "rent_recommendations": 205,
  "avg_price": 50000000,
  "avg_area": 2500
}

CLIENT PROCESSING:
──────────────────
1. Parse JSON
2. Update DOM elements
3. Initialize charts
4. Display to user
```

### Example 2: Filter Properties
```
REQUEST (Client → Server):
─────────────────────────
GET /api/properties?page=1&per_page=10&city=Delhi&decision=Buy HTTP/1.1

RESPONSE (Server → Client):
──────────────────────────
{
  "success": true,
  "data": [
    {
      "location": "Park Ave",
      "city": "Delhi",
      "price": 5000000,
      "area_sqft": 2500,
      "decision": "Buy",
      ...
    },
    ...
  ],
  "total": 150,
  "page": 1,
  "per_page": 10,
  "total_pages": 15
}

CLIENT PROCESSING:
──────────────────
1. Parse JSON
2. Render table rows
3. Update pagination info
4. Display results
```

---

This architecture ensures:
- ✅ Clean separation of concerns
- ✅ Easy to maintain and extend
- ✅ Scalable design
- ✅ Good performance
- ✅ User-friendly interface
- ✅ Secure data handling
