import os
import requests

API_KEY = os.environ.get("BREVO_API_KEY")
FROM_EMAIL = os.environ.get("BREVO_SENDER")

def send_real_email(receiver, message_text):
    url = "https://api.brevo.com/v3/smtp/email"
    payload = {
        "sender": {"name": "MysticMail", "email": FROM_EMAIL},
        "to": [{"email": receiver}],
        "subject": "✨ MysticMail - You've got a message!",
        "htmlContent": f"<p>{message_text}</p>"
    }
    headers = {
        "accept": "application/json",
        "api-key": API_KEY,
        "content-type": "application/json"
    }

    try:
        print(f"[📧 EMAIL REAL] Trimit către {receiver}: {message_text}")
        r = requests.post(url, json=payload, headers=headers)
        print(f"[✅] Răspuns Brevo: {r.status_code} | {r.json()}")
        if r.status_code in [200, 201, 202]:
            return {
                "status": "sent",
                "receiver": receiver,
                "note": "Email trimis cu succes prin Brevo!"
            }
        else:
            return {
                "status": "error",
                "code": r.status_code,
                "response": r.json()
            }
    except Exception as e:
        print(f"[❌] Eroare la trimitere: {e}")
        return {
            "status": "failed",
            "error": str(e)
        }
