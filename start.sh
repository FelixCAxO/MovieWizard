#!/bin/bash

# MovieWizard Starter Script for macOS and Linux

# Set Title (Compatible terminals)
echo -ne "\033]0;MovieWizard Starter\007"

clear
echo "=========================================="
echo "   🧙‍♂️ MovieWizard is starting..."
echo "=========================================="
echo

# 1. Open the UI
if [ -f "interface.html" ]; then
    echo "[1/2] Opening Web Interface..."
    
    # Check OS to use correct open command
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "interface.html"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v xdg-open > /dev/null; then
            xdg-open "interface.html"
        else
            echo "[!] Could not detect a browser launcher (xdg-open). Please open interface.html manually."
        fi
    else
        echo "[!] Unsupported OS. Please open interface.html manually."
    fi
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
