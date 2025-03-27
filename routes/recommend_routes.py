from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Union
from openai_service import get_recommendation
import sqlite3
from db.db_service import save_recommendation_to_db

recommend_router = APIRouter()

# 🧠 요청 데이터 모델 정의
class RecommendRequest(BaseModel):
    dog_name: str
    breed: str
    age: int
    weight: float
    neutered: bool
    activity_level: str
    health_conditions: List[str]
    exercise_preferences: dict
    available_equipment: List[str]

# 🧠 응답이 JSON 형식일 수도 있고 그냥 문자열일 수도 있음
class RecommendResponse(BaseModel):
    recommendations: Union[List[dict], str]

# ✅ POST /recommend
@recommend_router.post("/recommend", response_model=RecommendResponse)
def recommend_exercises(request_data: RecommendRequest):
    try:
        result = get_recommendation(request_data)
        save_recommendation_to_db(request_data, result)
        return {"recommendations": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
