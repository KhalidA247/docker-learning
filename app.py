import socket

import redis
from flask import Flask, render_template_string

app = Flask(__name__)
r = redis.Redis(host="redis", port=6379, decode_responses=True)

PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Khalid's Flask App</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      min-height: 100vh;
      display: grid;
      place-items: center;
      padding: 24px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      color: #e6edf3;
      background:
        radial-gradient(circle at top left, rgba(31, 111, 235, 0.25), transparent 50%),
        radial-gradient(circle at bottom right, rgba(137, 87, 229, 0.25), transparent 50%),
        #0d1117;
    }

    .card {
      width: 100%;
      max-width: 460px;
      padding: 40px 32px;
      text-align: center;
      background: rgba(22, 27, 34, 0.85);
      border: 1px solid #30363d;
      border-radius: 20px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.45);
    }

    .badge {
      display: inline-block;
      margin-bottom: 20px;
      padding: 6px 14px;
      font-size: 13px;
      color: #58a6ff;
      background: rgba(56, 139, 253, 0.12);
      border: 1px solid rgba(56, 139, 253, 0.4);
      border-radius: 999px;
    }

    h1 { font-size: 28px; margin-bottom: 10px; }
    p.sub { color: #8b949e; line-height: 1.5; margin-bottom: 28px; }

    .counter {
      font-size: 72px;
      font-weight: 700;
      line-height: 1;
      margin: 8px 0 6px;
      background: linear-gradient(135deg, #58a6ff, #bc8cff);
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
    }
    .counter-label { color: #8b949e; margin-bottom: 28px; }

    .error {
      margin-bottom: 28px;
      padding: 14px;
      color: #ff7b72;
      background: rgba(248, 81, 73, 0.1);
      border: 1px solid rgba(248, 81, 73, 0.4);
      border-radius: 12px;
    }

    .button {
      display: inline-block;
      padding: 12px 26px;
      color: #fff;
      font-weight: 600;
      text-decoration: none;
      background: linear-gradient(135deg, #1f6feb, #8957e5);
      border-radius: 12px;
      transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .button:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(31, 111, 235, 0.4);
    }
    .button.secondary {
      background: transparent;
      border: 1px solid #30363d;
      color: #c9d1d9;
    }

    .footer {
      margin-top: 32px;
      padding-top: 18px;
      border-top: 1px solid #30363d;
      font-size: 13px;
      color: #6e7681;
    }
    .footer code {
      color: #79c0ff;
      background: rgba(110, 118, 129, 0.2);
      padding: 2px 6px;
      border-radius: 6px;
    }
  </style>
</head>
<body>
  <div class="card">
    <span class="badge">🐳 Running in Docker</span>

    {% if page == "home" %}
      <h1>Welcome to Khalid's Flask App</h1>
      <p class="sub">A small Flask app talking to Redis, containerised with Docker and orchestrated with Compose.</p>
      <a class="button" href="/count">View visit counter</a>
    {% else %}
      <h1>Visit counter</h1>
      {% if error %}
        <div class="error">Couldn't reach Redis. Is the redis container running?</div>
      {% else %}
        <div class="counter">{{ count }}</div>
        <p class="counter-label">{{ "visit" if count == 1 else "visits" }} so far. Refresh to add one!</p>
      {% endif %}
      <a class="button secondary" href="/">← Back home</a>
    {% endif %}

    <div class="footer">Served by container <code>{{ hostname }}</code></div>
  </div>
</body>
</html>
"""


@app.route("/")
def welcome_message():
    return render_template_string(PAGE, page="home", hostname=socket.gethostname())


@app.route("/count")
def count_message():
    try:
        count = r.incr("visits")
        error = False
    except redis.exceptions.ConnectionError:
        count = None
        error = True
    return render_template_string(
        PAGE, page="count", count=count, error=error, hostname=socket.gethostname()
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
