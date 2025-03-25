import sqlite3
from flask import Flask, g
from flask import request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
import json


app = Flask(__name__)

DATABASE = 'db/dog_trainer.db'

load_dotenv()
print("✅ API KEY:", os.getenv("OPENAI_API_KEY"))

client = OpenAI()




# DB 연결 함수
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# 간단한 테스트 API
@app.route('/dogs', methods=['GET'])
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

    return {"dogs": dogs}

@app.route('/dogs', methods=['POST'])
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
        int(data['neutered']),  # Boolean은 int로 처리 (True = 1, False = 0)
        data['activity_level'],
        data.get('health_conditions', ''),
        data.get('exercise_preferences', ''),
        data.get('available_equipment', '')
    ))

    db.commit()

    return {'message': '강아지 정보가 성공적으로 등록되었습니다!'}, 201


# openai api 호출
@app.route('/recommend', methods=['POST'])
def recommend_exercises():
    data = request.get_json()

    # 1. 입력 데이터 파싱
    dog_name = data.get('dog_name', '이름 없음')
    breed = data.get('breed', '알 수 없음')
    age = data.get('age', 0)
    weight = data.get('weight', 0.0)
    neutered = data.get('neutered', False)
    activity_level = data.get('activity_level', 'Medium')
    health_conditions = data.get('health_conditions', ['건강함'])
    exercise_preferences = data.get('exercise_preferences', {})
    available_equipment = data.get('available_equipment', [])

    # 2. 프롬프트 구성
    prompt = f"""
    아래는 강아지에 대한 정보입니다:

    - 이름: {dog_name}
    - 품종: {breed}
    - 나이: {age}살
    - 체중: {weight}kg
    - 중성화 여부: {'됨' if neutered else '안됨'}
    - 활동 수준: {activity_level}
    - 건강 상태: {', '.join(health_conditions)}
    - 운동 선호도: {exercise_preferences}
    - 보유 기구: {', '.join(available_equipment) if available_equipment else '없음'}

    위 정보를 바탕으로 이 강아지를 위한 피트니스 운동 3가지를 추천해줘.

    각 운동에 대해 다음과 같은 정보를 제공해줘:
    - 운동 이름
    - 해부학적, 운동학적 근거를 포함한 추천 이유
    - 보호자에게 줄 수 있는 주의사항 또는 피드백

    응답 형식은 반드시 JSON 배열로 해줘.
    """

    # 3. OpenAI 호출
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # gpt-3.5-turbo 도 가능
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=0.7,
            max_tokens=800
        )

        ai_response = response.choices[0].message.content.strip()

        # 🧪 응답 문자열을 JSON으로 파싱
        try:
            recommendations = json.loads(ai_response)
        except json.JSONDecodeError:
            # GPT가 JSON 형태로 응답하지 않았을 경우 문자열 그대로 전달
            recommendations = ai_response

        return jsonify({"recommendations": recommendations})

    except Exception as e:
        return jsonify({"error": str(e)}), 500





if __name__ == '__main__':
    app.run(debug=True)
