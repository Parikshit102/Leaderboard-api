# app.py — Flask entry point, serves the frontend HTML

from flask import Flask, render_template

app = Flask(__name__)

# ── Route to serve the leaderboard page ─────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")   # serves templates/index.html


if __name__ == "__main__":
    app.run(debug=True, port=5000)
