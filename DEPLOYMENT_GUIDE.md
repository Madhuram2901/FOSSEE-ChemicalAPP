# Complete Deployment Guide: Railway (Backend) + Vercel (Frontend)

## Table of Contents
1. [Railway Backend Deployment](#railway-backend-deployment)
2. [Vercel Frontend Deployment](#vercel-frontend-deployment)
3. [Environment Configuration](#environment-configuration)
4. [Post-Deployment Testing](#post-deployment-testing)
5. [Troubleshooting](#troubleshooting)

---

## RAILWAY Backend Deployment

### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Click "Start Project"
3. Sign up with GitHub (recommended for auto-deployment)
4. Authorize Railway to access your GitHub account

### Step 2: Create New Railway Project
1. In Railway dashboard, click "New Project"
2. Select "Deploy from GitHub repo"
3. Search and select your `FOSSEE-ChemicalAPP` repository
4. Click "Deploy Now"

### Step 3: Add PostgreSQL Database
1. In your Railway project, click "+ Add"
2. Click "Database" → "PostgreSQL"
3. Select the PostgreSQL service
4. The `DATABASE_URL` environment variable is **automatically created**

### Step 4: Configure Environment Variables
1. In Railway dashboard → your project
2. Click on the "Backend" (web service)
3. Go to "Variables" tab
4. Add these environment variables:

```
SECRET_KEY = (generate a secure key - see next step)
DEBUG = False
ALLOWED_HOSTS = your-project-name.railway.app
CORS_ALLOWED_ORIGINS = https://your-vercel-url.vercel.app
CSRF_TRUSTED_ORIGINS = https://your-vercel-url.vercel.app,https://*.railway.app
```

**To generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 5: Verify Deployment
1. Click the "Backend" service
2. Go to "Deployments" tab
3. Wait for deployment to complete (green checkmark)
4. Click "View Logs" to verify:
   - `Running on <URL>`
   - No database connection errors
   - Migrations applied successfully

5. Test API endpoint:
```bash
curl https://your-railway-url.railway.app/api/
```

Should return:
```json
{"status": "Backend initialized"}
```

---

## VERCEL Frontend Deployment

### Step 1: Create Vercel Account
1. Go to [vercel.com](https://vercel.com)
2. Click "Sign Up"
3. Choose "GitHub" authentication
4. Authorize Vercel to access your GitHub

### Step 2: Import Repository
1. In Vercel dashboard, click "Add New..." → "Project"
2. Click "Import Git Repository"
3. Paste: `https://github.com/YOUR-USERNAME/FOSSEE-ChemicalAPP`
4. Click "Import"

### Step 3: Configure Build Settings
When prompted with build configuration:
- **Project Name**: `chemical-equipment-visualizer-web`
- **Framework**: `Vite`
- **Root Directory**: `frontend-web` ← **IMPORTANT**
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm ci`

Click "Deploy" to continue.

### Step 4: Add Environment Variables
1. After project creation, go to "Settings" → "Environment Variables"
2. Add:
   ```
   VITE_API_URL = https://your-railway-backend.railway.app/api
   ```
3. Click "Add" and then "Redeploy"

**To find your Railway backend URL:**
- Go to Railway dashboard
- Click your backend service
- Look for "URL" section at the top
- Copy the full URL (e.g., `https://equipment-api-prod.railway.app`)

### Step 5: Verify Deployment
1. Vercel will automatically deploy
2. Wait for "Deployment Complete" message
3. Click the deployment URL
4. Check browser console (F12 → Console) for any API errors
5. Test login/signup functionality

---

## Environment Configuration

### Backend Environment Variables (Railway)

| Variable | Value | Notes |
|----------|-------|-------|
| `SECRET_KEY` | Generated | Use `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | `False` | Never set to True in production |
| `ALLOWED_HOSTS` | `your-project.railway.app` | Replace with actual Railway URL |
| `DATABASE_URL` | Auto-set by PostgreSQL | Don't modify - Railway sets this |
| `CORS_ALLOWED_ORIGINS` | `https://your-vercel-url.vercel.app` | Replace with Vercel URL |
| `CSRF_TRUSTED_ORIGINS` | `https://your-vercel-url.vercel.app,https://*.railway.app` | Both origins |

### Frontend Environment Variables (Vercel)

| Variable | Value | Notes |
|----------|-------|-------|
| `VITE_API_URL` | `https://your-railway-backend.railway.app/api` | Must end with `/api` |

### Local Testing (.env files)

**Backend `backend/.env`:**
```
SECRET_KEY=your-local-test-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:5173
CSRF_TRUSTED_ORIGINS=http://localhost:5173
```

**Frontend `frontend-web/.env.local`:**
```
VITE_API_URL=http://localhost:8000/api
```

---

## Post-Deployment Testing

### 1. Test Backend API
```bash
# Check if backend is running
curl https://your-railway-backend.railway.app/api/

# Should return:
# {"status": "Backend initialized"}

# Test user registration
curl -X POST https://your-railway-backend.railway.app/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@test.com","password":"testpass123"}'
```

### 2. Test Frontend
1. Open your Vercel deployment URL
2. See login page loads correctly
3. Try to register a new account
4. Upload a CSV file
5. View the dashboard with data

### 3. Check Browser Console
Press `F12` in browser → "Console" tab
- Should see NO errors
- API requests should show 200 status
- Charts should render without warnings

### 4. Test API Connectivity
In browser console, run:
```javascript
fetch('https://your-railway-backend.railway.app/api/')
  .then(r => r.json())
  .then(d => console.log('Backend OK:', d))
  .catch(e => console.error('Backend Error:', e))
```

---

## Troubleshooting

### Issue: "CORS error" on Vercel

**Solution:**
1. Check `CORS_ALLOWED_ORIGINS` in Railway includes your Vercel URL
2. Check Vercel's `VITE_API_URL` has correct backend URL
3. Redeploy both services after updating variables

### Issue: "404 Not Found" from API

**Solution:**
1. Verify API URL ends with `/api`
2. Check Railway backend is actually deployed (green checkmark)
3. Test backend URL directly in browser

### Issue: "502 Bad Gateway" from Railway

**Solution:**
1. Check Railway deployment logs for errors
2. Run migrations: `railway run python manage.py migrate`
3. Check environment variables are set correctly
4. Restart the service: Railway dashboard → Backend → Actions → Restart

### Issue: Static files not loading (CSS/Images broken)

**Solution:**
1. This is usually on backend - check `STATIC_ROOT` configuration
2. Run: `railway run python manage.py collectstatic --noinput`
3. Restart backend service

### Issue: "Secret key not set" error

**Solution:**
1. Generate new secret key:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
2. Add to Railway environment variables
3. Redeploy

### Issue: Database migrations not running

**Solution:**
1. In Railway, click Backend service
2. Click "Shell" tab
3. Run: `python manage.py migrate`
4. Check for errors in output

---

## Quick Reference URLs

After deployment, you'll have:

- **Backend API**: `https://your-project-name.railway.app/api/`
- **Admin Panel**: `https://your-project-name.railway.app/admin/`
- **Frontend**: `https://chemical-equipment-visualizer.vercel.app/`

---

## Monitoring & Logs

### View Railway Logs
1. Railway dashboard → Backend service
2. "Deployments" tab → click latest
3. "View Logs" button

### View Vercel Logs
1. Vercel dashboard → Project
2. "Deployments" tab → click latest
3. Logs auto-display

### Real-time Monitoring
- Railway: Dashboard shows CPU, Memory, Bandwidth
- Vercel: Shows build times, analytics, errors

---

## Next Steps

1. ✅ Deploy backend to Railway
2. ✅ Deploy frontend to Vercel
3. ✅ Test API connectivity
4. ✅ Monitor logs for issues
5. Share your deployed URLs:
   - Backend: `https://your-railway-url.railway.app/api/`
   - Frontend: `https://your-vercel-url.vercel.app/`

