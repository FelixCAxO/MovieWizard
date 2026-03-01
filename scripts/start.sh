#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR/.."

echo "=========================================="
echo "          MovieWizard Launcher"
echo "=========================================="
echo ""
echo "[1] Launch Web Interface (Local Server)"
echo "[2] Launch Deep Search CLI (Terminal)"
echo ""
read -p "Select an option (1-2): " choice

if [ "$choice" == "1" ]; then
    echo "Starting local server at http://localhost:8000..."
    # Attempt to open browser based on OS
    if command -v xdg-open > /dev/null; then
        xdg-open "http://localhost:8000/interface.html"
    elif command -v open > /dev/null; then
        open "http://localhost:8000/interface.html"
    fi
    python3 -m http.server 8000
elif [ "$choice" == "2" ]; then
    python3 -m src.app.cli
else
    echo "Invalid choice."
fi
