#!/bin/bash
# Cartographer AI — Start both backend and frontend
ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "Starting Cartographer AI..."

# Start backend
export PYTHONPATH="$ROOT"
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "Backend started (PID $BACKEND_PID) at http://localhost:8000"

# Start frontend
cd "$ROOT/frontend"
npm run dev &
FRONTEND_PID=$!
echo "Frontend starting at http://localhost:3000"

echo ""
echo "Press Ctrl+C to stop both servers."
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
