import threading
import time
import requests
from storage import list_monitors, update_monitor_status, get_conn
from notifier import notify_down


# Basic check function
def check_once(monitor):
    url = monitor['url']
    monitor_id = monitor['id']
    try:
        start = time.time()
        r = requests.get(url, timeout=10)
        elapsed_ms = round((time.time() - start) * 1000, 2)
        status_code = r.status_code
        status_text = 'UP' if 200 <= status_code < 400 else f'ERROR {status_code}'
        update_monitor_status(monitor_id, status_text, status_code, elapsed_ms)
        return status_text, status_code, elapsed_ms
    except requests.exceptions.RequestException as e:
        update_monitor_status(monitor_id, 'DOWN', None, None)
        notify_down(url, str(e))
        return 'DOWN', None, None




class MonitorWorker:
    """Singleton worker that periodically checks all active monitors.
    Runs in a background thread so the UI is responsive.
    """
    def __init__(self):
        self._stop = threading.Event()
        self._thread = None

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()


    def stop(self):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=1)


    def _run_loop(self):
        # naive scheduler: fetch monitors and sleep for 1 sec between checks
        while not self._stop.is_set():
            monitors = list_monitors()
            for m in monitors:
                if not m.get('active', 1):
                    continue
                # check each monitor in its own short-lived thread to avoid blocking
                t = threading.Thread(target=check_once, args=(m,), daemon=True)
                t.start()
            time.sleep(5)