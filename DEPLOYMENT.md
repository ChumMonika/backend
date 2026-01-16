# DigitalOcean App Platform Deployment Guide

## 🚀 Step-by-Step Deployment Instructions

### **Prerequisites**
1. DigitalOcean account
2. GitHub repository with this code pushed
3. PostgreSQL database (DigitalOcean Managed Database recommended)

---

## **Step 1: Create PostgreSQL Database**

1. Go to DigitalOcean Dashboard
2. Click **Create** → **Databases**
3. Choose **PostgreSQL** (version 14 or higher)
4. Select your region and plan
5. Name it (e.g., `webcv-db`)
6. Click **Create Database**
7. Wait for provisioning (~2-3 minutes)
8. Copy the **Connection String** (starts with `postgresql://`)

---

## **Step 2: Create App Platform Service**

### **2.1 Create New App**
1. Go to **Apps** in DigitalOcean Dashboard
2. Click **Create App**
3. Choose **GitHub** as source
4. Authorize DigitalOcean to access your repository
5. Select your `backend` repository
6. Choose branch: `main`
7. Click **Next**

### **2.2 Configure Web Service**
DigitalOcean should auto-detect Python app. Configure:

- **Name**: `webcv-backend`
- **Environment**: Python
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Run Command**: 
  ```bash
  gunicorn --config gunicorn_config.py wsgi:app
  ```
- **HTTP Port**: `8080`
- **Instance Size**: Basic ($5/month or higher)
- **Instance Count**: 1

### **2.3 Add Environment Variables**
Click **Environment Variables** and add:

| Variable | Value | Example |
|----------|-------|---------|
| `FLASK_ENV` | `production` | production |
| `PORT` | `8080` | 8080 |
| `SECRET_KEY` | Generate strong random key | `8f42a73054b1749f8f58848be5e6502c` |
| `JWT_SECRET_KEY` | Generate different random key | `7d9c8e4f1a2b3c5d6e7f8a9b0c1d2e3f` |
| `DATABASE_URL` | Your PostgreSQL connection string | `postgresql://user:pass@host:25060/db?sslmode=require` |
| `CORS_ORIGINS` | Your frontend URL(s) | `http://localhost:3000,https://yourfrontend.com` |

**To generate secure random keys**, run this in terminal:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Optional Variables:**
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### **2.4 Advanced Settings**
- **HTTP Routes**: `/`
- **Health Check Path**: `/health`
- **Source Directory**: `/` (or leave empty)

Click **Next** → **Review** → **Create Resources**

---

## **Step 3: Run Database Migrations**

After deployment completes:

1. Go to your app's **Console** tab
2. Click **Run Command** or open console
3. Run migrations:
   ```bash
   flask db upgrade
   ```

If `flask` command not found, use:
```bash
python -c "from app import create_app, db; from flask_migrate import upgrade; app = create_app('production'); app.app_context().push(); upgrade()"
```

---

## **Step 4: Test Your Backend**

### **4.1 Check Health Endpoint**
Your app URL will be: `https://your-app-name.ondigitalocean.app`

Test:
```bash
curl https://your-app-name.ondigitalocean.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "WebCV Backend API is running"
}
```

### **4.2 Test API Endpoint**
```bash
curl https://your-app-name.ondigitalocean.app/api/jobs
```

---

## **Step 5: Connect Frontend to Backend**

### **5.1 Update Frontend API URL**

In your frontend code, update the API base URL:

**React Example** (`.env` or config file):
```env
REACT_APP_API_URL=https://your-app-name.ondigitalocean.app
```

**Next.js Example**:
```env
NEXT_PUBLIC_API_URL=https://your-app-name.ondigitalocean.app
```

### **5.2 Update CORS_ORIGINS**

Once you deploy your frontend, update the backend's `CORS_ORIGINS`:

1. Go to App Platform → Your Backend App
2. Settings → Environment Variables
3. Edit `CORS_ORIGINS`:
   ```
   https://your-frontend-app.ondigitalocean.app,https://www.yourdomain.com
   ```
4. Save and redeploy

### **5.3 Test Frontend Connection**

From your local frontend:
```javascript
// In your API service file
const API_URL = 'https://your-app-name.ondigitalocean.app';

fetch(`${API_URL}/api/jobs`)
  .then(res => res.json())
  .then(data => console.log(data))
  .catch(err => console.error('API Error:', err));
```

---

## **Step 6: Set Up Background Jobs (Optional)**

The scheduler and scraper should **NOT** run in the web service.

### **6.1 Create Worker Service**

1. In your app, click **Create** → **Worker**
2. Configure:
   - **Name**: `webcv-scheduler`
   - **Run Command**: `python scheduler.py`
   - **Instance Size**: Basic ($5/month)
   
3. Add same environment variables as web service
4. Save

---

## **Troubleshooting**

### **Issue: Frontend can't connect to backend**

**Symptom**: CORS errors, network errors

**Solutions**:
1. Check `CORS_ORIGINS` includes your frontend URL (with `https://`)
2. Check frontend is using correct backend URL
3. Verify backend is running: visit `/health` endpoint
4. Check browser console for exact error

### **Issue: Database connection fails**

**Solutions**:
1. Verify `DATABASE_URL` is correct (copy from DigitalOcean database page)
2. Ensure it includes `?sslmode=require` at the end
3. Check database firewall allows App Platform connections
4. Run migrations: `flask db upgrade`

### **Issue: 502 Bad Gateway**

**Solutions**:
1. Check Runtime Logs for errors
2. Verify gunicorn command is correct
3. Ensure `PORT=8080` in environment variables
4. Check `wsgi.py` exists and has no syntax errors

### **Issue: Import errors**

**Solutions**:
1. Verify all packages in `requirements.txt`
2. Check build logs for failed dependencies
3. Pin specific versions if needed

---

## **Monitoring & Logs**

### **View Logs**
1. Go to your app → **Runtime Logs**
2. Filter by component (web, worker)
3. Check for errors

### **Monitor Performance**
1. Go to **Insights** tab
2. Monitor CPU, Memory, Request rate
3. Scale up if needed

---

## **Custom Domain (Optional)**

1. Go to **Settings** → **Domains**
2. Click **Add Domain**
3. Enter your domain: `api.yourdomain.com`
4. Add DNS records as instructed
5. Wait for SSL certificate provisioning
6. Update `CORS_ORIGINS` with new domain

---

## **Environment Variables Summary**

### **Required (Minimum)**
```env
FLASK_ENV=production
PORT=8080
SECRET_KEY=<random-32-char-hex>
JWT_SECRET_KEY=<random-32-char-hex>
DATABASE_URL=postgresql://...
CORS_ORIGINS=https://your-frontend.com
```

### **Optional (Email)**
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

---

## **Deployment Checklist**

- [ ] PostgreSQL database created
- [ ] App Platform app created
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Run command: `gunicorn --config gunicorn_config.py wsgi:app`
- [ ] Port set to `8080`
- [ ] All required environment variables added
- [ ] App deployed successfully
- [ ] Database migrations run
- [ ] `/health` endpoint returns 200 OK
- [ ] `/api/jobs` endpoint works
- [ ] Frontend `CORS_ORIGINS` configured
- [ ] Frontend connected and tested

---

## **Support**

If you encounter issues:
1. Check Runtime Logs
2. Verify all environment variables
3. Test endpoints with curl
4. Check database connection
5. Review CORS configuration

---

## **Security Notes**

1. ✅ Never commit `.env` file to git
2. ✅ Use strong random keys for SECRET_KEY and JWT_SECRET_KEY
3. ✅ Enable SSL (DigitalOcean provides free SSL)
4. ✅ Restrict CORS_ORIGINS to your actual frontend URLs
5. ✅ Use managed database with SSL enabled
6. ✅ Regularly update dependencies

---

**Happy Deploying! 🚀**
