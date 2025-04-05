from dotenv import load_dotenv
import os

# Load environment variables
dotenv_loaded = load_dotenv()
print(f"Loaded .env: {dotenv_loaded}")

# Print values
print("TWILIO_ACCOUNT_SID:", os.getenv("TWILIO_ACCOUNT_SID"))
print("TWILIO_AUTH_TOKEN:", os.getenv("TWILIO_AUTH_TOKEN"))
print("TWILIO_WHATSAPP_NUMBER:", os.getenv("TWILIO_WHATSAPP_NUMBER"))
