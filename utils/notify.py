from twilio.rest import Client
import json

# Load Twilio API credentials from config.json
with open("config.json") as f:
    config = json.load(f)

account_sid = config["twilio_sid"]
auth_token = config["twilio_token"]
client = Client(account_sid, auth_token)

# Function to send an SMS to the nearest collector
def send_sms_notification(collector_phone, bin_id, location):
    message = client.messages.create(
        body=f"🚨 Alert: Bin {bin_id} at {location} is full. Please collect it ASAP!",
        from_=config["twilio_phone"],
        to=collector_phone
    )
    print(f"Notification sent to {collector_phone}: {message.sid}")
