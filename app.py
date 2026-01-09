"""
Flask application for Real Estate Analyzer frontend
"""
from flask import Flask, render_template, request, jsonify, session
import pandas as pd
import os
import json
from src.Parameters.analyzer import run_analysis
from src.rag.intent_classifier import classify_intent, extract_filters
from src.rag.sql_retriever import filter_properties, get_filtered_analysis_stats

# Session for storing context (location, BHK from previous queries)
conversation_context = {
    "location": None,
    "bhk": None,
    "budget_min": None,
    "budget_max": None
}

# Initialize RAG Engine with fallback
rag_engine = None
rag_available = False

try:
    print("🔁 Initializing RAG resources...")
    from src.rag.rag_engine import RAGEngine
    rag_engine = RAGEngine()
    rag_available = True
    print("✅ RAG Engine initialized successfully")
except ImportError:
    print("⚠️  RAG modules not available - Chat will use basic responses")
    rag_available = False
except Exception as e:
    print(f"⚠️  RAG Engine initialization failed: {str(e)}")
    print("⚠️  Chat will use basic responses instead")
    rag_available = False

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/api/dashboard')
def dashboard():
    """Get dashboard data"""
    try:
        df = pd.read_csv("data/outputs/analyzed_properties.csv")
        
        total_properties = len(df)
        buy_recommendations = len(df[df['decision'] == 'Buy'])
        rent_recommendations = len(df[df['decision'] == 'Rent'])
        
        avg_price = df['price'].mean() if len(df) > 0 else 0
        avg_area = df['area_sqft'].mean() if len(df) > 0 else 0
        
        return jsonify({
            'success': True,
            'total_properties': int(total_properties),
            'buy_recommendations': int(buy_recommendations),
            'rent_recommendations': int(rent_recommendations),
            'avg_price': float(avg_price),
            'avg_area': float(avg_area)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/properties', methods=['GET'])
def get_properties():
    """Get properties with filters"""
    try:
        df = pd.read_csv("data/outputs/analyzed_properties.csv")
        
        # Get filter parameters
        city = request.args.get('city')
        decision = request.args.get('decision')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        
        # Apply filters
        if city and city != 'all':
            df = df[df['city'].str.lower() == city.lower()]
        
        if decision and decision != 'all':
            df = df[df['decision'] == decision]
        
        if min_price:
            df = df[df['price'] >= min_price]
        
        if max_price:
            df = df[df['price'] <= max_price]
        
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        total = len(df)
        start = (page - 1) * per_page
        end = start + per_page
        
        data = df.iloc[start:end].to_dict('records')
        
        # Convert to JSON-serializable format
        for record in data:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                elif isinstance(value, (float, int)):
                    record[key] = float(value)
        
        return jsonify({
            'success': True,
            'data': data,
            'total': int(total),
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Run analysis with custom parameters"""
    try:
        data = request.json
        
        # Extract parameters
        down_payment_percent = data.get('down_payment_percent', 20)
        loan_rate = data.get('loan_rate', 8.5)
        tax_rate = data.get('tax_rate', 20)
        appreciation_rate = data.get('appreciation_rate', 5)
        rent_escalation = data.get('rent_escalation', 5)
        invest_rate = data.get('invest_rate', 10)
        monthly_saving = data.get('monthly_saving', 15000)
        
        # Update analyzer parameters and run
        from src.Parameters.buy_vs_rent import buying_case, renting_case, compare_results
        
        df = pd.read_csv("data/outputs/magicbricks_india_final.csv")
        results = []
        
        def estimate_rent(area_sqft):
            return area_sqft * 20
        
        for _, row in df.iterrows():
            try:
                price = float(row["price_total_inr"])
                area = float(row["area_sqft"])
            except:
                continue
            
            down_payment = (down_payment_percent / 100) * price
            
            buy = buying_case(
                property_price=price,
                down_payment=down_payment,
                loan_rate=loan_rate,
                tax_rate=tax_rate,
                appreciation_rate=appreciation_rate
            )
            
            rent = renting_case(
                initial_rent=estimate_rent(area),
                escalation=rent_escalation,
                down_payment=down_payment,
                invest_rate=invest_rate,
                monthly_saving=monthly_saving
            )
            
            decision = compare_results(buy, rent)
            
            results.append({
                "location": row["location"],
                "city": row["city"],
                "price": price,
                "area_sqft": area,
                "bhk": row["BHK"],
                "price_per_sqft": row["price_per_sqft"],
                "wealth_buying": buy["wealth_buying"],
                "wealth_renting": rent["wealth_renting"],
                "decision": decision
            })
        
        out = pd.DataFrame(results)
        out.to_csv("data/outputs/analyzed_properties.csv", index=False)
        
        return jsonify({
            'success': True,
            'message': 'Analysis completed successfully',
            'total_properties': len(results),
            'buy_count': len([r for r in results if r['decision'] == 'Buy']),
            'rent_count': len([r for r in results if r['decision'] == 'Rent'])
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/city-options')
def city_options():
    """Get available cities"""
    try:
        df = pd.read_csv("data/outputs/analyzed_properties.csv")
        cities = sorted(df['city'].unique().tolist())
        return jsonify({'success': True, 'cities': cities})
    except:
        return jsonify({'success': True, 'cities': []})


@app.route('/api/rag-query', methods=['POST'])
def rag_query():
    """Process RAG query with context memory and filtered analysis"""
    global conversation_context
    try:
        data = request.json
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'success': False, 'error': 'Query is required'})
        
        query_lower = query.lower()
        
        # Use our new filtered response generator
        response = generate_basic_response(query)
        
        # Return response with current context
        return jsonify({
            'success': True,
            'response': response,
            'context': conversation_context
        })
    except Exception as e:
        print(f"Query error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})


def generate_basic_response(query):
    """
    Generate context-aware responses using filtered dataset.
    Remembers location, BHK from previous queries ONLY if user doesn't specify a new one.
    If user provides a new location, it REPLACES the previous one.
    """
    global conversation_context
    
    query_lower = query.lower()
    
    # Step 1: Classify intent
    intent = classify_intent(query)
    
    # Step 2: Extract new filters from query
    new_filters = extract_filters(query)
    
    # Step 3: Update context with smart merging
    # If user mentions a NEW location, it replaces the old one (don't preserve old location)
    # If user doesn't mention location, keep previous context location
    if new_filters["location"] is not None:
        # User explicitly mentioned a location - use it
        conversation_context["location"] = new_filters["location"]
    # else: keep previous location from context
    
    # Same logic for BHK, budget
    if new_filters["bhk"] is not None:
        conversation_context["bhk"] = new_filters["bhk"]
    
    if new_filters["budget_min"] is not None:
        conversation_context["budget_min"] = new_filters["budget_min"]
    
    if new_filters["budget_max"] is not None:
        conversation_context["budget_max"] = new_filters["budget_max"]
    
    # Step 4: Get filtered statistics based on current context
    stats = get_filtered_analysis_stats(
        location=conversation_context["location"],
        bhk=conversation_context["bhk"],
        budget_min=conversation_context["budget_min"],
        budget_max=conversation_context["budget_max"]
    )
    
    # Step 5: Generate response based on intent
    
    # Handle empty results
    if stats.get("empty", False):
        filter_desc = stats["filter_description"]
        return f"I couldn't find any properties matching your criteria ({filter_desc}). Would you like to adjust your filters?"
    
    # BUY VS RENT ANALYSIS
    if intent == "BUY_VS_RENT":
        total = stats["total"]
        buy_count = stats["buy_count"]
        rent_count = stats["rent_count"]
        buy_pct = stats["buy_percentage"]
        rent_pct = stats["rent_percentage"]
        avg_wealth_buy = stats["avg_wealth_buy"]
        avg_wealth_rent = stats["avg_wealth_rent"]
        filter_desc = stats["filter_description"]
        
        if total == 0:
            return f"No properties found for {filter_desc}. Please adjust your filters."
        
        summary = f"For {filter_desc}:\n\n"
        summary += f"📊 Analysis of {total} properties:\n"
        summary += f"  • Buy recommended: {buy_count} properties ({buy_pct}%)\n"
        summary += f"  • Rent recommended: {rent_count} properties ({rent_pct}%)\n\n"
        
        if buy_count > rent_count:
            summary += f"💡 Verdict: Buying is financially better for most properties here.\n"
            summary += f"   Average 20-year wealth (buying): ₹{avg_wealth_buy:,.0f}\n"
            summary += f"   Average 20-year wealth (renting): ₹{avg_wealth_rent:,.0f}\n"
        elif rent_count > buy_count:
            summary += f"💡 Verdict: Renting offers better financial flexibility for most properties here.\n"
            summary += f"   Average 20-year wealth (renting): ₹{avg_wealth_rent:,.0f}\n"
            summary += f"   Average 20-year wealth (buying): ₹{avg_wealth_buy:,.0f}\n"
        else:
            summary += f"💡 Verdict: Both buying and renting are equally viable options.\n"
        
        return summary
    
    # RENT ANALYSIS
    elif intent == "RENT_ANALYSIS":
        total = stats["total"]
        avg_price = stats["avg_price"]
        avg_wealth_rent = stats["avg_wealth_rent"]
        filter_desc = stats["filter_description"]
        
        if total == 0:
            return f"No properties found for {filter_desc}. Please adjust your filters."
        
        summary = f"Rental Analysis for {filter_desc}:\n\n"
        summary += f"📈 {total} properties analyzed\n"
        summary += f"💰 Average price: ₹{avg_price:,.0f}\n"
        summary += f"📊 20-year wealth potential (renting + investing): ₹{avg_wealth_rent:,.0f}\n"
        summary += f"\n✨ Renting provides flexibility and reduced capital lock-in while you invest the down payment.\n"
        
        return summary
    
    # SEARCH PROPERTY
    elif intent == "SEARCH_PROPERTY":
        records, total = filter_properties(
            location=conversation_context["location"],
            bhk=conversation_context["bhk"],
            budget_min=conversation_context["budget_min"],
            budget_max=conversation_context["budget_max"],
            limit=5
        )
        
        filter_desc = stats["filter_description"]
        
        if total == 0:
            return f"No properties found for {filter_desc}. Try adjusting your filters (location, BHK, or budget)."
        
        summary = f"Found {total} properties in {filter_desc}.\n\n"
        
        for i, prop in enumerate(records[:3], 1):
            location = prop.get("location", "N/A")
            price = prop.get("price", 0)
            bhk = prop.get("bhk", "N/A")
            decision = prop.get("decision", "N/A")
            
            summary += f"{i}. {location} - {bhk} BHK\n"
            summary += f"   Price: ₹{price:,.0f} | Recommendation: {decision}\n"
        
        if total > 3:
            summary += f"\n... and {total - 3} more properties.\n"
        
        return summary
    
    # EXPLAIN
    elif intent == "EXPLAIN":
        return "I can explain real estate concepts like:\n• Buy vs Rent analysis\n• EMI calculations\n• Investment returns\n• Rental yields\n\nWhat would you like to understand better?"
    
    # EDUCATIONAL
    elif intent == "EDUCATIONAL":
        return "Real estate investing involves factors like property appreciation, rental income, loan interest, and tax implications. Our analysis helps you determine whether buying or renting makes more financial sense for your specific situation."
    
    # DEFAULT
    else:
        return "I can help with property search, buy vs rent analysis, rental insights, and investment guidance. What would you like to know?"



@app.route('/api/export', methods=['GET'])
def export():
    """Export analyzed properties"""
    try:
        df = pd.read_csv("data/outputs/analyzed_properties.csv")
        
        format_type = request.args.get('format', 'csv')
        
        if format_type == 'json':
            return jsonify({
                'success': True,
                'data': df.to_dict('records')
            })
        else:
            # Return CSV as downloadable
            return df.to_csv(index=False), 200, {'Content-Disposition': 'attachment; filename=properties.csv'}
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.json.get("message")

    docs = vector_db.similarity_search(user_query, k=3)
    context = [d.page_content for d in docs]

    answer = generate_rag_response(context, user_query)

    return jsonify({"reply": answer})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
