from flask import Flask, request, render_template, redirect, url_for, make_response, session
import time
from collections import defaultdict
import secrets
import pyotp
import base64
import os

# --- App Setup ---
app = Flask(__name__)

# Generate a secure secret key and corresponding base32 key for TOTP
app.secret_key = secrets.token_hex(32)
totp_key = base64.b32encode(bytes.fromhex(app.secret_key)).decode('utf-8')
VALID_2FA_CODE = pyotp.TOTP(totp_key, digits=3)  # 3-digit TOTP code, changes every 30s

# In-memory rate limit store per IP
rate_limit_storage = defaultdict(list)

# Read valid credentials from environment
VALID_USER = os.environ.get("VALID_USER")
VALID_PASS = os.environ.get("VALID_PASS")

# --- Rate Limiting + OTP Check Logic ---
def check_rate_limit_and_code(ip_address, codeCorrect, max_requests=5, time_window=3600):
    """
    Checks if the user is within the rate limit and whether the OTP is correct.
    If the OTP is wrong, delay the response and log the attempt for rate limiting.
    """
    current_time = time.time()

    # Retrieve recent attempts for this IP
    requests = rate_limit_storage[ip_address]

    # Filter out outdated attempts outside the time window
    requests = [req_time for req_time in requests if current_time - req_time < time_window]

    # If IP is not rate-limited
    if len(requests) < max_requests:
        if codeCorrect:
            return True  # Let them through if OTP is correct 
        
        # If OTP is incorrect, add delay to prevent brute force attacks
        time.sleep(1)

        # Log current attempt to rate limit list
        requests.append(current_time)
        rate_limit_storage[ip_address] = requests

    return False  # Either OTP is wrong or too many attempts

# --- Routes ---

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Login page. First layer of authentication.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == VALID_USER:
            session["user"] = username

            if password == VALID_PASS:
                resp = make_response(redirect(url_for('two_factor')))
                resp.set_cookie('Correct Password', "True", httponly=True)
                return resp

        return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')


@app.route('/2fa', methods=['GET', 'POST'])
def two_factor():
    """
    2FA page. IP Rate-limited if wrong OTP is repeatedly submitted.
    """
    if not session.get('user') or not request.cookies.get('Correct Password'):
        return redirect(url_for('home'))

    if request.method == 'POST':
        user_ip = request.remote_addr
        code = request.form.get('code')

        # Boolean on whether submitted OTP is correct
        print(VALID_2FA_CODE.now())
        codeCorrect = (code == VALID_2FA_CODE.now())

        # Run combined rate-limit and OTP check
        if check_rate_limit_and_code(user_ip, codeCorrect):
            session['authenticated'] = True
            return redirect(url_for('index'))
        else:
            return render_template('2fa.html', error='Invalid 2FA code OR Rate Limit Exceeded')

    return render_template('2fa.html')


@app.route('/index')
def index():
    """
    Protected page. Flag here.
    """
    if not session.get('authenticated') or not session.get('user'):
        return redirect(url_for('home'))

    flag = VALID_PASS  # Flag is stored in password env for convenience
    return render_template('index.html', flag=flag)


# --- Run App ---
if __name__ == '__main__':
    app.run(threaded=True) 
