from flask import Flask, jsonify
import redis
import os

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


@app.route("/reset", methods=["POST"])
def reset():
    r.set("visits", 0)

    return jsonify({
        "message": "Visit counter reset to zero.",
        "visits": 0
    })


@app.route("/stats")
def stats():
    visits = r.get("visits") or "0"

    return jsonify({
        "visits": int(visits),
        "hostname": os.uname().nodename,
        "redis_host": os.getenv("REDIS_HOST", "localhost")
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
