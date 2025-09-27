import time
import requests
import psutil  # Optional: Can be used for monitoring if needed, but here for keep-alive pings

def keep_alive():
    url = "https://www.google.com"  # Or any URL to ping for activity
    while True:
        try:
            response = requests.get(url)
            print(f"Keep-alive ping: {response.status_code}")
        except Exception as e:
            print(f"Ping error: {e}")
        # Optional: Print system info using psutil
        print(f"CPU usage: {psutil.cpu_percent()}%")
        print(f"Memory usage: {psutil.virtual_memory().percent}%")
        time.sleep(300)  # Sleep 5 minutes to prevent rate limiting, keeps the workflow active until timeout (up to 6 hours per run)

keep_alive()
