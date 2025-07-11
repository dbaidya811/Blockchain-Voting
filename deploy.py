#!/usr/bin/env python3
"""
Deployment helper script for the voting application
"""
import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}: {e}")
        print(f"Error output: {e.stderr}")
        return None

def check_git():
    """Check if git is initialized"""
    if not os.path.exists('.git'):
        print("📁 Initializing Git repository...")
        run_command("git init", "Git initialization")
        run_command("git add .", "Adding files to git")
        run_command('git commit -m "Initial commit"', "Making initial commit")
    else:
        print("✅ Git repository already exists")

def deploy_to_heroku():
    """Deploy to Heroku"""
    print("\n🚀 Deploying to Heroku...")
    
    # Check if Heroku CLI is installed
    result = run_command("heroku --version", "Checking Heroku CLI")
    if not result:
        print("❌ Heroku CLI not found. Please install it first:")
        print("   https://devcenter.heroku.com/articles/heroku-cli")
        return False
    
    # Login to Heroku
    print("\n🔐 Please login to Heroku in the browser that opens...")
    run_command("heroku login", "Heroku login")
    
    # Create Heroku app
    app_name = input("\n📝 Enter your Heroku app name (or press Enter for auto-generated): ").strip()
    if app_name:
        create_cmd = f"heroku create {app_name}"
    else:
        create_cmd = "heroku create"
    
    result = run_command(create_cmd, "Creating Heroku app")
    if not result:
        return False
    
    # Deploy to Heroku
    result = run_command("git push heroku main", "Deploying to Heroku")
    if not result:
        return False
    
    # Open the app
    run_command("heroku open", "Opening your app")
    
    print("\n🎉 Deployment completed!")
    print("Your app is now live!")
    return True

def main():
    print("🌐 Voting Application Deployment Helper")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Error: app.py not found. Please run this script from your project directory.")
        return
    
    print("📋 Available deployment options:")
    print("1. Deploy to Heroku (Recommended)")
    print("2. Manual deployment instructions")
    print("3. Test locally")
    
    choice = input("\nSelect an option (1-3): ").strip()
    
    if choice == "1":
        check_git()
        deploy_to_heroku()
    elif choice == "2":
        print("\n📖 Manual deployment instructions:")
        print("1. Read DEPLOYMENT_GUIDE.md for detailed instructions")
        print("2. Choose your preferred platform (Heroku, Railway, Render, etc.)")
        print("3. Follow the platform-specific instructions")
    elif choice == "3":
        print("\n🧪 Testing locally...")
        run_command("pip install -r requirements.txt", "Installing dependencies")
        print("\n🚀 Starting local server...")
        print("Your app will be available at: http://localhost:5000")
        print("Press Ctrl+C to stop the server")
        run_command("python app.py", "Running local server")
    else:
        print("❌ Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main() 