from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Plugs in automatically when Person A pushes database.py
try:
    from database import save_attempt, get_all_attempts, get_stats
    DB_READY = True
    print("[INFO] database.py loaded")
except ImportError:
    DB_READY = False
    print("[WARN] database.py not found yet — running without DB")

# Plugs in automatically when Person E pushes honeypot_logic.py
try:
    from honeypot_logic import get_location, calculate_threat_score
    HONEYPOT_READY = True
    print("[INFO] honeypot_logic.py loaded")
except ImportError:
    HONEYPOT_READY = False
    print("[WARN] honeypot_logic.py not found yet — skipping threat scoring")


@app.route('/')
def login_page():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    # Extract data from the incoming request
    ip = request.remote_addr
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    user_agent = request.headers.get('User-Agent', '')

    # Get geolocation from Person E's module
    country, city = '', ''
    if HONEYPOT_READY:
        location = get_location(ip)
        country = location.get('country', '')
        city = location.get('city', '')

    # Get threat score from Person E's module
    threat_score = 0
    if HONEYPOT_READY:
        threat_score = calculate_threat_score(ip, username, password)

    # Save attempt via Person A's module
    if DB_READY:
        save_attempt(
            ip_address=ip,
            username=username,
            password=password,
            user_agent=user_agent,
            country=country,
            city=city,
            threat_score=threat_score
        )

    print(f"[ATTEMPT] ip={ip} | user={username} | threat={threat_score} | country={country}")
    return jsonify({"status": "error", "message": "Invalid credentials"})


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/api/logs')
def api_logs():
    if not DB_READY:
        return jsonify([])
    return jsonify(get_all_attempts())


@app.route('/api/stats')
def api_stats():
    if not DB_READY:
        return jsonify({})
    return jsonify(get_stats())


if __name__ == '__main__':
    app.run(debug=True)
