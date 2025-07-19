from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
import json
import os
import random
import hashlib
import base64
import datetime
import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2.rfc6749.errors import MismatchingStateError

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session management and flash messages

USERS_FILE = 'data/users.json'
ELECTIONS_FILE = 'data/elections.json'

GOOGLE_CLIENT_ID = "529170702607-m69gq0vt2k7bnrb44fsfgdmrvi12868k.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
FACEBOOK_CLIENT_ID = "1053147023660486"
FACEBOOK_CLIENT_SECRET = "b29262386d08c2cb4779d158502427c8"
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
REDIRECT_URI = "http://voting-system-kd9y.onrender.com/auth/google/callback"
FACEBOOK_AUTHORIZATION_BASE_URL = "https://www.facebook.com/v17.0/dialog/oauth"
FACEBOOK_TOKEN_URL = "https://graph.facebook.com/v17.0/oauth/access_token"
FACEBOOK_USERINFO_URL = "https://graph.facebook.com/me?fields=id,name,email"
FACEBOOK_REDIRECT_URI = "https://voting-system-kd9y.onrender.com/auth/facebook/callback"

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # For local testing only

# Simple hash for password (SHA256) and email (base64 for demo)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def encrypt_email(email):
    return base64.b64encode(email.encode()).decode()

def decrypt_email(enc_email):
    return base64.b64decode(enc_email.encode()).decode()

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, 'r') as f:
        try:
            return json.load(f)
        except Exception:
            return []

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_elections():
    if not os.path.exists(ELECTIONS_FILE):
        return []
    with open(ELECTIONS_FILE, 'r') as f:
        try:
            return json.load(f)
        except Exception:
            return []

def save_elections(elections):
    with open(ELECTIONS_FILE, 'w') as f:
        json.dump(elections, f, indent=2)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route('/')
def index():
    return render_template('index.html')

# Remove the /login and /signup routes and their logic
# Remove all references to rendering login.html and signup.html
# Replace all redirect(url_for('login')) and url_for('signup') with redirect(url_for('index')) or url_for('index')

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        enc_email = encrypt_email(email)
        users = load_users()
        user = next((u for u in users if u['email'] == enc_email), None)
        if user:
            otp = str(random.randint(100000, 999999))
            session['reset_email'] = enc_email
            session['otp'] = otp
            session['show_otp_alert'] = True
            session['otp_type'] = 'forgot'
            return redirect(url_for('otp'))
        else:
            flash('No user found with this email!', 'danger')
    return render_template('forgot.html')

@app.route('/otp', methods=['GET', 'POST'])
def otp():
    otp_alert = None
    if 'otp' not in session or 'otp_type' not in session:
        return redirect(url_for('index'))
    if session.pop('show_otp_alert', False):
        otp_alert = session.get('otp')
    if request.method == 'POST':
        user_otp = request.form['otp']
        if user_otp == session.get('otp'):
            otp_type = session.pop('otp_type')
            session.pop('otp', None)
            if otp_type == 'login':
                username = session.pop('pending_login')
                session['username'] = username
                flash('Login successful!', 'success')
                next_page = session.pop('next', None)
                if next_page:
                    return redirect(next_page)
                return redirect(url_for('dashboard'))
            elif otp_type == 'signup':
                user_data = session.pop('pending_signup')
                users = load_users()
                users.append(user_data)
                save_users(users)
                session['username'] = user_data['username']
                flash('Signup successful! You are now logged in.', 'success')
                next_page = session.pop('next', None)
                if next_page:
                    return redirect(next_page)
                return redirect(url_for('dashboard'))
            elif otp_type == 'forgot':
                return redirect(url_for('reset_password'))
            elif otp_type == 'delete_account':
                users = load_users()
                username = session.get('username')
                email = session.get('delete_email')
                users = [u for u in users if not (u['username'] == username and u['email'] == email)]
                save_users(users)
                session.clear()
                flash('Account deleted successfully!', 'success')
                return redirect(url_for('index'))
        else:
            flash('Invalid OTP!', 'danger')
    return render_template('otp.html', otp_alert=otp_alert)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if 'reset_email' not in session:
        return redirect(url_for('forgot'))
    if request.method == 'POST':
        new_password = request.form['password']
        users = load_users()
        for user in users:
            if user['email'] == session['reset_email']:
                user['password'] = hash_password(new_password)
        save_users(users)
        flash('Password reset successful! Please login.', 'success')
        session.pop('reset_email', None)
        return redirect(url_for('index'))
    return render_template('reset_password.html')

@app.route('/metamask_auth')
def metamask_auth():
    # Get MetaMask account and balance from sessionStorage via JS fetch
    account = request.cookies.get('metamask_account') or request.args.get('account')
    balance = request.cookies.get('metamask_balance') or request.args.get('balance')
    # Fallback: try from sessionStorage via JS
    if not account:
        account = request.args.get('account')
    if not balance:
        balance = request.args.get('balance')
    if not account:
        # Try to get from JS sessionStorage
        return '''<script>
            var acc = sessionStorage.getItem('metamask_account');
            var bal = sessionStorage.getItem('metamask_balance');
            if(acc){ window.location = '/metamask_auth?account='+acc+'&balance='+bal; }
            else { window.location = '/index'; }
        </script>'''
    # Check if user exists
    users = load_users()
    user = next((u for u in users if u.get('metamask') == account), None)
    if not user:
        # Signup
        user = {'username': account[:8], 'email': '', 'password': '', 'metamask': account}
        users.append(user)
        save_users(users)
    session['username'] = user['username']
    session['metamask'] = account
    session['metamask_balance'] = balance
    flash('MetaMask login successful!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/auth/google')
def google_login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    oauth = OAuth2Session(GOOGLE_CLIENT_ID, redirect_uri=REDIRECT_URI, scope=["openid", "email", "profile"])
    authorization_url, state = oauth.authorization_url(authorization_endpoint, access_type="offline", prompt="consent")
    session["oauth_state"] = state
    return redirect(authorization_url)

@app.route('/auth/google/callback')
def google_callback():
    if "oauth_state" not in session:
        flash("Session expired or invalid OAuth flow. Please try again.", "danger")
        return redirect(url_for("index"))
    try:
        oauth = OAuth2Session(GOOGLE_CLIENT_ID, redirect_uri=REDIRECT_URI, state=session["oauth_state"])
        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]
        token = oauth.fetch_token(
            token_endpoint,
            client_secret=GOOGLE_CLIENT_SECRET,
            authorization_response=request.url,
        )
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        resp = oauth.get(userinfo_endpoint)
        userinfo = resp.json()
        session['username'] = userinfo["email"]
        session['google_name'] = userinfo.get("name")
        return redirect(url_for("dashboard"))
    except MismatchingStateError:
        flash("OAuth state mismatch. Please try logging in again.", "danger")
        return redirect(url_for("index"))

@app.route('/auth/facebook')
def facebook_login():
    facebook = OAuth2Session(FACEBOOK_CLIENT_ID, redirect_uri=FACEBOOK_REDIRECT_URI, scope=["email"])
    authorization_url, state = facebook.authorization_url(FACEBOOK_AUTHORIZATION_BASE_URL)
    session["oauth_state_fb"] = state
    return redirect(authorization_url)

@app.route('/auth/facebook/callback')
def facebook_callback():
    if "oauth_state_fb" not in session:
        return redirect(url_for("index"))
    facebook = OAuth2Session(FACEBOOK_CLIENT_ID, redirect_uri=FACEBOOK_REDIRECT_URI, state=session["oauth_state_fb"])
    token = facebook.fetch_token(
        FACEBOOK_TOKEN_URL,
        client_secret=FACEBOOK_CLIENT_SECRET,
        authorization_response=request.url,
    )
    resp = facebook.get(FACEBOOK_USERINFO_URL, params={"access_token": token["access_token"]})
    userinfo = resp.json()
    session['username'] = userinfo.get("email", userinfo.get("id"))
    session['facebook_name'] = userinfo.get("name")
    return redirect(url_for("dashboard"))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    users = load_users()
    user = next((u for u in users if u['username'] == session['username']), None)
    email = decrypt_email(user['email']) if user and user['email'] else ''
    metamask = session.get('metamask')
    metamask_balance = session.get('metamask_balance')
    return render_template('dashboard.html', username=session['username'], email=email, metamask=metamask, metamask_balance=metamask_balance)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    if 'username' not in session:
        return redirect(url_for('index'))
    users = load_users()
    user = next((u for u in users if u['username'] == session['username']), None)
    if not user:
        session.clear()
        flash('User not found or already deleted.', 'danger')
        return redirect(url_for('index'))
    if request.method == 'POST':
        users = [u for u in users if u['username'] != user['username']]
        save_users(users)
        session.clear()
        flash('Account deleted successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('delete_account_confirm.html', username=user['username'])

@app.route('/create_election', methods=['GET', 'POST'])
def create_election():
    import os
    from werkzeug.utils import secure_filename
    if 'username' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form['name'].strip()
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        # Handle event image
        event_image = request.files.get('event_image')
        event_image_filename = ''
        if event_image and event_image.filename:
            event_image_filename = secure_filename(f"event_{int(datetime.datetime.now().timestamp())}_{event_image.filename}")
            event_image.save(os.path.join('static/uploads', event_image_filename))
        # Handle competitors
        competitors = []
        for key in request.form:
            if key.startswith('competitor_name_'):
                idx = key.split('_')[-1]
                comp_name = request.form[key].strip()
                comp_img = request.files.get(f'competitor_img_{idx}')
                comp_img_filename = ''
                if comp_img and comp_img.filename:
                    comp_img_filename = secure_filename(f"comp_{idx}_{int(datetime.datetime.now().timestamp())}_{comp_img.filename}")
                    comp_img.save(os.path.join('static/uploads', comp_img_filename))
                competitors.append({'name': comp_name, 'image': comp_img_filename})
        if not name or len(competitors) < 2:
            flash('Please provide a name and at least two competitors.', 'danger')
            return render_template('create_election.html')
        try:
            start_dt = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M') if start_time else None
            end_dt = datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M') if end_time else None
        except Exception:
            flash('Invalid date/time format.', 'danger')
            return render_template('create_election.html')
        elections = load_elections()
        creator = session.get('metamask') or session['username']
        election = {
            'id': f'elect_{len(elections)+1}_{int(datetime.datetime.now().timestamp())}',
            'name': name,
            'competitors': competitors,
            'votes': {},
            'creator': creator,
            'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
            'start_time': start_time,
            'end_time': end_time,
            'event_image': event_image_filename,
            'status': 'active'
        }
        elections.append(election)
        save_elections(elections)
        flash('Election created successfully!', 'success')
        return redirect(url_for('my_elections'))
    return render_template('create_election.html')

@app.route('/my_elections')
def my_elections():
    if 'username' not in session:
        return redirect(url_for('index'))
    elections = load_elections()
    creator = session.get('metamask') or session['username']
    current_user = session.get('metamask') or session['username']
    my_elections = [e for e in elections if e.get('creator') == creator]
    return render_template('my_elections.html', elections=my_elections, current_user=current_user)

# --- In vote_now, add logic to hide voters and show receipt ---
@app.route('/vote_now', methods=['GET', 'POST'])
def vote_now():
    if 'username' not in session:
        next_url = request.url
        return redirect(url_for('index', next=next_url))
    election_id = request.args.get('election_id')
    elections = load_elections()
    election = None
    show_voters = False  # Always False for shared link experience
    vote_receipt = None
    if election_id:
        election = next((e for e in elections if e['id'] == election_id), None)
        if not election:
            flash('Election not found.', 'danger')
            return redirect(url_for('dashboard'))
        ended = False
        if election['end_time']:
            try:
                end_dt = datetime.datetime.strptime(election['end_time'], '%Y-%m-%d %H:%M')
                if datetime.datetime.now() > end_dt:
                    ended = True
                    election['status'] = 'ended'
            except Exception:
                pass
        voter = session.get('metamask') or session['username']
        has_voted = voter in election['votes']
        if request.method == 'POST' and not ended and not has_voted:
            choice = request.form.get('option')
            competitor_names = [comp['name'] for comp in election['competitors']]
            if choice and choice in competitor_names:
                election['votes'][voter] = choice
                save_elections(elections)
                flash('Your vote has been recorded!', 'success')
                has_voted = True
                # Generate a unique receipt (hash of username+election+timestamp)
                import hashlib
                import time
                receipt_data = f"{voter}|{election['id']}|{choice}|{int(time.time())}"
                vote_receipt = hashlib.sha256(receipt_data.encode()).hexdigest()
                session['vote_receipt'] = vote_receipt
                session['vote_receipt_data'] = receipt_data
            else:
                flash('Invalid vote option.', 'danger')
        # Prepare results
        competitor_names = [comp['name'] for comp in election['competitors']]
        results = {name: 0 for name in competitor_names}
        for v in election['votes'].values():
            if v in results:
                results[v] += 1
        total_votes = sum(results.values())
        creator = session.get('metamask') or session['username']
        current_user = session.get('metamask') or session['username']
        # Show receipt if just voted
        if 'vote_receipt' in session and has_voted:
            vote_receipt = session.pop('vote_receipt')
            vote_receipt_data = session.pop('vote_receipt_data')
        else:
            vote_receipt = None
            vote_receipt_data = None
        return render_template('vote_now.html', election=election, ended=ended, has_voted=has_voted, results=results, total_votes=total_votes, is_creator=(creator == election['creator']), current_user=current_user, show_voters=show_voters, vote_receipt=vote_receipt, vote_receipt_data=vote_receipt_data)
    # If no election_id, show a list of available elections to vote in
    voter = session.get('metamask') or session['username']
    available = []
    for e in elections:
        ended = False
        if e['end_time']:
            try:
                end_dt = datetime.datetime.strptime(e['end_time'], '%Y-%m-%d %H:%M')
                if datetime.datetime.now() > end_dt:
                    ended = True
            except Exception:
                pass
        if e['status'] == 'active' and not ended and voter not in e['votes']:
            available.append(e)
    return render_template('vote_now.html', available=available)

@app.route('/voting_history')
def voting_history():
    if 'username' not in session:
        return redirect(url_for('index'))
    elections = load_elections()
    current_user = session.get('metamask') or session['username']
    
    # Get all elections where the user has voted
    user_voting_history = []
    for election in elections:
        if current_user in election.get('votes', {}):
            user_voting_history.append({
                'election': election,
                'user_vote': election['votes'][current_user],
                'voted_at': election.get('created_at', 'Unknown')
            })
    
    # Sort by creation date (newest first)
    user_voting_history.sort(key=lambda x: x['voted_at'], reverse=True)
    
    return render_template('voting_history.html', voting_history=user_voting_history, current_user=current_user)

@app.route('/election/<election_id>')
def election_detail(election_id):
    if 'username' not in session:
        return redirect(url_for('index'))
    elections = load_elections()
    election = next((e for e in elections if e['id'] == election_id), None)
    if not election:
        flash('Election not found.', 'danger')
        return redirect(url_for('my_elections'))
    return render_template('election_detail.html', election=election)

@app.route('/delete_election/<election_id>', methods=['POST'])
def delete_election(election_id):
    if 'username' not in session:
        return redirect(url_for('index'))
    elections = load_elections()
    creator = session.get('metamask') or session['username']
    election = next((e for e in elections if e['id'] == election_id), None)
    if not election or election.get('creator') != creator:
        flash('You are not authorized to delete this election.', 'danger')
        return redirect(url_for('my_elections'))
    
    # Remove the election from the list
    elections = [e for e in elections if e['id'] != election_id]
    save_elections(elections)
    flash('Election has been deleted successfully.', 'success')
    return redirect(url_for('my_elections'))

@app.route('/stop_election/<election_id>', methods=['POST'])
def stop_election(election_id):
    if 'username' not in session:
        return redirect(url_for('index'))
    elections = load_elections()
    creator = session.get('metamask') or session['username']
    election = next((e for e in elections if e['id'] == election_id), None)
    if not election or election.get('creator') != creator:
        flash('You are not authorized to stop this election.', 'danger')
        return redirect(url_for('my_elections'))
    if election['status'] == 'ended':
        flash('Election is already ended.', 'info')
        return redirect(url_for('my_elections'))
    election['status'] = 'ended'
    save_elections(elections)
    flash('Election has been stopped and voting is now closed.', 'success')
    return redirect(url_for('my_elections'))

if __name__ == '__main__':
    app.run(debug=True) 
