import os
import time
import requests

def send_discord_message(webhook_url: str, message: str):
    """Send an error message to Discord webhook."""
    try:
        response = requests.post(webhook_url, json={"content": message})
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to send message to Discord: {e}")

def main():
    url = os.getenv("URL")
    webhook_url = os.getenv("DISCORD_WEBHOOK")

    if not url or not webhook_url:
        raise ValueError("Both URL and DISCORD_WEBHOOK environment variables must be set.")

    while True:
        try:
            response = requests.get(url, timeout=10)
            if not response.ok:  # Non-200 responses
                msg = f"Error: {url} returned status {response.status_code}"
                print(msg)
                send_discord_message(webhook_url, msg)
        except Exception as e:
            msg = f"Exception while fetching {url}: {e}"
            print(msg)
            send_discord_message(webhook_url, msg)

        time.sleep(60)  # wait one minute

if __name__ == "__main__":
    main()
