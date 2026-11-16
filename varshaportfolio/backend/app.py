from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Backend is Running Successfully!"

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, request, jsonify, send_from_directory
import sqlite3
from pathlib import Path

app = Flask(
    __name__,
    static_folder="../frontend",
    static_url_path=""
)

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "portfolio.db"


# Database Connection
def get_connection():
    return sqlite3.connect(DATABASE)


# Create Database Table
def create_table():

    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Home Page
@app.route("/")
def home():
    return send_from_directory(
        app.static_folder, "index.html"
    )


# Contact API
@app.route("/api/contact", methods=["POST"])
def contact():

    data = request.get_json(silent=True) or {}

    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    message = str(data.get("message", "")).strip()

    if not name or not email or not message:
        return jsonify({
            "error": "Please fill all fields."
        }), 400

    if len(name) > 100 or len(email) > 254 or len(message) > 3000:
        return jsonify({
            "error": "Input is too long."
        }), 400

    conn = get_connection()

    conn.execute(
        "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
        (name, email, message)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Thank you! Your message has been received."
    }), 201


if __name__ == "__main__":

    create_table()

    app.run(debug=True)
