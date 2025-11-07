# API Uptime Monitoring (MSPA)

A real-time monitoring system built with **Python** and **Streamlit** that continuously checks the availability of APIs, logs their response status, and sends **email alerts** when any API goes down.

## Features

- Real-time API monitoring  
- Interactive Streamlit dashboard  
- Response time tracking  
- Automatic email alerts on downtime  
- SQLite-based data logging  
- Secure credentials via `.env`

---

## Project Architecture

| Component       | Description                                                  |
| --------------- | ------------------------------------------------------------ |
| **app.py**      | Streamlit UI — handles input, charts, and status display     |
| **monitor.py**  | Core logic — sends requests, logs responses, triggers alerts |
| **notifier.py** | Sends email notifications via SMTP                           |
| **storage.py**  | Manages SQLite DB for storing checks and monitor info        |
| **utils.py**    | Loads `.env` variables and helper utilities                  |

## Setup & Installation

1️⃣ Clone Repository
```
git clone https://github.com/SnehalSanap0/MSPA.git
cd MSPA
```

2️⃣ Install Dependencies
```
pip install -r requirements.txt
```

3️⃣ Configure Environment Variables
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
ALERT_EMAIL=receiver_email@gmail.com
```

(For testing, you can use Mailtrap)
4️⃣ Run Application
```
streamlit run app.py
```

## Usage


- Enter an API endpoint (e.g., https://api.github.com)


- Choose monitoring interval (in seconds or minutes)


- View real-time status updates and response times


- Receive email alerts when the API is down

## Conclusion
This project provides a lightweight and automated solution for API uptime tracking using Streamlit and Python.
It ensures reliability, transparency, and proactive alerting — a key tool for developers and businesses relying on APIs.
