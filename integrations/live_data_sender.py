import requests
import time
import random

# Configuration
API_URL = "http://127.0.0.1:5000/api/v1/receive"
APP_NAME = "E-Commerce-Service"

ERROR_MESSAGES = [
    "Connection timeout to payment gateway",
    "Database disk full on node 4",
    "NullPointerException in checkout flow",
    "Invalid API key provided by merchant",
    "High latency detected in recommendation engine",
    "Unauthorized access attempt to /admin",
    "Stack Overflow in recursive search function",
    "Failed to load user profile from cache"
]

def send_bug_report(message, user_count):
    payload = {
        "error_message": message,
        "user_count": user_count,
        "app_source": APP_NAME
    }
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 201:
            print(f"[SUCCESS] Sent: {message[:40]}... | Severity: {response.json()['received']['severity']}")
        else:
            print(f"[ERROR] Failed to send: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[CRITICAL] Could not connect to Monitoring API: {e}")

if __name__ == "__main__":
    print(f"🚀 Starting Live Data Integration for {APP_NAME}...")
    print(f"📡 Sending data to {API_URL}")
    print("-" * 50)

    # Simulate occasional bugs
    try:
        while True:
            msg = random.choice(ERROR_MESSAGES)
            users = random.randint(1, 100)
            send_bug_report(msg, users)

            # Wait between 5 to 15 seconds for next event
            wait_time = random.uniform(5, 15)
            # print(f"Sleeping for {wait_time:.1f}s...")
            time.sleep(wait_time)
    except KeyboardInterrupt:
        print("\n👋 Integration stopped.")
