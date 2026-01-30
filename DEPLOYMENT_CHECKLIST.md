# Deployment Checklist

## Pre-Deployment (Local Testing)

- [ ] Backend runs locally: `python manage.py runserver`
- [ ] Frontend runs locally: `npm run dev`
- [ ] Production build works: `npm run build`
- [ ] No errors in browser console
- [ ] API endpoints respond correctly

## Railway Backend Setup

- [ ] Create Railway account at [railway.app](https://railway.app)
- [ ] Connect GitHub repository
- [ ] Create new project from GitHub
- [ ] Add PostgreSQL database
- [ ] Generate SECRET_KEY:
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
- [ ] Set environment variables:
  - [ ] `SECRET_KEY` = (generated key)
  - [ ] `DEBUG` = `False`
  - [ ] `ALLOWED_HOSTS` = `your-railway-url.railway.app`
  - [ ] `CORS_ALLOWED_ORIGINS` = (will add after Vercel deployment)
  - [ ] `CSRF_TRUSTED_ORIGINS` = (will add after Vercel deployment)
- [ ] Backend deploys successfully (green checkmark)
- [ ] Test API: `curl https://your-railway-url.railway.app/api/`
- [ ] Note down Railway URL for next step

## Vercel Frontend Setup

- [ ] Create Vercel account at [vercel.com](https://vercel.com)
- [ ] Connect GitHub repository
- [ ] Import project with correct Root Directory: `frontend-web`
- [ ] Configure build settings:
  - [ ] Framework: Vite
  - [ ] Build Command: `npm run build`
  - [ ] Output Directory: `dist`
- [ ] Set environment variables:
  - [ ] `VITE_API_URL` = `https://your-railway-backend.railway.app/api`
- [ ] Frontend deploys successfully
- [ ] Note down Vercel URL for next step

## Post-Deployment Configuration

- [ ] Update Railway environment variables with Vercel URL:
  - [ ] `CORS_ALLOWED_ORIGINS` = `https://your-vercel-url.vercel.app`
  - [ ] `CSRF_TRUSTED_ORIGINS` = `https://your-vercel-url.vercel.app,https://*.railway.app`
- [ ] Redeploy Railway backend
- [ ] Redeploy Vercel frontend

## Testing

- [ ] Frontend loads without errors
- [ ] Login page displays correctly
- [ ] Registration works
- [ ] Can upload CSV file
- [ ] Charts and data display
- [ ] Browser console has no errors (F12)
- [ ] API calls show 200/201 status codes

## Monitoring

- [ ] Set up Railway alerts for errors
- [ ] Monitor Vercel analytics
- [ ] Check logs regularly for issues
- [ ] Test endpoints periodically

## URLs to Save

- Backend API: `https://______.railway.app/api/`
- Admin Panel: `https://______.railway.app/admin/`
- Frontend: `https://______.vercel.app/`

## Troubleshooting Checklist

If something breaks:
- [ ] Check Railway deployment logs
- [ ] Check Vercel deployment logs
- [ ] Verify environment variables match between services
- [ ] Test backend API directly in browser
- [ ] Check CORS configuration
- [ ] Restart services if needed

