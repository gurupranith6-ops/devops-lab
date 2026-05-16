from flask import Flask, jsonify
import redis, os

app = Flask(__name__)

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=6379,
    decode_responses=True
)

@app.route("/")
def index():
    count = r.incr("visits")
    return jsonify({
        "message": "Hello from the DevOps Lab!",
        "hostname": os.uname().nodename,
        "visits": count
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
