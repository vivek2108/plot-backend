import os

import requests

# Fetch API key from environment or a secure place
MSG91_API_KEY = os.getenv("MSG91_API_KEY")  # Store your MSG91 API key here securely
MSG91_SENDER_ID = os.getenv("MSG91_SENDER_ID")  # Set your sender ID


def send_sms(msg: str, phone_number: str):
    url = "https://api.msg91.com/api/v5/otp"
    headers = {"Content-Type": "application/json"}

    data = {
        "authkey": MSG91_API_KEY,
        "sender": MSG91_SENDER_ID,
        "route": "4",  # Route 4 is for transactional SMS
        "country": "91",  # India country code
        "sms": [{"message": msg, "to": [phone_number]}],
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Exception in sending SMS: {e}")
        return None
