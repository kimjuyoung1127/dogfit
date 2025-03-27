from fastapi import APIRouter, HTTPException
import sqlite3
import json

history_router = APIRouter()

# ✅ 전체 추천 이력 조회
@history_router.get("/history")
def get_recommendation_history():
    conn = sqlite3.connect("db/dog_trainer.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, dog_name, breed, created_at
        FROM recommendations
        ORDER BY created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "dog_name": row[1],
            "breed": row[2],
            "created_at": row[3]
        }
        for row in rows
    ]

# ✅ 개별 추천 상세 조회
@history_router.get("/recommendations/{recommendation_id}")
def get_recommendation_detail(recommendation_id: int):
    conn = sqlite3.connect("db/dog_trainer.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM recommendations WHERE id = ?", (recommendation_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="추천 기록을 찾을 수 없습니다.")

    try:
        recommendation_data = json.loads(row["recommendation_json"])
    except json.JSONDecodeError:
        recommendation_data = row["recommendation_json"]

    return {
        "id": row["id"],
        "dog_name": row["dog_name"],
        "breed": row["breed"],
        "created_at": row["created_at"],
        "recommendation": recommendation_data
    }
