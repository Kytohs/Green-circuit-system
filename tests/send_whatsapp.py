from flask import Flask, request, jsonify
from twilio.rest import Client
import os
from dotenv import load_dotenv

# ✅ Initialize Flask app
app = Flask(__name__)

# ✅ Load environment variables
load_dotenv()

# ✅ Twilio Credentials from .env
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

# ✅ Initialize Twilio Client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
TO_WHATSAPP_NUMBER = "whatsapp:+254758293126"  # <-- Your verified WhatsApp number

@app.route('/send-whatsapp', methods=['POST'])
def send_whatsapp():
    try:
        data = request.get_json()

        to_number = data.get("to")  # e.g., "whatsapp:+1234567890"
        message_body = data.get("message", "Hello from Twilio WhatsApp!")

        if not to_number:
            return jsonify({"error": "Missing 'to' field"}), 400

        message = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=message_body,
            to=to_number
        )

        return jsonify({"message": "WhatsApp sent successfully!", "sid": message.sid})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
