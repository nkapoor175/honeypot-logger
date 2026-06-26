import requests
import random
import time

# --- Configuration ---
TARGET_URL    = "http://127.0.0.1:5000/login"
DELAY_BETWEEN_REQUESTS = 0.2
TOTAL_REQUESTS         = 30
DEFAULT_USER_AGENT     = "python-requests/2.28.0"  
# --- Attack Data ---
USERNAMES = ["admin", "root", "administrator", "user", "test", "guest"]

PASSWORDS = [
    "password", "123456", "admin123", "letmein", "qwerty",
    "welcome", "monkey", "dragon", "master", "abc123",
    "pass123", "root123", "toor", "test123", "guest123"
]

# Each tuple: (ip_address, number_of_attempts)
# 192.168.1.10 fires 15 to simulate brute force — total = 15+5+5+5 = 30
ATTACKER_IPS = [
    ("192.168.1.10", 15),   # brute forcer — triggers is_brute_force()
    ("10.0.0.5",      5),
    ("172.16.0.3",    5),
    ("8.8.4.4",       5),
]


def build_attack_queue():
    """
    Builds a flat list of (ip, username, password) tuples based on
    the attempt counts defined in ATTACKER_IPS. Shuffled so attacks
    from different IPs are interleaved — more realistic traffic pattern.
    """
    queue = []

    for ip, count in ATTACKER_IPS:
        for _ in range(count):
            username = random.choice(USERNAMES)
            password = random.choice(PASSWORDS)
            queue.append((ip, username, password))

    random.shuffle(queue)
    return queue


def send_attempt(ip, username, password):
    """
    Sends a single fake POST request to the login endpoint.
    Spoofs the X-Forwarded-For header so Flask sees the fake IP
    instead of 127.0.0.1.
    """
    headers = {
        "X-Forwarded-For": ip,
        "User-Agent": "python-requests/2.28.0"
    }
    payload = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(TARGET_URL, data=payload, headers=headers, timeout=5)
        return response.status_code
    except requests.exceptions.ConnectionError:
        return None


def run_simulation():
    """
    Main simulation loop. Fires all attacks in the queue with a fixed
    delay between each request, printing progress as it goes.
    """
    print(f"Starting simulation — {TOTAL_REQUESTS} fake login attempts\n")
    print(f"{'#':<5} {'IP':<16} {'Username':<16} {'Password':<12} {'Status'}")
    print("-" * 60)

    queue      = build_attack_queue()
    failed_count = 0

    for index, (ip, username, password) in enumerate(queue, start=1):
        status_code = send_attempt(ip, username, password)

        if status_code is None:
            status = "CONNECTION FAILED — is Flask running?"
            failed_count += 1
        else:
            status = str(status_code)

        print(f"{index:<5} {ip:<16} {username:<16} {password:<12} {status}")
        time.sleep(DELAY_BETWEEN_REQUESTS)

    print("\nSimulation complete.")
    print("Check your dashboard — threat scores for 192.168.1.10 should be high.")


if __name__ == "__main__":
    run_simulation()