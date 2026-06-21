from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    # TODO: wire up to database + honeypot logic
    print("Login attempt received:", request.form)
    return jsonify({"status": "error", "message": "Invalid credentials"})

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/logs')
def api_logs():
    return jsonify([])  # TODO: return real logs

@app.route('/api/stats')
def api_stats():
    return jsonify({})  # TODO: return real stats

if __name__ == '__main__':
    app.run(debug=True)
