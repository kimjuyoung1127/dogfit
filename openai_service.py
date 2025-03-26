import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def generate_exercise_recommendations(data):
    dog_name = data.get('dog_name', '이름 없음')
    breed = data.get('breed', '알 수 없음')
    age = data.get('age', 0)
    weight = data.get('weight', 0.0)
    neutered = data.get('neutered', False)
    activity_level = data.get('activity_level', 'Medium')
    health_conditions = data.get('health_conditions', ['건강함'])
    exercise_preferences = data.get('exercise_preferences', {})
    available_equipment = data.get('available_equipment', [])

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

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=0.7,
            max_tokens=800
        )

        ai_response = response.choices[0].message.content.strip()

        try:
            return json.loads(ai_response)
        except json.JSONDecodeError:
            return ai_response

    except Exception as e:
        return {"error": str(e)}
