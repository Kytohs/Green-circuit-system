from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from twilio.rest import Client
from dotenv import load_dotenv
from waitress import serve
from functools import wraps
import traceback
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Twilio Setup
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Flask App Setup
app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ============================ MODELS ============================
class Bin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bin_id = db.Column(db.String, unique=True, nullable=False)
    weight = db.Column(db.String)
    location = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    status = db.Column(db.String)

class Collector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    whatsapp = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class NotificationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    collector_id = db.Column(db.Integer, db.ForeignKey('collector.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# ============================ HELPERS ============================
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = User.query.get(session.get("user_id"))
        if not user or not user.is_admin:
            flash("Admin access only!", "danger")
            return redirect(url_for("home"))
        return f(*args, **kwargs)
    return decorated

# ============================ ROUTES ============================
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            flash("Logged in successfully!", "success")
            return redirect(url_for("home"))
        flash("Invalid username or password", "danger")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if User.query.filter_by(username=username).first():
            flash("Username already exists", "warning")
            return redirect(url_for("register"))

        if User.query.filter_by(is_admin=True).count() >= 3:
            flash("Admin limit reached. Cannot register more admins.", "danger")
            return redirect(url_for("register"))

        new_user = User(username=username, is_admin=True)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("Admin registered successfully. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Logged out.", "info")
    return redirect(url_for("login"))

@app.route("/admin/collectors")
@admin_required
def admin_collectors():
    collectors = Collector.query.all()
    return render_template("admin_collectors.html", collectors=collectors)

@app.route("/edit-collector/<int:id>", methods=["GET", "POST"])
@admin_required
def edit_collector(id):
    collector = Collector.query.get_or_404(id)
    if request.method == 'POST':
        collector.name = request.form.get('name')
        collector.whatsapp = request.form.get('whatsapp')
        db.session.commit()
        flash("Collector updated!", "success")
        return redirect(url_for('admin_collectors'))
    return render_template('edit_collector.html', collector=collector)

@app.route("/delete-collector/<int:id>", methods=["POST"])
@admin_required
def delete_collector(id):
    collector = Collector.query.get_or_404(id)
    db.session.delete(collector)
    db.session.commit()
    flash("Collector deleted.", "info")
    return redirect(url_for('admin_collectors'))

@app.route("/register-collector", methods=["POST"])
@admin_required
def register_collector():
    name = request.form.get("name")
    whatsapp = request.form.get("whatsapp")
    if not name or not whatsapp:
        return jsonify({"error": "Missing fields"}), 400
    new_collector = Collector(name=name, whatsapp=whatsapp)
    db.session.add(new_collector)
    db.session.commit()
    return jsonify({"message": "Collector registered"}), 200

@app.route("/notify-all", methods=["POST"])
@admin_required
def notify_all_collectors():
    try:
        data = request.get_json()
        message = data.get("message")
        if not message:
            return jsonify({"error": "Message is required"}), 400

        collectors = Collector.query.all()
        for collector in collectors:
            client.messages.create(
                from_=TWILIO_WHATSAPP_NUMBER,
                body=message,
                to=f"whatsapp:{collector.whatsapp}"
            )
            db.session.add(NotificationLog(collector_id=collector.id, message=message))

        db.session.commit()
        return jsonify({"message": "Notifications sent"}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/logs")
@admin_required
def view_logs():
    logs = NotificationLog.query.order_by(NotificationLog.timestamp.desc()).limit(10).all()
    return jsonify({
        "logs": [
            {
                "collector": Collector.query.get(log.collector_id).name,
                "message": log.message,
                "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            } for log in logs
        ]
    })

@app.route("/get-bins", methods=["GET"])
def get_bins():
    bins = Bin.query.all()
    return jsonify({
        "bins": [
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
    })

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

        weight_val = float(bin_obj.weight.replace("kg", "").strip())
        if weight_val > 40:
            message = f"🚨 Bin {bin_obj.bin_id} at {bin_obj.location} is full!\n📍 {bin_obj.latitude}, {bin_obj.longitude}"
            for collector in Collector.query.all():
                client.messages.create(
                    from_=TWILIO_WHATSAPP_NUMBER,
                    body=message,
                    to=f"whatsapp:{collector.whatsapp}"
                )
                db.session.add(NotificationLog(collector_id=collector.id, message=message))
            db.session.commit()

        return jsonify({"message": "Bin updated"}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# ============================ INIT DB ============================
with app.app_context():
    db.create_all()

# ============================ RUN ============================
if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
