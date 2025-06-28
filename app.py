from flask import Flask, jsonify
from limiter import rate_limiter, r  # Redis client

print("🟡 Starting Flask App...")

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to RateShield"})

@app.route('/api/data')
@rate_limiter
def get_data():
    return jsonify({"data": "This is protected data."})

# ✅ Abuse log viewer route
@app.route('/api/logs/abuse')
def get_abuse_logs():
    logs = r.lrange("abuse_log", 0, -1)
    formatted = []
    for entry in logs:
        ip, ts = entry.split('|')
        formatted.append({"ip": ip, "timestamp": ts})
    return jsonify(formatted)

if __name__ == '__main__':
    print("🟢 Running app on http://127.0.0.1:5050")
    app.run(debug=True, host='0.0.0.0', port=5050)
