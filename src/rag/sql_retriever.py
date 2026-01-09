# src/rag/sql_retriever.py

import pandas as pd
from typing import List, Dict, Tuple

CSV_PATH = "data/outputs/analyzed_properties.csv"

try:
    df = pd.read_csv(CSV_PATH)
except:
    df = pd.DataFrame()


def filter_properties(
    location: str = None,
    bhk: int = None,
    budget_min: float = None,
    budget_max: float = None,
    decision: str = None,
    limit: int = 10
) -> Tuple[List[Dict], int]:
    """
    Filter properties based on user criteria.
    
    Returns:
        Tuple[filtered_records (list), total_count (int)]
        - filtered_records: List of matching properties (max `limit` items)
        - total_count: Total matching records (before limit)
    """
    if df.empty:
        return [], 0
    
    result = df.copy()
    
    # Apply location filter
    if location:
        result = result[result["city"].str.lower() == location.lower()]
    
    # Apply BHK filter
    if bhk is not None:
        result = result[result["bhk"] == bhk]
    
    # Apply budget filter (using price column)
    if budget_min is not None:
        result = result[result["price"] >= budget_min]
    
    if budget_max is not None:
        result = result[result["price"] <= budget_max]
    
    # Apply decision filter (for buy vs rent analysis)
    if decision:
        result = result[result["decision"] == decision]
    
    total_count = len(result)
    records = result.head(limit).to_dict(orient="records")
    
    return records, total_count


def get_filtered_analysis_stats(
    location: str = None,
    bhk: int = None,
    budget_min: float = None,
    budget_max: float = None
) -> Dict:
    """
    Get buy vs rent statistics for filtered dataset.
    
    Returns:
        {
            "total": int,
            "buy_count": int,
            "rent_count": int,
            "avg_price": float,
            "avg_wealth_buy": float,
            "avg_wealth_rent": float,
            "filter_description": str
        }
    """
    if df.empty:
        return {
            "total": 0,
            "buy_count": 0,
            "rent_count": 0,
            "avg_price": 0,
            "avg_wealth_buy": 0,
            "avg_wealth_rent": 0,
            "filter_description": "No data available"
        }
    
    result = df.copy()
    
    # Apply filters
    if location:
        result = result[result["city"].str.lower() == location.lower()]
    
    if bhk is not None:
        result = result[result["bhk"] == bhk]
    
    if budget_min is not None:
        result = result[result["price"] >= budget_min]
    
    if budget_max is not None:
        result = result[result["price"] <= budget_max]
    
    # Calculate statistics on FILTERED data only
    total = len(result)
    
    if total == 0:
        return {
            "total": 0,
            "buy_count": 0,
            "rent_count": 0,
            "avg_price": 0,
            "avg_wealth_buy": 0,
            "avg_wealth_rent": 0,
            "filter_description": generate_filter_description(location, bhk, budget_min, budget_max),
            "empty": True
        }
    
    buy_count = len(result[result["decision"] == "Buy"])
    rent_count = len(result[result["decision"] == "Rent"])
    avg_price = result["price"].mean()
    
    # Calculate average wealth outcomes
    avg_wealth_buy = result["wealth_buying"].mean() if "wealth_buying" in result.columns else 0
    avg_wealth_rent = result["wealth_renting"].mean() if "wealth_renting" in result.columns else 0
    
    return {
        "total": total,
        "buy_count": buy_count,
        "rent_count": rent_count,
        "avg_price": avg_price,
        "avg_wealth_buy": avg_wealth_buy,
        "avg_wealth_rent": avg_wealth_rent,
        "buy_percentage": round((buy_count / total * 100), 1) if total > 0 else 0,
        "rent_percentage": round((rent_count / total * 100), 1) if total > 0 else 0,
        "filter_description": generate_filter_description(location, bhk, budget_min, budget_max),
        "empty": False
    }


def generate_filter_description(location: str, bhk: int, budget_min: float, budget_max: float) -> str:
    """Generate human-readable filter description"""
    parts = []
    
    if location:
        parts.append(f"{location}")
    
    if bhk is not None:
        parts.append(f"{bhk} BHK")
    
    if budget_min and budget_max:
        parts.append(f"₹{budget_min/100000:.1f}L - ₹{budget_max/100000:.1f}L")
    elif budget_min:
        parts.append(f"₹{budget_min/100000:.1f}L+")
    elif budget_max:
        parts.append(f"up to ₹{budget_max/100000:.1f}L")
    
    if not parts:
        return "all properties"
    
    return " ".join(parts)

