from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_socketio import SocketIO
from twilio.rest import Client
import eventlet
import traceback
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

# ✅ Load environment variables
load_dotenv()

# ✅ Twilio Credentials
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# ✅ Flask App Setup
app = Flask(__name__, static_folder="static")
app.secret_key = "supersecretkey"

# ✅ PostgreSQL Config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ✅ WebSockets
socketio = SocketIO(app, async_mode="eventlet")

# ✅ Bin Model
class Bin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bin_id = db.Column(db.String, unique=True, nullable=False)
    weight = db.Column(db.String)
    location = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    status = db.Column(db.String)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route("/get-bins", methods=["GET"])
def get_bins():
    bins = Bin.query.all()
    bin_data = [
        {
            "id": b.id,
            "bin_id": b.bin_id,
            "weight": b.weight,
            "location": b.location,
            "latitude": b.latitude,
            "longitude": b.longitude,
            "status": b.status
        } for b in bins
    ]
    return jsonify({"bins": bin_data})

@app.route("/update-bin", methods=["POST"])
def update_bin():
    try:
        data = request.get_json()
        bin_obj = Bin.query.filter_by(bin_id=data["bin_id"]).first()

        if not bin_obj:
            bin_obj = Bin(bin_id=data["bin_id"])
            db.session.add(bin_obj)

        bin_obj.weight = data["weight"]
        bin_obj.location = data["location"]
        bin_obj.latitude = data["latitude"]
        bin_obj.longitude = data["longitude"]
        bin_obj.status = "Not Collected"
        db.session.commit()

        socketio.emit("update_bin", {
            "bin_id": bin_obj.bin_id,
            "location": bin_obj.location,
            "weight": bin_obj.weight,
            "latitude": bin_obj.latitude,
            "longitude": bin_obj.longitude
        })

        try:
            numeric_weight = float(bin_obj.weight.replace("kg", "").strip())
            if numeric_weight > 40:
                message_body = f"🚨 Bin {bin_obj.bin_id} at {bin_obj.location} is full! 📍 {bin_obj.latitude}, {bin_obj.longitude}"
                client.messages.create(
                    from_=TWILIO_WHATSAPP_NUMBER,
                    body=message_body,
                    to="whatsapp:+254758293126"
                )
        except Exception as notify_error:
            print("⚠️ Failed to send WhatsApp message:", notify_error)

        return jsonify({"message": "Bin updated successfully!"}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/send-whatsapp", methods=["POST"])
def send_whatsapp():
    try:
        data = request.get_json()
        to_number = data.get("to")
        message_body = data.get("message")

        if not to_number or not message_body:
            return jsonify({"error": "Missing 'to' or 'message'"}), 400

        message = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=message_body,
            to=to_number
        )

        return jsonify({"status": "Message sent", "sid": message.sid}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# ✅ Auto-create tables
with app.app_context():
    db.create_all()

# ✅ Run the app
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
