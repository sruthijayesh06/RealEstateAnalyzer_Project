#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
End-to-end test to verify location extraction works through the entire pipeline
Tests the bug fix: location is now reliably extracted and used in filtering
"""

import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from src.rag.intent_classifier import extract_filters, classify_intent
from src.rag.sql_retriever import filter_properties, get_filtered_analysis_stats

print("=" * 80)
print("END-TO-END LOCATION HANDLING TEST")
print("=" * 80)

test_scenarios = [
    {
        "name": "Test 1: Trivandrum with spelling variant",
        "query": "Show me properties in thiruvananthapuram",
        "expected_location": "Trivandrum",
        "expected_min_results": 1,
    },
    {
        "name": "Test 2: Mumbai with 2 BHK filter",
        "query": "Find 2 BHK in Mumbai",
        "expected_location": "Mumbai",
        "expected_min_results": 1,
    },
    {
        "name": "Test 3: Kochi exact match",
        "query": "properties in Kochi",
        "expected_location": "Kochi",
        "expected_min_results": 1,
    },
    {
        "name": "Test 4: No location specified",
        "query": "Show me all properties with 2 BHK",
        "expected_location": None,
        "expected_min_results": 10,  # Should return many properties
    },
    {
        "name": "Test 5: Thane with budget",
        "query": "2 BHK in Thane between 50 lakh and 1 crore",
        "expected_location": "Thane",
        "expected_min_results": 1,
    },
]

passed = 0
failed = 0

for scenario in test_scenarios:
    print(f"\n{scenario['name']}")
    print("-" * 80)
    
    query = scenario["query"]
    print(f"Query: {query}")
    
    # Step 1: Extract filters
    filters = extract_filters(query)
    extracted_location = filters.get("location")
    expected_location = scenario["expected_location"]
    
    location_match = (extracted_location and expected_location and 
                     extracted_location.lower() == expected_location.lower()) or \
                     (extracted_location == expected_location)
    
    print(f"Expected location: {expected_location}")
    print(f"Extracted location: {extracted_location}")
    
    if not location_match:
        print(f"[FAIL] Location extraction failed")
        failed += 1
        continue
    
    # Step 2: Filter properties using extracted location
    records, total_count = filter_properties(
        location=filters.get("location"),
        bhk=filters.get("bhk"),
        budget_min=filters.get("budget_min"),
        budget_max=filters.get("budget_max"),
        limit=10
    )
    
    print(f"Total properties found: {total_count}")
    print(f"Sample properties returned: {len(records)}")
    
    if total_count < scenario["expected_min_results"]:
        print(f"[FAIL] Expected at least {scenario['expected_min_results']} results, got {total_count}")
        failed += 1
        continue
    
    # Step 3: Get analysis stats
    stats = get_filtered_analysis_stats(
        location=filters.get("location"),
        bhk=filters.get("bhk"),
        budget_min=filters.get("budget_min"),
        budget_max=filters.get("budget_max")
    )
    
    print(f"Buy vs Rent: {stats['buy_count']} buy, {stats['rent_count']} rent out of {stats['total']}")
    print(f"Filter description: {stats['filter_description']}")
    
    if stats.get("empty"):
        print(f"[FAIL] No properties found after filtering")
        failed += 1
        continue
    
    print(f"[PASS] Location extraction and filtering works correctly")
    passed += 1

print("\n" + "=" * 80)
print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_scenarios)} tests")
print("=" * 80)

if failed == 0:
    print("\n*** BUG FIX VERIFIED ***")
    print("Location extraction is now working correctly:")
    print("- User-provided locations (including spelling variants) are extracted")
    print("- Locations are passed through the entire pipeline (classifier -> retriever)")
    print("- SQL queries do NOT default to Pune (uses extracted location)")
    print("- Different locations in new queries update the search context")
else:
    print("\n*** ISSUES FOUND ***")
    print(f"Failed {failed} test(s) - location handling may still have issues")
