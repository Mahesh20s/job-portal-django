# DEPLOYMENT GUIDE - Job Portal

## Step 1: Push to GitHub

### 1.1 Initialize Git repository
```bash
cd job_portal
git init
git add .
git commit -m "Initial commit: Job portal application"
```

### 1.2 Create GitHub repository
1. Go to https://github.com/new
2. Create a new repository named `job_portal`
3. Do NOT initialize with README, .gitignore, or license (we already have them)

### 1.3 Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/job_portal.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy to Render.com (FREE TIER AVAILABLE)

### 2.1 Create Render Account
- Go to https://render.com
- Click "Sign Up"
- Choose "Sign up with GitHub"
- Authorize Render to access your GitHub account

### 2.2 Create Web Service
1. Click "Dashboard" → "New" → "Web Service"
2. Select "Deploy existing code from a repository"
3. Click "Connect GitHub" and authorize
4. Select the `job_portal` repository
5. Configure:
   - **Name**: `job-portal` (or your preferred name)
   - **Root Directory**: (leave empty)
   - **Runtime**: `Python 3`
   - **Build Command**:
     ```
     pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --no-input
     ```
   - **Start Command**:
     ```
     gunicorn job_portal.wsgi:application
     ```
   - **Plan**: Free (recommended for testing)

### 2.3 Set Environment Variables
In the Render dashboard, go to "Environment":
```
DEBUG=False
SECRET_KEY=generate-a-strong-random-secret-here
ALLOWED_HOSTS=yourdomain.onrender.com
DATABASE_URL=internal database URL (Render will provide)
```

### 2.4 Deploy
- Click "Create Web Service"
- Wait 5-10 minutes for deployment
- Your app will be live at: `https://job-portal.onrender.com`

---

## Step 3: Deploy to Heroku (Alternative)

### 3.1 Install Heroku CLI
**Windows:**
```bash
# Using Chocolatey:
choco install heroku-cli

# Or download from:
https://devcenter.heroku.com/articles/heroku-cli
```

**Mac/Linux:**
```bash
brew tap heroku/brew && brew install heroku
```

### 3.2 Login to Heroku
```bash
heroku login
```

### 3.3 Create Heroku App
```bash
heroku create your-job-portal-app

# The app will be at: https://your-job-portal-app.herokuapp.com
```

### 3.4 Add PostgreSQL Database
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

### 3.5 Set Environment Variables
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-super-secret-key-here
heroku config:set ALLOWED_HOSTS=your-job-portal-app.herokuapp.com
```

### 3.6 Deploy
```bash
git push heroku main
```

### 3.7 Run Migrations
```bash
heroku run python manage.py migrate
heroku run python manage.py populate_jobs
heroku run python manage.py createsuperuser
```

---

## Step 4: Generate Secret Key

### Generate a Strong Secret Key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and use it for `SECRET_KEY` in environment variables.

---

## Step 5: Share Your Link on LinkedIn

### 5.1 Get Your Live URL
- **Render**: `https://job-portal.onrender.com`
- **Heroku**: `https://your-job-portal-app.herokuapp.com`

### 5.2 Add to LinkedIn
1. Go to your LinkedIn profile
2. Click "Edit public profile URL"
3. Add your portfolio/projects section
4. Link to your deployed app
5. Include a description:

```
Job Portal - A Django web application for job posting and applications.
Built with Django, PostgreSQL, and deployed on Render.

Features:
- User authentication (job seekers & employers)
- Job posting and management
- Application tracking
- Job bookmarking
- Advanced search and filtering

Live Demo: [Your Deployed URL]
GitHub: https://github.com/YOUR_USERNAME/job_portal
```

---

## Step 6: Set Up Custom Domain (Optional)

### With Render:
1. Go to Service Settings
2. Click "Domain"
3. Add your custom domain
4. Update DNS records as instructed

### With Heroku:
```bash
heroku domains:add www.yourdomain.com
```

---

## Step 7: Troubleshooting

### Issue: Static files not loading
**Solution**: Run `python manage.py collectstatic`

### Issue: Database errors on deployment
**Solution**: 
```bash
# Render: Automatic
# Heroku: 
heroku run python manage.py migrate
```

### Issue: 500 error after deployment
**Solution**: Check logs:
```bash
# Render: Dashboard → Logs
# Heroku: 
heroku logs --tail
```

### Issue: Email not sending
**Solution**: Configure `EMAIL_HOST_PASSWORD` with Gmail App Password (not your regular password)

---

## Step 8: First-Time Admin Setup

After deployment:
1. Navigate to `https://yourdomain.com/admin/`
2. Create a superuser:
   ```bash
   # Render/Heroku Shell:
   python manage.py createsuperuser
   ```
3. Login with your credentials
4. Add companies and sample jobs

---

## Production Checklist

- [x] Added `DEBUG=False` in environment
- [x] Set unique `SECRET_KEY`
- [x] Configured `ALLOWED_HOSTS`
- [x] Set up database (PostgreSQL)
- [x] Configured static files serving
- [x] Added security middleware
- [x] Set up email for notifications
- [x] Created `.gitignore`
- [x] Pushed to GitHub
- [x] Deployed to hosting platform
- [x] Created admin account
- [x] Tested all major features
- [x] Added link to LinkedIn

---

## Monitoring & Maintenance

### Check app status:
```bash
# Render: Dashboard
# Heroku:
heroku ps
```

### View logs:
```bash
# Render: Real-time logs in dashboard
# Heroku:
heroku logs --tail
```

### Auto-deploy on GitHub push:
- Render: Automatic (enabled by default)
- Heroku: Use GitHub integration in dashboard

---

## Next Steps

1. **Promote on LinkedIn** - Share your deployed app
2. **Add features** - Collect resumes, email digest, ratings
3. **Optimize** - Add caching, CDN for images
4. **Scale** - Move to paid tier when you get users
5. **Custom Domain** - Get your own domain name

---

**Questions? Check:**
- [Render Documentation](https://render.com/docs)
- [Heroku Documentation](https://devcenter.heroku.com/)
- [Django Deployment Guide](https://docs.djangoproject.com/en/6.0/howto/deployment/)
