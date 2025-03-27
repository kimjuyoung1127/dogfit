from fastapi import FastAPI
from dotenv import load_dotenv
import os
from routes.dog_routes import dog_router
from routes.recommend_routes import recommend_router
from db.db_service import create_recommendation_table
from routes.history_routes import history_router




create_recommendation_table()  # ✅ 서버 시작할 때 운동 추천 테이블도 같이 생성

# ✅ 환경변수 로딩
load_dotenv()
print("✅ API KEY:", os.getenv("OPENAI_API_KEY"))

# ✅ FastAPI 앱 초기화
app = FastAPI(
    title="AiPetTrainer",
    description="AI 기반 강아지 맞춤 운동 추천 API",
    version="1.0.0"
)

# ✅ 라우터 등록
app.include_router(dog_router)
app.include_router(recommend_router)

app.include_router(history_router) # history_routes

# ✅ DB 종료 연결 설정
@app.on_event("shutdown")
def shutdown_event():
    close_connection(None)
