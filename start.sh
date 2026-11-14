#!/bin/bash

# CAMAS Platform Startup Script
# Starts both frontend and backend for local development

set -e

echo "🚀 CAMAS Platform Startup"
echo "=========================="

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required. Please install Python 3.11+"
    exit 1
fi

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required. Please install Node.js 20+"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "✓ Virtual environment ready"
source .venv/bin/activate

# Install/update Python dependencies
echo "📦 Installing Python dependencies..."
pip install -q -r requirements.txt

# Install/update frontend dependencies
echo "📦 Installing Node.js dependencies..."
cd frontend
npm install --quiet
cd ..

# Create necessary directories
mkdir -p database reports visualizations

# Initialize database
echo "📊 Initializing database..."
python -c "from database.schema import initialize_database; initialize_database('database/camas.db')" 2>/dev/null || true

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Starting CAMAS Platform..."
echo ""
echo "📊 Backend starting on http://localhost:8000"
echo "🎨 Frontend starting on http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start backend in background
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload > /tmp/camas_backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Give backend time to start
sleep 2

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Backend failed to start. Check /tmp/camas_backend.log"
    exit 1
fi

echo "✓ Backend running"

# Start frontend
cd frontend
npm run dev &
FRONTEND_PID=$!
echo "✓ Frontend running"

cd ..

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo ''; echo 'Shutting down...'; exit 0" INT

wait $BACKEND_PID $FRONTEND_PID 2>/dev/null
