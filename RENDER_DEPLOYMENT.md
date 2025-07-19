# Render Deployment Guide - Live Preview

## 🚀 Quick Deploy to Render (Live Preview)

### Step 1: Prepare Your Repository
1. **Create a GitHub repository** (if you haven't already):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Push to GitHub:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy to Render

1. **Go to Render.com:**
   - Visit: https://render.com/
   - Sign up with your GitHub account

2. **Create New Web Service:**
   - Click "New +" button
   - Select "Web Service"
   - Connect your GitHub repository

3. **Configure Your Service:**
   - **Name:** `your-voting-app` (or any name you want)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn wsgi:app`
   - **Plan:** Free (or choose paid if needed)

4. **Advanced Settings (Optional):**
   - **Auto-Deploy:** Yes (recommended)
   - **Branch:** main

5. **Click "Create Web Service"**

### Step 3: Get Your Live Preview URL

After deployment (usually 2-5 minutes), you'll get:
- **Live URL:** `https://your-app-name.onrender.com`
- **Status:** Live/Deployed

## 🔍 Live Preview Features

### What You Can Test:
1. **Homepage:** Visit your live URL
2. **User Registration:** Create new accounts
3. **Login System:** Test authentication
4. **Election Creation:** Create voting polls
5. **Voting System:** Cast votes
6. **MetaMask Integration:** Connect wallet
7. **Dashboard:** View user dashboard

### Testing Checklist:
- [ ] Homepage loads correctly
- [ ] User registration works
- [ ] Login/logout functions
- [ ] OTP verification works
- [ ] Election creation works
- [ ] Voting system works
- [ ] MetaMask connection works
- [ ] Dashboard displays correctly

## 🛠️ Troubleshooting

### If Deployment Fails:
1. **Check Build Logs:** Click on your service → Logs
2. **Common Issues:**
   - Missing dependencies in requirements.txt
   - Port configuration issues
   - File path issues

### If App Doesn't Work:
1. **Check Runtime Logs:** View real-time logs
2. **Verify Environment:** Make sure all files are uploaded
3. **Test Locally First:** Run `python app.py` locally

## 📱 Mobile Preview

Your app will work on:
- ✅ Desktop browsers
- ✅ Mobile browsers
- ✅ Tablets
- ✅ All devices

## 🔄 Auto-Deploy

Render automatically redeploys when you:
1. Push changes to GitHub
2. Update your main branch
3. Make code changes

## 📊 Monitoring

Monitor your app:
- **Uptime:** Check if app is running
- **Logs:** View real-time logs
- **Performance:** Monitor response times
- **Errors:** Check for any issues

## 🎯 Quick Commands

```bash
# Update your app
git add .
git commit -m "Update app"
git push origin main

# Check deployment status
# Go to Render dashboard
```

## 📞 Support

If you need help:
1. Check Render documentation
2. View deployment logs
3. Test locally first
4. Contact Render support

Your app will be live at: `https://your-app-name.onrender.com` 