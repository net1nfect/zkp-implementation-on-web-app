#!/bin/bash

echo "============================================================"
echo "ZKP Authentication System - Setup and Run"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Go to backend directory
cd backend

# Run the application
echo "============================================================"
echo "Starting ZKP Authentication Server..."
echo "============================================================"
echo ""
echo "Server will be available at: http://localhost:5000"
echo ""
echo "Press CTRL+C to stop the server"
echo ""
python app.py

