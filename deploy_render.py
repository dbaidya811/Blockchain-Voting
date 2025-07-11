#!/usr/bin/env python3
"""
Render Deployment Helper with Live Preview
"""
import os
import subprocess
import webbrowser
import time

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

def check_git_repo():
    """Check if git repository is properly set up"""
    if not os.path.exists('.git'):
        print("📁 Initializing Git repository...")
        run_command("git init", "Git initialization")
        run_command("git add .", "Adding files to git")
        run_command('git commit -m "Initial commit for Render deployment"', "Making initial commit")
        return False
    else:
        print("✅ Git repository exists")
        return True

def setup_github():
    """Help user set up GitHub repository"""
    print("\n📋 GitHub Repository Setup:")
    print("1. Go to https://github.com/new")
    print("2. Create a new repository")
    print("3. Don't initialize with README (we'll push existing code)")
    print("4. Copy the repository URL")
    
    repo_url = input("\nEnter your GitHub repository URL (e.g., https://github.com/username/repo-name): ").strip()
    
    if repo_url:
        print(f"\n🔗 Adding remote origin: {repo_url}")
        run_command(f"git remote add origin {repo_url}", "Adding remote origin")
        run_command("git branch -M main", "Setting main branch")
        run_command("git push -u origin main", "Pushing to GitHub")
        return True
    else:
        print("❌ No repository URL provided")
        return False

def open_render_dashboard():
    """Open Render dashboard in browser"""
    print("\n🌐 Opening Render dashboard...")
    webbrowser.open("https://render.com/dashboard")
    
    print("\n📋 Render Deployment Steps:")
    print("1. Click 'New +' button")
    print("2. Select 'Web Service'")
    print("3. Connect your GitHub repository")
    print("4. Configure settings:")
    print("   - Name: your-voting-app")
    print("   - Environment: Python 3")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: gunicorn wsgi:app")
    print("5. Click 'Create Web Service'")
    print("6. Wait 2-5 minutes for deployment")

def test_local():
    """Test the app locally first"""
    print("\n🧪 Testing locally...")
    run_command("pip install -r requirements.txt", "Installing dependencies")
    
    print("\n🚀 Starting local server...")
    print("Your app will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    try:
        run_command("python app.py", "Running local server")
    except KeyboardInterrupt:
        print("\n⏹️ Server stopped")

def show_live_preview_info():
    """Show information about live preview"""
    print("\n🎯 Live Preview Information:")
    print("After deployment, your app will be available at:")
    print("https://your-app-name.onrender.com")
    print("\n📱 Features to test:")
    print("- Homepage and navigation")
    print("- User registration and login")
    print("- OTP verification system")
    print("- Election creation")
    print("- Voting system")
    print("- MetaMask integration")
    print("- User dashboard")
    print("\n📊 Monitor your app:")
    print("- Check deployment status in Render dashboard")
    print("- View logs for any errors")
    print("- Test all features thoroughly")

def main():
    print("🚀 Render Deployment with Live Preview")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Error: app.py not found. Please run this script from your project directory.")
        return
    
    print("📋 Available options:")
    print("1. Setup GitHub repository and deploy to Render")
    print("2. Test app locally first")
    print("3. Open Render dashboard")
    print("4. Show live preview information")
    
    choice = input("\nSelect an option (1-4): ").strip()
    
    if choice == "1":
        print("\n🚀 Starting Render deployment process...")
        
        # Check git setup
        has_git = check_git_repo()
        
        # Setup GitHub
        if setup_github():
            print("\n✅ GitHub repository setup complete!")
            
            # Open Render dashboard
            open_render_dashboard()
            
            # Show live preview info
            show_live_preview_info()
            
            print("\n🎉 Deployment process initiated!")
            print("Follow the steps above to complete deployment.")
            print("Your app will be live in 2-5 minutes after deployment.")
        else:
            print("\n❌ GitHub setup failed. Please try again.")
    
    elif choice == "2":
        test_local()
    
    elif choice == "3":
        open_render_dashboard()
    
    elif choice == "4":
        show_live_preview_info()
    
    else:
        print("❌ Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    main() 