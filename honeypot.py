import os
import csv
import datetime
import requests
import threading
import webbrowser
import time

from flask import (
    Flask,
    request,
    render_template_string,
    jsonify,
    send_from_directory,
    make_response,
)
# try to import CORS
try:
    from flask_cors import CORS
except Exception:
    CORS = None

# ===== Configuration =====
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
LOG_FILE = os.getenv("LOG_FILE", "honeypot_log.csv")
HOST = os.getenv("HOST", "0.0.0.0")   # Flask binding address
PORT = int(os.getenv("PORT", 8080))  # port to run on

# Flask app (serves static frontend from ./frontend)
app = Flask(__name__, static_folder="frontend", static_url_path="/frontend")

# enable CORS if available (helps when frontend is opened via file:// or different origin)
if CORS:
    CORS(app)
else:
    print("Warning: flask-cors not installed. Install with `pip install flask-cors` if you get CORS errors.")

# fallback simple admin HTML in case frontend/admin.html missing
FAKE_ADMIN_HTML = """
<html>
  <head><title>Admin Login</title></head>
  <body>
    <h2>Admin Panel</h2>
    <form method="POST">
      <label>Username</label><input name="username"><br>
      <label>Password</label><input name="password" type="password"><br>
      <button type="submit">Login</button>
    </form>
    <p>If you are the admin, sign in.</p>
  </body>
</html>
"""

# Ensure CSV log file exists with header
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "timestamp",
                "ip",
                "method",
                "path",
                "user_agent",
                "headers",
                "form",
                "raw_body",
                "extra",
            ]
        )


def send_telegram_alert(text: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text}, timeout=5)
    except Exception as e:
        print("Telegram send failed:", e)


def log_request(req, extra=""):
    """Log incoming Flask request to CSV and optionally send Telegram alert."""
    ip = req.remote_addr or "unknown"
    ua = req.headers.get("User-Agent", "")
    headers = dict(req.headers)
    form = dict(req.form)
    raw = req.get_data(as_text=True)
    ts = datetime.datetime.utcnow().isoformat()

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([ts, ip, req.method, req.path, ua, str(headers), str(form), raw, extra])

    # Print + alert
    alert = f"[HONEYPOT] {ts}\nIP: {ip}\nPath: {req.path}\nUA: {ua}\nExtra: {extra}"
    print(alert)
    send_telegram_alert(alert)


# Basic index
@app.route("/", methods=["GET"])
def index():
    return "<h3>Welcome</h3><p>This is a public server.</p>"


# Admin route: serves frontend/admin.html (if present) and logs POST attempts
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "GET":
        frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
        index_path = os.path.join(frontend_dir, "admin.html")
        if os.path.exists(index_path):
            return send_from_directory(frontend_dir, "admin.html")
        else:
            return render_template_string(FAKE_ADMIN_HTML)

    # POST: log the attempt and return 401 so frontend shows invalid credentials
    form = dict(request.form)
    log_request(request, extra=f"submitted creds: {form}")
    resp = make_response("Invalid credentials", 401)
    resp.headers["Content-Type"] = "text/plain"
    return resp


# Honeytoken route (example fake secret)
@app.route("/config/secret.txt")
def honeytoken():
    log_request(request, extra="accessed honeytoken")
    return "API_KEY=ABC123-FAKE-TOKEN-XYZ"


# API: return logs as JSON (frontend should call GET /api/logs)
@app.route("/api/logs", methods=["GET"])
def get_logs():
    logs = []
    if not os.path.exists(LOG_FILE):
        return jsonify(logs)

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                logs.append(row)
    except Exception as e:
        print("Error reading log file:", e)
        return jsonify([]), 500

    return jsonify(logs)


# Serve the frontend index (dashboard) at /dashboard
@app.route("/dashboard", methods=["GET"])
def serve_dashboard():
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return send_from_directory(frontend_dir, "index.html")
    else:
        return "<p>Dashboard not found. Put index.html into the folder 'frontend/'</p>", 404


# Optional simple HTML viewer for quick checking (no JS)
@app.route("/raw_logs", methods=["GET"])
def raw_logs():
    # returns a simple HTML list of latest log lines for quick manual inspection
    rows = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    html = "<h2>Honeypot Raw Logs</h2><pre style='white-space:pre-wrap;'>" + (
        "\n".join([str(r) for r in rows[-200:]]) if rows else "No logs yet."
    ) + "</pre>"
    return html


# Auto-open admin and dashboard in browser after server starts (opens 127.0.0.1)
def _auto_open_pages(port: int):
    def _open():
        time.sleep(1.0)  # wait for server to bind
        admin_url = f"http://127.0.0.1:{port}/admin"
        dashboard_url = f"http://127.0.0.1:{port}/dashboard"
        try:
            webbrowser.open(admin_url)
            webbrowser.open(dashboard_url)
            print(f"[INFO] Opening admin: {admin_url} and dashboard: {dashboard_url}")
        except Exception as e:
            print("[WARN] Could not open browser automatically:", e)

    threading.Thread(target=_open, daemon=True).start()


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "true").lower() == "true"

    # open pages only in the actual serving process (prevents double-open with reloader)
    if (not debug_mode) or (os.getenv("WERKZEUG_RUN_MAIN") == "true"):
        _auto_open_pages(PORT)

    # bind to HOST (0.0.0.0 allowed) but browsers will open 127.0.0.1
    app.run(host=HOST, port=PORT, debug=debug_mode)
