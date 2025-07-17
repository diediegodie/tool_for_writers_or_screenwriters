#!/bin/bash

# Writer Tool Backend Setup Script
# This script sets up the Python virtual environment and installs dependencies

echo "🚀 Setting up Writer Tool Backend..."

# Check if Python 3.11+ is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📄 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️ Please edit .env file with your actual configuration values"
fi

echo "✅ Backend setup complete!"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "source venv/bin/activate"
echo ""
echo "To start the development server:"
echo "python run.py"
echo ""
echo "To run with Docker:"
echo "docker-compose up --build"
