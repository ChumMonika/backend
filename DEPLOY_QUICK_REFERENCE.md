# Quick Deployment Reference

## 🚀 DigitalOcean App Platform - Quick Start

### **Gunicorn Command**
```bash
gunicorn --config gunicorn_config.py wsgi:app
```

### **Required Environment Variables**
```env
FLASK_ENV=production
PORT=8080
SECRET_KEY=<generate-with-command-below>
JWT_SECRET_KEY=<generate-with-command-below>
DATABASE_URL=<your-postgresql-connection-string>
CORS_ORIGINS=https://your-frontend-url.com
```

### **Generate Secret Keys**
```bash
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_hex(32))"
```

---

## 📋 Files Changed/Added

### **New Files Created:**
1. ✅ `wsgi.py` - Production WSGI entry point (no side effects)
2. ✅ `.do/app.yaml` - DigitalOcean App Spec
3. ✅ `.env.example` - Environment variables template
4. ✅ `DEPLOYMENT.md` - Complete deployment guide

### **Modified Files:**
1. ✅ `gunicorn_config.py` - Port changed to 8080
2. ✅ `config.py` - Improved CORS origins handling (strips whitespace)

---

## 🔧 Deployment Commands

### **Build Command:**
```bash
pip install -r requirements.txt
```

### **Run Command:**
```bash
gunicorn --config gunicorn_config.py wsgi:app
```

### **After Deployment - Run Migrations:**
```bash
flask db upgrade
```

Or if flask command not available:
```bash
python -c "from app import create_app, db; from flask_migrate import upgrade; app = create_app('production'); app.app_context().push(); upgrade()"
```

---

## 🌐 Frontend Connection Fix

### **Issue**: Frontend (localhost) → Backend (DigitalOcean) connection failing

### **Root Cause**: CORS configuration

### **Solution**:

1. **In DigitalOcean Backend** - Set `CORS_ORIGINS`:
   ```
   http://localhost:3000,http://127.0.0.1:3000
   ```
   *(Add more origins separated by commas, NO SPACES)*

2. **In Frontend Code** - Update API URL:
   ```javascript
   const API_URL = 'https://your-app-name.ondigitalocean.app';
   ```

3. **Test Connection**:
   ```bash
   curl https://your-app-name.ondigitalocean.app/health
   ```
   Should return:
   ```json
   {"status": "healthy", "message": "WebCV Backend API is running"}
   ```

---

## 🎯 Port Configuration

- **DigitalOcean App Platform**: Port `8080` (configured)
- **Render**: Port from `$PORT` env variable (already configured)
- **Heroku**: Port from `$PORT` env variable (already configured)

Your app now works on all platforms! ✅

---

## 🔒 Security Checklist

- [ ] Generate new SECRET_KEY (don't use default)
- [ ] Generate new JWT_SECRET_KEY (don't use default)
- [ ] Set CORS_ORIGINS to actual frontend URLs only
- [ ] Use PostgreSQL with SSL (`?sslmode=require`)
- [ ] Don't commit `.env` file
- [ ] Enable DigitalOcean SSL certificate (automatic)

---

## 📊 Testing Endpoints

After deployment, test these:

```bash
# Health check
curl https://your-app.ondigitalocean.app/health

# API root
curl https://your-app.ondigitalocean.app/

# Jobs endpoint
curl https://your-app.ondigitalocean.app/api/jobs

# Login (POST example)
curl -X POST https://your-app.ondigitalocean.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}'
```

---

## ⚠️ Important Notes

### **Schedulers/Scrapers**
- `scheduler.py` and `auto_scraper.py` should **NOT** run in web service
- They are separate processes (run as workers if needed)
- Web service only serves HTTP requests

### **No Side Effects on Import**
- ✅ `wsgi.py` imports cleanly (no auto-start of schedulers)
- ✅ `run.py` only runs dev server if `__name__ == '__main__'`
- ✅ App factory pattern ensures clean initialization

---

**Read full guide**: [DEPLOYMENT.md](DEPLOYMENT.md)

**Need help?** Check Runtime Logs in DigitalOcean dashboard.
