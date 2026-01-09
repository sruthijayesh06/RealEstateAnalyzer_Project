#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify location extraction from user queries
Tests fuzzy matching for spelling variants like trivandrum/thiruvananthapuram
"""

import sys
# Fix encoding for Windows PowerShell
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from src.rag.intent_classifier import extract_filters, classify_intent

test_queries = [
    # Exact matches
    ("Show me properties in Mumbai", "Mumbai"),
    ("Find 2 BHK in Pune", "Pune"),
    ("properties in Trivandrum", "Trivandrum"),
    ("2 BHK in Kochi", "Kochi"),
    ("Hyderabad homes", "Hyderabad"),
    
    # Spelling variants (fuzzy matching)
    ("Properties in thiruvananthapuram", "Trivandrum"),  # Should fuzzy match to Trivandrum
    ("Show me homes in thiruvanantapuram", "Trivandrum"),  # Slightly different spelling
    ("properties in trivandram", "Trivandrum"),  # Missing h
    ("Looking for properties in thane", "Thane"),
    ("New Delhi properties", "New-delhi"),
    
    # Case insensitivity
    ("MUMBAI properties", "Mumbai"),
    ("show me homes in PUNE", "Pune"),
    
    # Combined filters
    ("2 BHK in Mumbai with 50 lakh budget", "Mumbai"),
    ("3 bedroom home in Hyderabad between 50L and 1 crore", "Hyderabad"),  # Changed from Bangalore which is not in CSV
    
    # No location
    ("Show me 2 BHK properties", None),
    ("Buy vs rent analysis", None),
]

print("=" * 70)
print("LOCATION EXTRACTION TEST")
print("=" * 70)

passed = 0
failed = 0

for query, expected_location in test_queries:
    filters = extract_filters(query)
    extracted_location = filters.get("location")
    
    # Match considering case-insensitive comparison
    match = False
    if extracted_location and expected_location:
        match = extracted_location.lower() == expected_location.lower()
    else:
        match = extracted_location == expected_location
    
    status = "[PASS]" if match else "[FAIL]"
    
    if match:
        passed += 1
    else:
        failed += 1
    
    print(f"\n{status}")
    print(f"  Query: {query}")
    print(f"  Expected: {expected_location}")
    print(f"  Got:      {extracted_location}")

print("\n" + "=" * 70)
print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_queries)} tests")
print("=" * 70)

# Additional test: Check that all cities from CSV are recognized
print("\n" + "=" * 70)
print("CSV CITY RECOGNITION TEST")
print("=" * 70)

import pandas as pd

try:
    df = pd.read_csv("data/outputs/analyzed_properties.csv")
    cities = df['city'].unique()
    
    print(f"\nTesting recognition of all {len(cities)} cities from CSV:")
    
    all_recognized = True
    for city in sorted(cities):
        query = f"properties in {city}"
        filters = extract_filters(query)
        recognized = filters.get("location") is not None
        
        if not recognized:
            print(f"  [FAIL]: {city} not recognized")
            all_recognized = False
    
    if all_recognized:
        print(f"  [PASS] All {len(cities)} cities from CSV are recognized!")
    
except Exception as e:
    print(f"  Error loading CSV: {e}")

print("=" * 70)
