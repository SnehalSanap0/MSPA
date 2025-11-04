import sqlite3
from pathlib import Path
from utils import now_iso

DB_PATH = Path('data') / 'uptime.db'
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

SCHEMA = '''
CREATE TABLE IF NOT EXISTS monitors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL UNIQUE,
    interval_minutes INTEGER NOT NULL DEFAULT 5,
    active INTEGER NOT NULL DEFAULT 1,
    last_status TEXT,
    last_checked TEXT
);

CREATE TABLE IF NOT EXISTS checks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    monitor_id INTEGER NOT NULL,
    status_code INTEGER,
    status_text TEXT,
    response_time_ms REAL,
    checked_at TEXT NOT NULL,
    FOREIGN KEY(monitor_id) REFERENCES monitors(id)
);
'''


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.executescript(SCHEMA)
    conn.commit()
    conn.close()


# Monitor CRUD
def add_monitor(url, interval=5):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('INSERT OR IGNORE INTO monitors(url, interval_minutes) VALUES (?,?)', (url, interval))
    conn.commit()
    conn.close()


def update_monitor_status(monitor_id, status_text, status_code, response_time_ms):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('UPDATE monitors SET last_status = ?, last_checked = ? WHERE id=?', (status_text, now_iso(), monitor_id))
    cur.execute('INSERT INTO checks(monitor_id, status_code, status_text, response_time_ms, checked_at) VALUES (?,?,?,?,?)',
    (monitor_id, status_code, status_text, response_time_ms, now_iso()))
    conn.commit()
    conn.close()


def list_monitors():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM monitors')
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_checks(monitor_id, limit=200):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM checks WHERE monitor_id=? ORDER BY checked_at DESC LIMIT ?', (monitor_id, limit))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]