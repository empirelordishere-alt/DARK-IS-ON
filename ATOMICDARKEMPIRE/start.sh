#!/bin/bash

echo ""
echo "========================================"
echo "  DARK EMPIRE BOT LAUNCHER"
echo "========================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found!"
    echo ""
    echo "Please create a .env file with:"
    echo "DISCORD_TOKEN=your_token_here"
    echo "OWNER_ID=your_user_id_here"
    echo "PREFIX=!"
    echo ""
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "[1/3] Checking dependencies..."
pip3 install -r requirements.txt --quiet

echo "[2/3] Creating data directory..."
mkdir -p data

echo "[3/3] Starting Dark Empire Bot..."
echo ""
echo "========================================"
echo "  BOT IS STARTING..."
echo "  Press Ctrl+C to stop"
echo "========================================"
echo ""

python3 bot.py
