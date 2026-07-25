import sqlite3
import pandas as pd
import json
import os

DB_NAME = "users.db"

def init_history_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            user TEXT,
            patient_name TEXT,
            risk_level TEXT,
            health_score INTEGER,
            parameters_json TEXT
        )
    """)
    conn.commit()
    conn.close()

# Initialize table automatically
init_history_db()

# ─────────────────────────────────────────────
# Save History
# ─────────────────────────────────────────────

def save_history(data):
    init_history_db()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    date_str = str(data.get("date", pd.Timestamp.now()))
    user = data.get("user", "")
    patient_name = data.get("patient_name", "")
    risk_level = data.get("risk_level", "")
    health_score = data.get("health_score", 0)

    # Extract parameters
    params = {
        k: v for k, v in data.items()
        if k not in ["date", "user", "patient_name", "risk_level", "health_score"]
    }

    parameters_json = json.dumps(params)

    c.execute("""
        INSERT INTO history (date, user, patient_name, risk_level, health_score, parameters_json)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date_str, user, patient_name, risk_level, health_score, parameters_json))

    conn.commit()
    conn.close()

# ─────────────────────────────────────────────
# Load User History
# ─────────────────────────────────────────────

def load_history(username=None):
    init_history_db()
    conn = sqlite3.connect(DB_NAME)
    
    if username:
        df_raw = pd.read_sql_query(
            "SELECT date, user, patient_name, risk_level, health_score, parameters_json FROM history WHERE user=?",
            conn,
            params=(username,)
        )
    else:
        df_raw = pd.read_sql_query(
            "SELECT date, user, patient_name, risk_level, health_score, parameters_json FROM history",
            conn
        )
    conn.close()

    if df_raw.empty:
        return pd.DataFrame()

    records = []
    for _, row in df_raw.iterrows():
        rec = {
            "date": row["date"],
            "user": row["user"],
            "patient_name": row["patient_name"],
            "risk_level": row["risk_level"],
            "health_score": row["health_score"]
        }
        try:
            params = json.loads(row["parameters_json"])
            rec.update(params)
        except Exception:
            pass
        records.append(rec)

    return pd.DataFrame(records)