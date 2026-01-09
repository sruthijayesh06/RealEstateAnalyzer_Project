# src/rag/intent_classifier.py
import re
import pandas as pd
from difflib import get_close_matches

INTENTS = {"SEARCH_PROPERTY", "BUY_VS_RENT", "RENT_ANALYSIS", "EXPLAIN", "EDUCATIONAL"}

# Known spelling variants for cities (when similarity matching isn't enough)
CITY_ALIASES = {
    "thiruvananthapuram": "trivandrum",
    "thiruvanantapuram": "trivandrum",
    "bengaluru": "bangalore",  # Note: not in our data, but good for future
}

# Load available cities from CSV (dynamic, not hardcoded)
_available_cities = set()
try:
    _csv_path = "data/outputs/analyzed_properties.csv"
    _df = pd.read_csv(_csv_path)
    _available_cities = set(_df['city'].unique().lower())
except:
    # Fallback list if CSV loading fails
    _available_cities = {
        "mumbai", "thane", "navi-mumbai", "pune", "new-delhi", "noida", "gurgaon",
        "jaipur", "udaipur", "ahmedabad", "surat", "vadodara", "indore", "bhopal",
        "lucknow", "kanpur", "patna", "gaya", "kolkata", "bhubaneswar", "cuttack",
        "ranchi", "jamshedpur", "raipur", "bilaspur", "nagpur", "nashik", "aurangabad",
        "mysore", "chennai", "coimbatore", "hyderabad", "kochi", "trivandrum",
        "thrissur", "kottayam"
    }


def _find_location_in_query(query: str) -> str:
    """
    Extract location from query using intelligent matching.
    Priority: Known aliases > Exact substring > Fuzzy match for long words.
    Handles spelling variants (e.g., trivandrum, thiruvananthapuram).
    
    Returns:
        Location name (capitalized) or None if not found
    """
    query_lower = query.lower()
    
    # Step 1: Check for known spelling variants first
    for alias, standard_city in CITY_ALIASES.items():
        if alias in query_lower and standard_city in _available_cities:
            return standard_city.capitalize()
    
    # Step 2: Direct exact match
    for city in _available_cities:
        if city in query_lower:
            return city.capitalize()
    
    # Step 3: Fuzzy match for spelling variants
    # Extract words that might be city names (length > 4, not common words)
    common_words = {"in", "of", "the", "and", "for", "is", "bhk", "properties", "homes", "house", 
                    "property", "with", "between", "from", "to", "at", "near", "around", "show", 
                    "find", "looking", "search", "want", "need", "bedroom", "bedrooms", "budget",
                    "1l", "50l", "1cr", "10cr"}
    
    words = query_lower.split()
    
    # Try longer words first (more likely to be city names)
    words_sorted = sorted(words, key=len, reverse=True)
    
    for word in words_sorted:
        # Clean punctuation
        word_clean = word.strip(',.!?;:')
        
        # Skip common words and very short words
        if len(word_clean) < 4 or word_clean in common_words:
            continue
        
        # Find close matches
        matches = get_close_matches(word_clean, _available_cities, n=1, cutoff=0.60)
        if matches:
            return matches[0].capitalize()
    
    return None


def classify_intent(query: str) -> str:
    """
    Classify user intent from query.
    Enhanced to distinguish between search, buy_vs_rent, and rent_analysis.
    """
    q = query.lower()

    # Buy vs Rent comparison
    if any(phrase in q for phrase in ["buy vs rent", "should i buy", "should i rent", "better to buy", "better to rent", "buy or rent"]):
        return "BUY_VS_RENT"
    
    # Rent analysis
    if any(phrase in q for phrase in ["rent analysis", "renting option", "rental income", "rental yield"]):
        return "RENT_ANALYSIS"
    
    # Search/Filter properties
    if any(phrase in q for phrase in ["show me", "find", "search", "properties in", "bhk", "budget", "price range", "location"]):
        return "SEARCH_PROPERTY"
    
    # Explanations
    if any(word in q for word in ["why", "explain", "how does"]):
        return "EXPLAIN"
    
    # Educational content
    if any(word in q for word in ["what is", "tell me about", "information about"]):
        return "EDUCATIONAL"

    return "SEARCH_PROPERTY"  # Default to search


def extract_filters(query: str) -> dict:
    """
    Extract structured filters from user query.
    Uses fuzzy matching to handle spelling variants (e.g., trivandrum, thiruvananthapuram).
    
    Returns: {location: str, bhk: int, budget_min: float, budget_max: float}
    """
    filters = {
        "location": None,
        "bhk": None,
        "budget_min": None,
        "budget_max": None
    }
    
    q = query.lower()
    
    # Extract location using fuzzy matching (handles spelling variants)
    filters["location"] = _find_location_in_query(q)
    
    # Extract BHK
    bhk_match = re.search(r'(\d+)\s*(?:bhk|bedroom|bed)', q)
    if bhk_match:
        filters["bhk"] = int(bhk_match.group(1))
    
    # Extract budget (handle variations like "10 lakh", "10L", "1000000", "10-15 lakh")
    budget_pattern = r'(?:₹|rs\.?|budget|price)\s*(?:of\s+)?(\d+(?:[,\.]?\d{3})*)\s*(?:lakh|l|crore|cr)?'
    budget_matches = re.findall(budget_pattern, q)
    
    if budget_matches:
        # Convert lakh/crore to actual numbers
        budgets = []
        for match in budget_matches:
            num = int(match.replace(',', '').replace('.', ''))
            # If "lakh" or "l" in query, multiply by 100000
            if 'lakh' in q or re.search(r'\bl\b', q):
                num *= 100000
            # If "crore" in query, multiply by 10000000
            if 'crore' in q:
                num *= 10000000
            budgets.append(num)
        
        if budgets:
            filters["budget_min"] = min(budgets)
            filters["budget_max"] = max(budgets)
    
    return filters
