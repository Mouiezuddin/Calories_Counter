#!/bin/bash

# NutriCore Setup Script for macOS/Linux

echo "🍎 NutriCore Calorie Tracker - Setup"
echo "===================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✓ Virtual environment created"
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "✓ Virtual environment activated"
echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✓ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created (update with your settings if needed)"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the app, run:"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "Then visit: http://localhost:5000"
