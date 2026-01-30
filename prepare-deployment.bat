@echo off
REM Quick deployment preparation script for Windows

echo ===============================================
echo Chemical Equipment Visualizer - Deployment Prep
echo ===============================================
echo.

REM Check if directories exist
if not exist "backend" (
    echo ERROR: backend directory not found!
    pause
    exit /b 1
)

if not exist "frontend-web" (
    echo ERROR: frontend-web directory not found!
    pause
    exit /b 1
)

REM Backend preparation
echo.
echo [1/3] Installing backend dependencies...
cd backend
if not exist "venv" (
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -r requirements.txt
echo Backend dependencies installed ✓

REM Frontend preparation
echo.
echo [2/3] Installing frontend dependencies...
cd ..\frontend-web
call npm install
echo Frontend dependencies installed ✓

REM Create environment files
echo.
echo [3/3] Creating environment file templates...
cd ..

if not exist "backend\.env" (
    echo Creating backend\.env template...
    (
        echo SECRET_KEY=your-secret-key
        echo DEBUG=True
        echo ALLOWED_HOSTS=localhost,127.0.0.1
        echo DATABASE_URL=sqlite:///db.sqlite3
        echo CORS_ALLOWED_ORIGINS=http://localhost:5173
        echo CSRF_TRUSTED_ORIGINS=http://localhost:5173
    ) > backend\.env
    echo backend\.env created ✓
)

if not exist "frontend-web\.env.local" (
    echo Creating frontend-web\.env.local template...
    (
        echo VITE_API_URL=http://localhost:8000/api
    ) > frontend-web\.env.local
    echo frontend-web\.env.local created ✓
)

echo.
echo ===============================================
echo Deployment Preparation Complete!
echo ===============================================
echo.
echo Next steps:
echo 1. Commit all changes: git add . && git commit -m "Deployment setup"
echo 2. Push to GitHub: git push origin main
echo 3. Follow DEPLOYMENT_GUIDE.md for Railway and Vercel setup
echo.
echo To run locally:
echo   Backend:  cd backend && venv\Scripts\activate && python manage.py runserver
echo   Frontend: cd frontend-web && npm run dev
echo.
pause
