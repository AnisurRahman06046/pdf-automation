#!/bin/bash

echo "========================================"
echo "PDF Automation - Test Runner"
echo "========================================"

# Check if server is running
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "ERROR: Server is not running!"
    echo "Start it with: uvicorn app.main:app --reload"
    exit 1
fi

echo "Server is running."

# Generate demo files
echo ""
echo "Generating demo files..."
python scripts/generate_demo_pdf.py
python scripts/generate_demo_image.py

# Run tests
echo ""
echo "Running API tests..."
python scripts/test_api.py
