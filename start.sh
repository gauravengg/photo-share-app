#!/bin/bash

echo "🚀 Smart Photo Share - Quick Start Script"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install it first."
    exit 1
fi

# Check if Node is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install it first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo "✅ Node.js found: $(node --version)"
echo ""

# Backend setup
echo "📦 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo "Initializing database..."
python init_db.py

echo "✅ Backend setup complete!"
echo ""

# Open new terminal for backend
echo "Starting backend server in a new terminal..."
osascript -e 'tell app "Terminal" to do script "cd '$(pwd)' && source venv/bin/activate && python main.py"' 2>/dev/null || \
gnome-terminal -- bash -c "cd $(pwd) && source venv/bin/activate && python main.py; exec bash" 2>/dev/null || \
xterm -e "cd $(pwd) && source venv/bin/activate && python main.py" 2>/dev/null || \
echo "⚠️  Please manually run: cd backend && source venv/bin/activate && python main.py"

cd ..

# Frontend setup
echo "📦 Setting up frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node dependencies..."
    npm install
fi

echo "✅ Frontend setup complete!"
echo ""

# Open new terminal for frontend
echo "Starting frontend server in a new terminal..."
osascript -e 'tell app "Terminal" to do script "cd '$(pwd)' && npm start"' 2>/dev/null || \
gnome-terminal -- bash -c "cd $(pwd) && npm start; exec bash" 2>/dev/null || \
xterm -e "cd $(pwd) && npm start" 2>/dev/null || \
echo "⚠️  Please manually run: cd frontend && npm start"

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Check the terminals for server output."
echo "Press Ctrl+C in each terminal to stop the servers."
echo "=========================================="
