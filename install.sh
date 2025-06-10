#!/bin/bash
echo "Installing Rebol 3 Script Analysis Tool..."
echo

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7 or higher"
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "macOS: brew install python3"
    echo "Or download from: https://python.org"
    exit 1
fi

echo "Python version:"
python3 --version

echo
echo "Installing Flask..."
pip3 install flask

echo
echo "Installation complete!"
echo
echo "To run the application:"
echo "  python3 app.py"
echo
echo "Then open your browser to: http://localhost:5000"
echo