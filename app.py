from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_socketio import SocketIO
from twilio.rest import Client
import eventlet
import geopy.distance
import traceback
import os
import sqlite3
from dotenv import load_dotenv  # ✅ Load environment variables

# ✅ Load Twilio Credentials Securely
load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# ✅ Initialize Flask App
app = Flask(__name__, static_folder="static")
app.secret_key = "supersecretkey"

# ✅ Initialize WebSockets
socketio = SocketIO(app, async_mode="eventlet")

# ✅ Database Connection
DB_PATH = os.path.abspath("database.db")
print(f"📌 Database Path: {DB_PATH}")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# ✅ Serve Dashboard
@app.route("/")
def home():
    return render_template("index.html")  # Ensure "index.html" exists

@app.route('/login')
def login():
    return render_template('login.html')  # Ensure 'login.html' exists in 'templates/' folder

# ✅ Serve Static Files
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# ✅ API: Get All Bins
@app.route("/get-bins", methods=["GET"])
def get_bins():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bins")
    bins = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({"bins": bins})

# ✅ API: Update Bin Status & Notify Collector
@app.route("/update-bin", methods=["POST"])
def update_bin():
    try:
        data = request.get_json()
        bin_id = data["bin_id"]
        weight = data["weight"]
        location = data["location"]
        lat = data["latitude"]
        lng = data["longitude"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO bins (bin_id, weight, location, latitude, longitude, status)
            VALUES (?, ?, ?, ?, ?, 'Not Collected')
            ON CONFLICT(bin_id) DO UPDATE SET
                weight = excluded.weight,
                location = excluded.location,
                latitude = excluded.latitude,
                longitude = excluded.longitude;
            """,
            (bin_id, weight, location, lat, lng),
        )

        conn.commit()
        conn.close()

        # ✅ Emit real-time update
        socketio.emit("update_bin", {
            "bin_id": bin_id, "location": location, "weight": weight, "latitude": lat, "longitude": lng
        })

        # ✅ Optional WhatsApp Notification if weight > 40kg
        try:
            numeric_weight = float(weight.replace("kg", "").strip())
            if numeric_weight > 40:
                message_body = f"🚨 Bin {bin_id} at {location} is full! 📍 {lat}, {lng}"
                client.messages.create(
                    from_=TWILIO_WHATSAPP_NUMBER,
                    body=message_body,
                    to="whatsapp:+254758293126"  # Replace with the actual recipient number
                )
        except Exception as notify_error:
            print("⚠️ Failed to send WhatsApp message:", notify_error)

        return jsonify({"message": "Bin updated successfully!"}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500




# ✅ API: @app.route("/send-whatsapp", methods=["POST"])
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

# ✅ Start Flask Server
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

