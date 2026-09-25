import math
from datetime import datetime

import pymysql
from flask import Flask, g, jsonify, render_template, request

app = Flask(__name__)

DB_CONFIG = dict(
    host="localhost",
    user="root",
    password="bms@123",
    database="parking_db",
    cursorclass=pymysql.cursors.DictCursor,
)
RATES = {"bike": 10, "car": 30}          # ₹ per hour, minimum 1 hour
LAYOUT = [("B", "bike", 8), ("C", "car", 16)]


def db():
    if "db" not in g:
        g.db = pymysql.connect(**DB_CONFIG)
    return g.db


@app.teardown_appcontext
def close_db(_):
    conn = g.pop("db", None)
    if conn:
        conn.close()


def query(sql, args=(), one=False):
    with db().cursor() as cur:
        cur.execute(sql, args)
        return cur.fetchone() if one else cur.fetchall()


def run(sql, args=()):
    conn = db()
    with conn.cursor() as cur:
        cur.execute(sql, args)
    conn.commit()


def iso(rows):
    """Turn datetime values into ISO strings so JSON and JS can read them."""
    for r in rows:
        for k in ("entry_time", "exit_time"):
            if r.get(k):
                r[k] = r[k].isoformat()
    return rows


def init_db():
    cfg = {k: v for k, v in DB_CONFIG.items() if k != "database"}
    conn = pymysql.connect(**cfg)
    with conn.cursor() as cur:
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}`")
        cur.execute(f"USE `{DB_CONFIG['database']}`")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS slots(
                id INT AUTO_INCREMENT PRIMARY KEY,
                label VARCHAR(10) UNIQUE,
                type VARCHAR(10))""")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tickets(
                id INT AUTO_INCREMENT PRIMARY KEY,
                plate VARCHAR(20),
                type VARCHAR(10),
                slot_id INT,
                entry_time DATETIME,
                exit_time DATETIME NULL,
                fee INT NULL,
                FOREIGN KEY (slot_id) REFERENCES slots(id))""")
        cur.execute("SELECT COUNT(*) AS n FROM slots")
        if cur.fetchone()["n"] == 0:
            for prefix, vtype, n in LAYOUT:
                for i in range(1, n + 1):
                    cur.execute("INSERT INTO slots(label, type) VALUES(%s, %s)",
                                (f"{prefix}{i}", vtype))
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html", rates=RATES)


@app.get("/api/slots")
def slots():
    rows = query("""
        SELECT s.id, s.label, s.type, t.id AS ticket_id, t.plate, t.entry_time
        FROM slots s LEFT JOIN tickets t
          ON t.slot_id = s.id AND t.exit_time IS NULL
        ORDER BY s.id""")
    return jsonify(iso(rows))


@app.post("/api/park")
def park():
    data = request.get_json(force=True)
    plate = (data.get("plate") or "").strip().upper()
    vtype = data.get("type")
    if not plate or vtype not in RATES:
        return jsonify(error="Enter a plate number and pick a vehicle type."), 400
    if query("SELECT 1 FROM tickets WHERE plate=%s AND exit_time IS NULL",
             (plate,), one=True):
        return jsonify(error=f"{plate} is already parked."), 409
    slot = query("""
        SELECT id, label FROM slots WHERE type=%s AND id NOT IN
        (SELECT slot_id FROM tickets WHERE exit_time IS NULL)
        ORDER BY id LIMIT 1""", (vtype,), one=True)
    if not slot:
        return jsonify(error=f"No free {vtype} bays."), 409
    run("INSERT INTO tickets(plate, type, slot_id, entry_time) VALUES(%s,%s,%s,%s)",
        (plate, vtype, slot["id"], datetime.now()))
    return jsonify(message=f"{plate} assigned to bay {slot['label']}.")


@app.post("/api/exit/<int:ticket_id>")
def checkout(ticket_id):
    t = query("SELECT * FROM tickets WHERE id=%s AND exit_time IS NULL",
              (ticket_id,), one=True)
    if not t:
        return jsonify(error="Ticket not found or already closed."), 404
    now = datetime.now()
    hours = max(1, math.ceil((now - t["entry_time"]).total_seconds() / 3600))
    fee = hours * RATES[t["type"]]
    run("UPDATE tickets SET exit_time=%s, fee=%s WHERE id=%s", (now, fee, ticket_id))
    return jsonify(message=f"{t['plate']} checked out. {hours} h billed: ₹{fee}.")


@app.get("/api/history")
def history():
    rows = query("""
        SELECT t.plate, t.type, s.label AS bay, t.entry_time, t.exit_time, t.fee
        FROM tickets t JOIN slots s ON s.id = t.slot_id
        WHERE t.exit_time IS NOT NULL ORDER BY t.id DESC LIMIT 15""")
    total = query("SELECT COALESCE(SUM(fee), 0) AS total FROM tickets "
                  "WHERE DATE(exit_time) = CURDATE()", one=True)["total"]
    return jsonify(rows=iso(rows), revenue_today=int(total))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)