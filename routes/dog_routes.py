from flask import Blueprint, request, jsonify
from db.db_utils import get_db

dog_bp = Blueprint('dog', __name__)

@dog_bp.route('/dogs', methods=['GET'])
def get_dogs():
    db = get_db()
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

    return jsonify({"dogs": dogs})


@dog_bp.route('/dogs', methods=['POST'])
def add_dog():
    data = request.get_json()

    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
        INSERT INTO dogs (
            dog_name, breed, gender, birth_date, weight, neutered, activity_level,
            health_conditions, exercise_preferences, available_equipment
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['dog_name'],
        data['breed'],
        data['gender'],
        data['birth_date'],
        data['weight'],
        int(data['neutered']),
        data['activity_level'],
        data.get('health_conditions', ''),
        data.get('exercise_preferences', ''),
        data.get('available_equipment', '')
    ))

    db.commit()

    return {'message': '강아지 정보가 성공적으로 등록되었습니다!'}, 201
