# Step-by-Step Deployment Guide: Railway + Vercel

> **Total Time: ~20-30 minutes**

## PART 1: RAILWAY BACKEND DEPLOYMENT (10-15 min)

### Step 1.1: Create Railway Account
```
Go to https://railway.app
↓
Click "Start Project" (top right)
↓
Click "GitHub"
↓
Authorize Railway access to your GitHub
↓
Create Railway account
```

### Step 1.2: Connect Your Repository
```
Railway Dashboard
↓
Click "New Project"
↓
Select "Deploy from GitHub repo"
↓
Search "FOSSEE-ChemicalAPP"
↓
Select your repository
↓
Click "Deploy Now"
```
**⏱️ Wait 2-3 minutes for initial deployment**

### Step 1.3: Add PostgreSQL Database
```
Your Project Page (in Railway)
↓
Click "+ Add" (blue button)
↓
Select "Database" → "PostgreSQL"
↓
Click "Add PostgreSQL"
↓
PostgreSQL service will be created
↓
DATABASE_URL environment variable is automatically set ✓
```

### Step 1.4: Configure Environment Variables

Go to: **Railway Dashboard** → Your Project → **Backend (web service)** → **Variables** tab

Add these variables one by one:

| Variable | Value | How to Get |
|----------|-------|-----------|
| `SECRET_KEY` | Copy from below ⬇️ | Run: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` in your terminal |
| `DEBUG` | `False` | Type exactly as shown |
| `ALLOWED_HOSTS` | `your-project.railway.app` | Replace `your-project` with your Railway project name (see deployment URL) |
| `CORS_ALLOWED_ORIGINS` | `*` | For now, we'll update after Vercel setup |
| `CSRF_TRUSTED_ORIGINS` | `https://*.railway.app` | Type exactly as shown |

**Visual Steps:**
```
Railway Dashboard
  ↓
Click Backend service (the running one)
  ↓
"Variables" tab
  ↓
"Add Variable" button
  ↓
Enter Name: SECRET_KEY
  ↓
Enter Value: (paste your generated key)
  ↓
Click "Add"
  ↓ (Repeat for other variables)
  ↓
Railway will auto-redeploy
```

### Step 1.5: Verify Backend is Working

**Test 1: Check Deployment Status**
```
Railway Dashboard → Backend service
↓
Should see green checkmark ✓
(If red ✗, click "Deployments" and check logs)
```

**Test 2: Test API Endpoint**
```
Open your browser and visit:
https://your-railway-project.railway.app/api/

Should see: {"status": "Backend initialized"}
```

**Save this URL:** `https://________.railway.app`
(You'll need it for Vercel setup)

---

## PART 2: VERCEL FRONTEND DEPLOYMENT (8-10 min)

### Step 2.1: Create Vercel Account
```
Go to https://vercel.com
↓
Click "Sign Up"
↓
Choose "Continue with GitHub"
↓
Authorize Vercel
↓
Create account
```

### Step 2.2: Import Your Repository
```
Vercel Dashboard (after login)
↓
Click "Add New..." → "Project"
↓
Click "Import Git Repository"
↓
Paste: https://github.com/YOUR-USERNAME/FOSSEE-ChemicalAPP
↓
Click "Import"
```

### Step 2.3: Configure Build Settings
**Important:** On the "Configure Project" screen, set:

```
Framework Preset: Vite ← SELECT THIS
Root Directory: frontend-web ← CLICK THIS AND SELECT
Build Command: npm run build ← Should be auto-filled
Output Directory: dist ← Should be auto-filled
Install Command: npm ci ← Should be auto-filled
Environment Variables: (Set next in Step 2.4)
```

### Step 2.4: Add Environment Variables
```
After clicking "Deploy", wait for project to be created
↓
Go to Settings → Environment Variables
↓
Click "Add New"
↓
Name: VITE_API_URL
Value: https://your-railway-backend.railway.app/api
↓
Click "Add"
↓
Click "Redeploy" button to redeploy with new env var
```

**⏱️ Wait 2-3 minutes for build and deployment**

### Step 2.5: Verify Frontend is Working

**Test 1: Check Deployment Status**
```
Vercel Dashboard
  ↓
Click your project
  ↓
Should see "Deployed" status
```

**Test 2: Visit Your Site**
```
Click the deployment URL (or copy from top)
↓
You should see the login page
↓
Check browser console (F12) for errors - should be none
```

**Save this URL:** `https://________.vercel.app`

---

## PART 3: CONNECT SERVICES (Update Railway with Vercel URL)

### Step 3.1: Update Railway Environment Variables

Go back to: **Railway Dashboard** → **Backend service** → **Variables**

Update:
- `CORS_ALLOWED_ORIGINS`: Change `*` to `https://your-vercel-url.vercel.app`
- `CSRF_TRUSTED_ORIGINS`: Add your Vercel URL

```
Before:
CORS_ALLOWED_ORIGINS = *
CSRF_TRUSTED_ORIGINS = https://*.railway.app

After:
CORS_ALLOWED_ORIGINS = https://your-vercel-url.vercel.app
CSRF_TRUSTED_ORIGINS = https://your-vercel-url.vercel.app,https://*.railway.app
```

**Railway will auto-redeploy** ✓

---

## PART 4: FINAL TESTING

### Test 4.1: Check Backend API
```
Open your browser and visit:
https://your-railway-backend.railway.app/api/

Should see: {"status": "Backend initialized"}
```

### Test 4.2: Test Frontend
```
Visit: https://your-vercel-url.vercel.app

Check for:
✓ Login page loads without styling issues
✓ No errors in browser console (F12)
✓ Can create an account
✓ Can log in
✓ Can upload a CSV file
✓ Can see the dashboard with data
```

### Test 4.3: Verify API Connection
```
In browser console (F12 → Console tab), paste:
fetch('https://your-railway-backend.railway.app/api/')
  .then(r => r.json())
  .then(d => console.log('✓ Backend Connected:', d))
  .catch(e => console.error('✗ Backend Error:', e))

Should see: ✓ Backend Connected: {status: 'Backend initialized'}
```

---

## QUICK REFERENCE

### Your Deployed URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Backend API | `https://your-railway-project.railway.app/api/` | API endpoints |
| Admin Panel | `https://your-railway-project.railway.app/admin/` | Django admin |
| Frontend | `https://your-vercel-project.vercel.app/` | User interface |

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "CORS error" in console | Check `CORS_ALLOWED_ORIGINS` includes Vercel URL |
| "API endpoint not found" | Verify Railway URL ends with `/api` |
| "502 Bad Gateway" | Check Railway deployment logs |
| "CSS looks broken" | Clear browser cache (Ctrl+Shift+Delete) |
| "Login doesn't work" | Check backend logs for authentication errors |

---

## MONITORING AFTER DEPLOYMENT

### Check Railway Logs
```
Railway Dashboard
  ↓
Backend service
  ↓
"Deployments" tab
  ↓
Click latest deployment
  ↓
"View Logs" button
```

### Check Vercel Logs
```
Vercel Dashboard
  ↓
Your project
  ↓
"Deployments" tab
  ↓
Click latest deployment
  ↓
Logs display automatically
```

### Enable Error Notifications
```
Railway:
  Settings → Alerts (add email)

Vercel:
  Settings → Notifications (add email)
```

---

## 🎉 YOU'RE DONE!

Your application is now deployed:
- ✅ Backend running on Railway
- ✅ Frontend running on Vercel
- ✅ Both services connected
- ✅ Ready for production use

Share your URLs:
```
Frontend: https://your-vercel-project.vercel.app/
Backend API: https://your-railway-project.railway.app/api/
```

