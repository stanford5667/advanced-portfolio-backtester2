#!/bin/bash

# Advanced Portfolio Backtester Installation Script
echo "🚀 Installing Advanced Portfolio Backtester..."

# Check if Python 3.9+ is installed
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✅ Python $python_version detected (>= $required_version required)"
else
    echo "❌ Python $python_version detected. Please install Python 3.9 or higher."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Install the package in development mode
echo "🔨 Installing package in development mode..."
pip install -e .

echo ""
echo "✅ Installation completed successfully!"
echo ""
echo "🎯 Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the basic example: python examples/basic_example.py"
echo "3. Or use the CLI: python -m src.main sample"
echo ""
echo "📖 For more information, see the README.md file" 