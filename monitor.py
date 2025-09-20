import os
import time
import requests
from datetime import datetime

def log(message: str):
    """Log message with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} {message}", flush=True)

def send_discord_message(webhook_url: str, message: str):
    """Send an error message to Discord webhook."""
    try:
        response = requests.post(webhook_url, json={"content": message})
        response.raise_for_status()
    except Exception as e:
        log(f"Failed to send message to Discord: {e}")

def main():
    url = os.getenv("URL")
    webhook_url = os.getenv("DISCORD_WEBHOOK")

    if not url or not webhook_url:
        raise ValueError("Both URL and DISCORD_WEBHOOK environment variables must be set.")

    while True:
        try:
            response = requests.get(url, timeout=10)
            log(f"{url} {response.status_code}")
            if not response.ok:  # Non-200 responses
                msg = f"Error: {url} returned status {response.status_code}"
                send_discord_message(webhook_url, msg)
        except Exception as e:
            msg = f"Exception: {e}"
            log(f"{url} {msg}")
            send_discord_message(webhook_url, f"Exception while fetching {url}: {e}")

        time.sleep(60)  # wait one minute

if __name__ == "__main__":
    main()
