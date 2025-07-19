# Deployment Guide for Your Voting Application

## Option 1: Deploy to Heroku (Recommended for beginners)

### Prerequisites:
1. Install Git: https://git-scm.com/
2. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
3. Create a Heroku account: https://signup.heroku.com/

### Steps:
1. **Login to Heroku:**
   ```bash
   heroku login
   ```

2. **Initialize Git repository (if not already done):**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

3. **Create Heroku app:**
   ```bash
   heroku create your-app-name
   ```

4. **Deploy to Heroku:**
   ```bash
   git push heroku main
   ```

5. **Open your app:**
   ```bash
   heroku open
   ```

## Option 2: Deploy to Railway

### Steps:
1. Go to https://railway.app/
2. Sign up with GitHub
3. Connect your GitHub repository
4. Railway will automatically detect it's a Python app
5. Deploy!

## Option 3: Deploy to Render

### Steps:
1. Go to https://render.com/
2. Sign up and connect your GitHub
3. Create a new Web Service
4. Connect your repository
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `gunicorn wsgi:app`
7. Deploy!

## Option 4: Deploy to PythonAnywhere

### Steps:
1. Go to https://www.pythonanywhere.com/
2. Create an account
3. Upload your files via Files tab
4. Go to Web tab and create a new web app
5. Choose Flask and Python 3.9
6. Set the WSGI file to point to your app
7. Reload the web app

## Option 5: Deploy to Vercel

### Steps:
1. Go to https://vercel.com/
2. Sign up and connect GitHub
3. Import your repository
4. Vercel will auto-detect and deploy

## Local Testing Before Deployment

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run locally:**
   ```bash
   python app.py
   ```

3. **Test the application at:** http://localhost:5000

## Important Notes:

1. **Environment Variables:** For production, change the secret key:
   ```python
   app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')
   ```

2. **Database:** The current app uses JSON files. For production, consider using a proper database like PostgreSQL.

3. **Security:** 
   - Change the secret key
   - Use HTTPS in production
   - Implement proper session management

4. **File Uploads:** The uploads folder should be properly configured for production.

## Quick Deploy Commands (Heroku):

```bash
# If you haven't initialized git yet
git init
git add .
git commit -m "Initial commit"

# Create and deploy to Heroku
heroku create your-voting-app-name
git push heroku main
heroku open
```

Your app will be live at: `https://your-app-name.herokuapp.com` 