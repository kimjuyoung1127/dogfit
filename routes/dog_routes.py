from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from db.db_utils import get_db
import sqlite3

dog_router = APIRouter()

# ✅ Pydantic 모델 정의
class Dog(BaseModel):
    dog_name: str
    breed: str
    gender: str
    birth_date: str
    weight: float
    neutered: bool
    activity_level: str
    health_conditions: str = ""
    exercise_preferences: str = ""
    available_equipment: str = ""

# ✅ GET /dogs
@dog_router.get("/dogs")
def get_dogs(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM dogs")
    rows = cursor.fetchall()

    dogs = []
    for row in rows:
        dogs.append({
            "id": row["id"],
            "dog_name": row["dog_name"],
            "breed": row["breed"],
            "gender": row["gender"],
            "birth_date": row["birth_date"],
            "weight": row["weight"],
            "neutered": bool(row["neutered"]),
            "activity_level": row["activity_level"],
            "health_conditions": row["health_conditions"],
            "exercise_preferences": row["exercise_preferences"],
            "available_equipment": row["available_equipment"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"]
        })

    return {"dogs": dogs}

# ✅ POST /dogs
@dog_router.post("/dogs")
def add_dog(dog: Dog, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()

    cursor.execute('''
        INSERT INTO dogs (
            dog_name, breed, gender, birth_date, weight, neutered, activity_level,
            health_conditions, exercise_preferences, available_equipment
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        dog.dog_name,
        dog.breed,
        dog.gender,
        dog.birth_date,
        dog.weight,
        int(dog.neutered),
        dog.activity_level,
        dog.health_conditions,
        dog.exercise_preferences,
        dog.available_equipment
    ))

    db.commit()

    return JSONResponse(content={"message": "강아지 정보가 성공적으로 등록되었습니다!"}, status_code=201)
