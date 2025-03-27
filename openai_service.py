from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def get_recommendation(data):
    prompt = f"""
    아래는 강아지에 대한 정보입니다:

    - 이름: {data.dog_name}
    - 품종: {data.breed}
    - 나이: {data.age}살
    - 체중: {data.weight}kg
    - 중성화 여부: {'됨' if data.neutered else '안됨'}
    - 활동 수준: {data.activity_level}
    - 건강 상태: {', '.join(data.health_conditions)}
    - 운동 선호도: {data.exercise_preferences}
    - 보유 기구: {', '.join(data.available_equipment) if data.available_equipment else '없음'}

    위 정보를 바탕으로 이 강아지를 위한 피트니스 운동 3가지를 추천해줘.

    각 운동에 대해 다음과 같은 정보를 제공해줘:
    - 운동 이름
    - 해부학적, 운동학적 근거를 포함한 추천 이유
    - 보호자에게 줄 수 있는 주의사항 또는 피드백

    응답 형식은 반드시 JSON 배열로 해줘.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=800
    )

    ai_response = response.choices[0].message.content.strip()

    try:
        return json.loads(ai_response)
    except json.JSONDecodeError:
        return ai_response
