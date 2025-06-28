import redis
from flask import request, jsonify
from functools import wraps
from datetime import datetime

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

MAX_REQUESTS = 5
WINDOW_SECONDS = 60  # 1 minute

def rate_limiter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ip = request.remote_addr
        key = f"rate:{ip}"

        current = r.incr(key)

        if current == 1:
            r.expire(key, WINDOW_SECONDS)

        if current > MAX_REQUESTS:
            # LOG the abuse
            timestamp = datetime.utcnow().isoformat()
            r.lpush("abuse_log", f"{ip}|{timestamp}")
            r.ltrim("abuse_log", 0, 99)  # keep only latest 100

            return jsonify({
                "error": "Too many requests, please try again later.",
                "ip": ip,
                "requests": current
            }), 429

        return func(*args, **kwargs)

    return wrapper
