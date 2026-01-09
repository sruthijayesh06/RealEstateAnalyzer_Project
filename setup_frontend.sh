#!/bin/bash
# Frontend Setup Script
# This script installs all required dependencies for the frontend

echo "================================"
echo "Real Estate Analyzer - Frontend Setup"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null
then
    echo "❌ Python is not installed. Please install Python 3.11+"
    exit 1
fi

echo "✅ Python found: $(python --version)"
echo ""

# Install/Upgrade pip
echo "📦 Upgrading pip..."
python -m pip install --upgrade pip
echo ""

# Install Flask
echo "📦 Installing Flask..."
pip install Flask>=3.0.0
echo ""

# Install other frontend dependencies (if needed)
echo "📦 Installing other dependencies..."
pip install -r requirements.txt
echo ""

echo "================================"
echo "✅ Frontend Setup Complete!"
echo "================================"
echo ""
echo "To start the application, run:"
echo "  python app.py"
echo ""
echo "Then open your browser to:"
echo "  http://localhost:5000"
echo ""
