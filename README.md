# 🛡️ Web Honeypot

A lightweight Flask-based web honeypot designed to detect, capture, and monitor suspicious web requests in a controlled cybersecurity lab environment.

## 📌 Project Overview

This project simulates a vulnerable web application environment to attract and record suspicious activity.

The honeypot captures information about incoming requests such as:

- IP address
- HTTP method
- Requested path
- User-Agent
- HTTP headers
- Submitted form data
- Raw request body
- Additional activity details
- Timestamp

Captured activity is stored in a CSV log file and can optionally trigger Telegram alerts.

## 🚀 Features

- Flask-based web honeypot
- Fake Admin Login endpoint
- Credential-attempt logging
- Honeytoken endpoint
- Request monitoring and logging
- CSV-based activity logs
- Web-based monitoring dashboard
- Raw log viewer
- Telegram alert integration
- Docker support
- Docker Compose deployment
- Environment-based configuration

## 🔍 Honeypot Endpoints

### `/`

Basic public-facing page used to make the application appear like a normal web server.

### `/admin`

Fake administrator login page.

POST requests to this endpoint are logged, including submitted form data, and return an invalid-credentials response.

### `/config/secret.txt`

Honeytoken endpoint containing a fake API key.

Accessing this endpoint is logged as suspicious activity.

### `/api/logs`

Returns collected honeypot logs in JSON format for the monitoring dashboard.

### `/dashboard`

Displays the web-based monitoring dashboard.

### `/raw_logs`

Provides a simple HTML view of recently collected honeypot logs.

## 📊 Logging

The honeypot stores activity in:

```text
honeypot_log.csv

Each logged request contains:

timestamp
ip
method
path
user_agent
headers
form
raw_body
extra
🔔 Telegram Alerts

The project supports optional Telegram notifications whenever suspicious activity is detected.

Configure the following values in your .env file:

TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
LOG_FILE=honeypot_log.csv
PORT=8080
HOST=0.0.0.0
FLASK_DEBUG=true

Do not commit your actual .env file or real Telegram credentials to GitHub.

🐳 Docker Deployment

The project includes a Dockerfile and docker-compose.yml for containerized deployment.

Build and start the honeypot using:

docker compose up --build

The application runs on port:

8080

For a local lab environment:

http://127.0.0.1:8080

Dashboard:

http://127.0.0.1:8080/dashboard

Admin page:

http://127.0.0.1:8080/admin
💻 Local Setup

Clone the repository:

git clone https://github.com/Mannat29/web-honeypot.git
cd web-honeypot

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.\.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Create your environment file:

.env.example → .env

Configure the required values and run:

python honeypot.py
🗂️ Project Structure
web-honeypot/
│
├── frontend/
│   ├── admin.html
│   ├── dashboard.js
│   ├── index.html
│   └── style.css
│
├── task-manager/
│   ├── backend/
│   └── frontend/
│
├── honeypot.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
🧪 Security Demonstration

The project can be used in a controlled lab to demonstrate how a honeypot detects suspicious behavior such as:

Unauthorized admin login attempts
Attempts to access fake secrets
Automated web requests
Unexpected API requests
Suspicious request payloads
Reconnaissance activity

The collected logs can then be inspected through the dashboard or raw log viewer.

⚠️ Security Notice

This project is intended for educational and authorized cybersecurity testing only.

Do not deploy the honeypot on infrastructure you do not own or have explicit permission to monitor.

If exposed to a network, isolate the honeypot from sensitive systems and avoid storing real credentials, secrets, or personal information.

🛠️ Technologies Used
Python
Flask
HTML
CSS
JavaScript
Docker
Docker Compose
CSV logging
Telegram Bot API
🎯 Learning Objectives

This project demonstrates practical concepts related to:

Web honeypots
Threat detection
HTTP request monitoring
Security logging
Honeytokens
Attack observation
Security alerting
Containerization
Basic security monitoring dashboards
👩‍💻 Author

Mannat Tomar

GitHub: https://github.com/Mannat29