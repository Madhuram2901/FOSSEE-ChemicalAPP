#!/bin/bash

# Quick deployment preparation script for Linux/Mac

echo "========================================"
echo "Chemical Equipment Visualizer - Deployment Prep"
echo "========================================"
echo ""

# Check if directories exist
if [ ! -d "backend" ]; then
    echo "ERROR: backend directory not found!"
    exit 1
fi

if [ ! -d "frontend-web" ]; then
    echo "ERROR: frontend-web directory not found!"
    exit 1
fi

# Backend preparation
echo ""
echo "[1/3] Installing backend dependencies..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
echo "Backend dependencies installed ✓"

# Frontend preparation
echo ""
echo "[2/3] Installing frontend dependencies..."
cd ../frontend-web
npm install
echo "Frontend dependencies installed ✓"

# Create environment files
echo ""
echo "[3/3] Creating environment file templates..."
cd ..

if [ ! -f "backend/.env" ]; then
    echo "Creating backend/.env template..."
    cat > backend/.env << EOF
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:5173
CSRF_TRUSTED_ORIGINS=http://localhost:5173
EOF
    echo "backend/.env created ✓"
fi

if [ ! -f "frontend-web/.env.local" ]; then
    echo "Creating frontend-web/.env.local template..."
    cat > frontend-web/.env.local << EOF
VITE_API_URL=http://localhost:8000/api
EOF
    echo "frontend-web/.env.local created ✓"
fi

echo ""
echo "========================================"
echo "Deployment Preparation Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Commit all changes: git add . && git commit -m 'Deployment setup'"
echo "2. Push to GitHub: git push origin main"
echo "3. Follow DEPLOYMENT_GUIDE.md for Railway and Vercel setup"
echo ""
echo "To run locally:"
echo "  Backend:  cd backend && source venv/bin/activate && python manage.py runserver"
echo "  Frontend: cd frontend-web && npm run dev"
echo ""
