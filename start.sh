#!/bin/bash

# Start Cinematic Video Studio v2
# FastAPI backend + React frontend

echo "🌍 Starting Calm Meridian Studio..."

# Start backend
echo "📡 Starting FastAPI backend on port 3011..."
cd backend
source venv/bin/activate
nohup venv/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 3011 > /tmp/cvs-backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"
cd ..

# Wait for backend
sleep 3

# Start frontend
echo "🖥️ Starting React frontend on port 3012..."
cd frontend
nohup npm run dev > /tmp/cvs-frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"
cd ..

echo ""
echo "✅ Services started!"
echo ""
echo "📡 Backend API: http://192.168.29.56:3011"
echo "🖥️ Frontend UI: http://192.168.29.56:3012"
echo ""
echo "Logs:"
echo "  Backend:  tail -f /tmp/cvs-backend.log"
echo "  Frontend: tail -f /tmp/cvs-frontend.log"
