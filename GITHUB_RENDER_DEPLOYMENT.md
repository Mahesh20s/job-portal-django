# 🚀 Complete Deployment Guide: GitHub → Render.com

This guide will help you deploy your Job Portal to GitHub and host it on Render.com with a live link for your LinkedIn!

---

## **Part 1: Prepare GitHub Repository**

### Step 1: Create GitHub Account & Repository
1. Go to [github.com](https://github.com) and sign up (if you don't have an account)
2. Click **"New"** to create a new repository
3. Name it: `job-portal` (or any name you prefer)
4. **Do NOT initialize** with README, .gitignore, or license (we have these locally)
5. Click **"Create repository"**

### Step 2: Push Code to GitHub (Windows PowerShell)

```powershell
cd C:\Users\shind\job_portal

# Add your GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/job-portal.git

# Rename main branch (if needed)
git branch -M main

# Push code to GitHub
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

### Step 3: Verify on GitHub
- Go to `https://github.com/YOUR_USERNAME/job-portal`
- You should see all your code uploaded ✅

---

## **Part 2: Deploy to Render.com**

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub (click "Continue with GitHub")
3. Authorize Render to access your GitHub account

### Step 2: Create New Web Service
1. Click **"New +"** → Select **"Web Service"**
2. Connect your GitHub repository: Select `job-portal`
3. Fill in the configuration:

| Field | Value |
|-------|-------|
| **Name** | `job-portal` |
| **Environment** | `Python 3` |
| **Region** | `Oregon` (or closest to you) |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput` |
| **Start Command** | `gunicorn job_portal.wsgi:application` |

### Step 3: Add Environment Variables
1. Scroll to **"Environment"** section
2. Click **"Add Environment Variable"** for each:

```
DEBUG = False
SECRET_KEY = your-secret-key-here
ALLOWED_HOSTS = your-app-name.onrender.com
DATABASE_URL = (Render will provide PostgreSQL URL)
EMAIL_BACKEND = django.core.mail.backends.console.EmailBackend
```

**To generate SECRET_KEY**, run this in PowerShell:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 4: Auto-Add PostgreSQL Database
1. In Render dashboard, click **"Create +"** → **"PostgreSQL"**
2. Name: `job-portal-db`
3. Region: Same as web service
4. PostgreSQL Version: Latest
5. Click **"Create Database"**

The `DATABASE_URL` will be automatically added to your web service!

### Step 5: Deploy
1. Click **"Create Web Service"**
2. Render will automatically build and deploy
3. It takes 2-5 minutes ⏳
4. You'll see: **"Your service is live"** ✅

### Step 6: Get Your Live URL
- Your app URL: `https://job-portal.onrender.com` (or similar)
- **Copy this link!** 🔗

---

## **Part 3: Add to LinkedIn**

### Step 1: Copy Your Live Link
From Render dashboard, copy your deployed URL (e.g., `https://job-portal.onrender.com`)

### Step 2: Update LinkedIn Profile
1. Go to [linkedin.com](https://linkedin.com)
2. Edit your profile
3. Scroll to **"Featured"** section → Click **"+"**
4. Select **"Link"** → Paste your job portal URL
5. Add title: `"Job Portal - Full Stack Project"`
6. Add description:
   ```
   Live job portal built with Django & React.
   Features: Job search, applications, bookmarks, employer dashboard
   Deployed on Render.com with PostgreSQL database
   ```
7. Save & your link is live! 🎉

---

## **Part 4: First-Time Deployment Troubleshooting**

### Problem: Build Fails
**Solution**: Check build logs in Render dashboard
1. Click your service → **"Logs"** tab
2. Look for red error messages
3. Common issues:
   - Missing dependencies → Add to `requirements.txt`
   - Database not connected → Check `DATABASE_URL` variable
   - Static files not collected → Ensure `collectstatic` in build command

### Problem: 500 Error After Deploy
1. Check **"Logs"** for error messages
2. Ensure `DEBUG = False` is set
3. Verify `ALLOWED_HOSTS` includes `your-app-name.onrender.com`
4. Check database migration completed

### Problem: Static Files Not Loading
1. Verify build command includes `collectstatic`
2. Ensure `STATIC_URL` and `STATIC_ROOT` configured
3. WhiteNoise middleware should be in `MIDDLEWARE`

---

## **Part 5: Automatic Redeploys**

Your app will **automatically redeploy** whenever you:
1. Push code to `main` branch on GitHub
2. Changes take effect in 1-2 minutes

**Deploy new features**:
```powershell
git add -A
git commit -m "Add new feature: job filters"
git push origin main
```

Render will automatically rebuild and redeploy! 🚀

---

## **Part 6: Manage Your Live App**

### View Logs
- Render dashboard → **"Logs"** tab
- See all server activity in real-time

### Restart Service
- Render dashboard → **"Settings"**
- Click **"Restart Instance"**

### Update Database
- SSH into your service in Render
- Run migrations: `python manage.py migrate`

### Scale Up (Paid)
- Render dashboard → **"Plans"**
- Upgrade instance size if needed

---

## **Environment Variables Setup**

Create a `.env` file locally (don't commit it):

```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,your-app-name.onrender.com
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

For production on Render, set these in the Render dashboard.

---

## **Use This for LinkedIn Posts**

```
🚀 Just deployed my Job Portal to the cloud!

Features:
✅ Full job listings with advanced search
✅ User authentication & employer dashboard
✅ Job applications & bookmarks system
✅ Modern responsive UI
✅ Live database backend

Built with Django, PostgreSQL, and deployed on Render.com

Check it out: [YOUR_LIVE_URL]

#WebDevelopment #FullStack #Django #Deployment
```

---

## **Your Deployment Checklist**

- [ ] Created GitHub repository
- [ ] Pushed code to GitHub
- [ ] Created Render.com account
- [ ] Created web service on Render
- [ ] Added PostgreSQL database
- [ ] Set environment variables
- [ ] Deployed successfully
- [ ] Tested live application
- [ ] Added link to LinkedIn
- [ ] Shared on social media

---

## **Quick Reference: Important URLs**

| Item | URL |
|------|-----|
| GitHub Repo | `https://github.com/YOUR_USERNAME/job-portal` |
| Render Dashboard | `https://dashboard.render.com` |
| Live App | `https://job-portal.onrender.com` |
| LinkedIn Profile | `https://linkedin.com/in/YOUR_USERNAME` |

---

## **Support & Resources**

- **Render Docs**: https://render.com/docs
- **Django Deployment**: https://docs.djangoproject.com/en/6.0/howto/deployment/
- **GitHub Help**: https://docs.github.com
- **PostgreSQL Guide**: https://www.postgresql.org/docs/

---

**🎉 Congratulations! Your job portal is now live and shareable!**

Add that link to your LinkedIn, resume, and portfolio. Employers will be impressed! 💼

