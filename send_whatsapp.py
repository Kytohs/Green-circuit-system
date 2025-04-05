from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twilio credentials from .env
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

# Replace with your verified WhatsApp number
TO_WHATSAPP_NUMBER = "whatsapp:+1234567890"  # Change to your number

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Send WhatsApp message
message = client.messages.create(
    from_=TWILIO_WHATSAPP_NUMBER,
    body="Hello from Twilio via WhatsApp! 🚀",
    to=TO_WHATSAPP_NUMBER
)

print(f"✅ Message sent! SID: {message.sid}")
