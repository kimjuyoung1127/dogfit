# 추천 운동 결과 조회 db 서비스

import sqlite3
import json
from datetime import datetime

DB_PATH = "db/dog_trainer.db"

def create_recommendation_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dog_name TEXT,
            breed TEXT,
            age INTEGER,
            weight REAL,
            health_conditions TEXT,
            recommendation_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_recommendation_to_db(request_data, recommendations):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO recommendations (
            dog_name, breed, age, weight, health_conditions,
            recommendation_json, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        request_data.dog_name,
        request_data.breed,
        request_data.age,
        request_data.weight,
        ",".join(request_data.health_conditions),
        json.dumps(recommendations, ensure_ascii=False),
        datetime.now()
    ))

    conn.commit()
    conn.close()
