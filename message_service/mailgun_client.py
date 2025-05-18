import os
import requests

def _read_secret(path):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except OSError:
        return None

# First, try ENV; if not set, fall back to the Docker Secret file
MAILGUN_API_KEY = (
    os.getenv("MAILGUN_API_KEY")
    or _read_secret(os.getenv("MAILGUN_API_KEY_FILE", "/run/secrets/mailgun_api_key"))
)
MAILGUN_DOMAIN = (
    os.getenv("MAILGUN_DOMAIN")
    or _read_secret(os.getenv("MAILGUN_DOMAIN_FILE", "/run/secrets/mailgun_domain"))
)

def send_simple_message(recv, message):
    print("Sending message to Mailgun...", flush=True)
    # Optional debug prints:
    print("MAILGUN_API_KEY:", "[redacted]" if MAILGUN_API_KEY else None, flush=True)
    print("MAILGUN_DOMAIN:", MAILGUN_DOMAIN, flush=True)

    return requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"Mailgun Sandbox <postmaster@{MAILGUN_DOMAIN}>",
            "to": recv,
            "subject": "MysticMail Message",
            "text": message
        }
    )
