from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
	return "Server is running"

@app.route("/account", methods=["GET"])
def account():
    username = request.args.get("username")
    password = request.args.get("password")

    conn = sqlite3.connect("DATA.db")
    db = conn.cursor()

    db.execute('''
    CREATE TABLE IF NOT EXISTS account (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    db.execute("INSERT INTO account (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

    return jsonify({"code": "200"})

@app.route("/chndtr", methods=["GET"])
def chndtr():
    conn = sqlite3.connect("DATA.db")
    db = conn.cursor()

    db.execute("SELECT * FROM account")
    rows = db.fetchall()

    db.close()
    conn.close()

    items = [{"id": row[0], "username": row[1], "password": row[2]} for row in rows]

    return jsonify({"items": items})
    

if __name__ == "__main__":
    app.run(debug=True)