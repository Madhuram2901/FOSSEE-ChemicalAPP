# Deployment Guide

This document outlines the steps to deploy the FOSSEE ChemicalAPP to production environments (Railway, Render, AWS, etc.) and harden it for security.

## 🚀 Production Checklist

Before going live, ensure the following:

1.  **Environment Variables**: Never commit `.env` to version control. Set variables in your cloud provider's dashboard.
2.  **Secret Key**: `SECRET_KEY` must be a long, random string.
3.  **Debug Mode**: `DEBUG` must be set to `False`.
4.  **Database**: Use PostgreSQL for production.
5.  **Allowed Hosts**: configure `ALLOWED_HOSTS` to match your domain.

## 🛠 Configuration

The application is configured using environment variables.

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `False` |
| `SECRET_KEY` | Django security key | *(Unsafe default provided)* |
| `ALLOWED_HOSTS` | Comma-separated domains | `*` |
| `DATABASE_URL` | Database connection string | `sqlite:///db.sqlite3` |
| `CORS_ALLOWED_ORIGINS` | Allowed CORS origins | `*` |

### Database Strategy
*   **Strictly SQLite**: The application is configured to use SQLite in all environments (Development & Production).
*   **Persistence**: Ensure that the `db.sqlite3` file is located in a persistent volume if deploying to a containerized environment (like Railway, Render, or Docker), otherwise data will be lost on restart.

## 📦 Deployment (Railway / Render)

1.  **Connect Repository**: Link your GitHub repo.
2.  **Add Services**: Select Python/Django service.
3.  **Set Environment Variables**: Add the variables listed above.
4.  **Persistent Storage (Critical)**:
    *   Add a Volume/Disk to your service.
    *   Mount it to `/app/backend` (or wherever `db.sqlite3` is expected).
    *   Failure to do this will reset the database on every deploy!
5.  **Build Command**:
    ```bash
    pip install -r requirements.txt && python manage.py migrate
    ```
6.  **Start Command**:
    ```bash
    gunicorn equipment_visualizer.wsgi:application
    ```

## ⚠️ Known Limitations & Hardening

*   **Database**: Uses SQLite strictly. Not suitable for high-concurrency write-heavy loads, but perfect for this academic use case.
*   **File Size**: Uploads are strictly limited to **10MB**.
*   **Row Limit**: CSV files cannot exceed **20,000 rows**.
*   **Data Retention**: The system retains only the last **5 datasets** per user (or global anonymous pool) to prevent storage abuse.

## 🔐 Authentication

The system supports **Optional Authentication**:
*   **Anonymous Users**: Can upload and view datasets. Data is shared in a common "anonymous" pool on some endpoints.
*   **Authenticated Users**: Data is private and scoped to the user account.
*   **Desktop App**: Can function in either mode.
