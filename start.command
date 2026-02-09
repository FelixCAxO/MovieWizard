#!/bin/bash

# MovieWizard Starter Script for macOS (Double-clickable)

# Change directory to the script's location
cd "$(dirname "$0")"

# Set Title
echo -ne "\033]0;MovieWizard Starter\007"

clear
echo "=========================================="
echo "   MovieWizard is starting..."
echo "=========================================="
echo

# 1. Open the UI
if [ -f "interface.html" ]; then
    echo "[1/2] Opening Web Interface..."
    open "interface.html"
else
    echo "[!] Error: interface.html not found."
fi

echo
echo "------------------------------------------"
echo "NEXT STEPS:"
echo "1. Enter your TMDb API Key on the webpage."
echo "2. Follow the wizard to find movies."
echo "------------------------------------------"
echo
echo "If you want to use the CLI Bulk Downloader:"
echo "  - Ensure Python is installed."
echo "  - Run: pip install -r requirements.txt"
echo "  - Run: python smart_filter.py"
echo
echo "=========================================="
read -p "Press [Enter] to exit..."
