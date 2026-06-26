import requests
import logging
from database import get_attempts_by_ip, get_recent_attempts


# --- Scoring Constants ---
COUNT_THRESHOLDS = [
    (5,  20),
    (10, 20),
    (20, 20),
    (50, 20),
]
RECENT_BURST_THRESHOLD   = 5
RECENT_BURST_SCORE       = 20
RECENT_WINDOW_MINUTES    = 10

SUSPICIOUS_USERNAME_THRESHOLD = 2
SUSPICIOUS_USERNAME_SCORE     = 10
BOT_UA_SCORE                  = 10

BRUTE_FORCE_ATTEMPT_THRESHOLD = 10
BRUTE_FORCE_WINDOW_MINUTES    = 10

SUSPICIOUS_USERNAMES  = {"admin", "root", "administrator", "test", "guest", "user"}
SUSPICIOUS_UA_KEYWORDS = ("python-requests", "curl", "wget", "scrapy", "bot")

PRIVATE_IPS = ("127.", "192.168.", "10.", "172.16.", "::1")


def get_location(ip_address: str) -> dict:
    """
    Calls ip-api.com to get the country and city for a given IP address.
    Returns a dict with 'country' and 'city'.
    Falls back to 'Unknown' if the IP is private or the API call fails.
    """
    if ip_address.startswith(PRIVATE_IPS):
        return {"country": "Unknown", "city": "Unknown"}

    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=5)
        data = response.json()

        if data.get("status") == "success":
            return {
                "country": data.get("country", "Unknown"),
                "city":    data.get("city",    "Unknown")
            }
        else:
            return {"country": "Unknown", "city": "Unknown"}

    except Exception as e:
        logging.warning(f"get_location failed for {ip_address}: {e}")
        return {"country": "Unknown", "city": "Unknown"}


def calculate_threat_score(ip: str, conn) -> int:
    """
    Returns a threat score from 0 to 100 for a given IP.
    Based on attempt frequency, recent burst, suspicious usernames,
    and automated User-Agent detection.
    """
    score = 0

    all_attempts = get_attempts_by_ip(ip)
    total        = len(all_attempts)

    # Frequency scoring — more attempts from this IP = higher score
    for threshold, points in COUNT_THRESHOLDS:
        if total > threshold:
            score += points

    # Burst scoring — spike of attempts in a short window
    recent = get_recent_attempts(ip, minutes=RECENT_WINDOW_MINUTES)
    if len(recent) > RECENT_BURST_THRESHOLD:
        score += RECENT_BURST_SCORE

    # Credential signal — repeatedly trying known default usernames
    suspicious_count = sum(
        1 for a in all_attempts
        if a.get("username", "").lower() in SUSPICIOUS_USERNAMES
    )
    if suspicious_count > SUSPICIOUS_USERNAME_THRESHOLD:
        score += SUSPICIOUS_USERNAME_SCORE

    # Behavioural signal — User-Agent looks like an automated tool
    user_agents = [a.get("user_agent", "").lower() for a in all_attempts]
    if any(keyword in ua for ua in user_agents for keyword in SUSPICIOUS_UA_KEYWORDS):
        score += BOT_UA_SCORE

    return min(score, 100)


def is_brute_force(ip: str, conn) -> bool:
    """
    Returns True if an IP has made more than 10 login attempts
    in the last 10 minutes — indicating automated brute force behaviour.
    """
    recent = get_recent_attempts(ip, minutes=BRUTE_FORCE_WINDOW_MINUTES)
    return len(recent) > BRUTE_FORCE_ATTEMPT_THRESHOLD