# 🐶 DogFit - AI 기반 강아지 맞춤 운동 추천 API

> AI Pet Trainer 프로젝트의 백엔드 API입니다.  
> FastAPI와 OpenAI를 활용해 강아지의 상태와 기구 보유 여부에 따라 **운동을 자동 추천하고 저장/조회할 수 있는 시스템**입니다.

---

## 🚀 주요 기능

| 기능 | 설명 |
|------|------|
| 🧠 `POST /recommend` | 강아지 정보를 입력하면 GPT-4를 통해 맞춤 운동 3가지를 추천합니다. |
| 📦 `GET /history` | 지금까지 추천된 강아지 운동 내역을 모두 조회합니다. |
| 🔍 `GET /recommendations/{id}` | 특정 추천 결과의 운동 이름, 추천 이유, 주의사항을 상세히 조회합니다. |
| 🐾 `GET /dogs` | 등록된 강아지 목록을 조회합니다. (보너스 기능) |

---

## 🛠 기술 스택

- **Python 3.10+**
- **FastAPI** - 경량 비동기 API 서버
- **SQLite3** - 내장형 로컬 데이터베이스
- **OpenAI API (GPT-4)** - 운동 추천 모델
- **Pydantic** - 데이터 검증
- **Uvicorn** - 서버 실행

---

## 📦 디렉토리 구조

📁 PythonProject14/ ├── db/ # SQLite DB 및 DB 관련 유틸 │ ├── dog_trainer.db │ ├── db_service.py │ └── models.py ├── routes/ # API 라우터 정의 │ ├── dog_routes.py │ ├── recommend_routes.py │ └── history_routes.py ├── openai_service.py # GPT 추천 호출 로직 ├── main.py # FastAPI 엔트리포인트 ├── .env # OpenAI API 키 저장 (gitignore) └── README.md # ← 이 파일


🔑 .env 파일 생성
OPENAI_API_KEY=sk-xxxxxxx...


▶️ 서버 실행
uvicorn main:app --reload

🔍 Swagger 문서 확인

http://localhost:8000/docs

✅ TODO (계속 확장 예정)
 운동 추천 기록 삭제 API

 특정 강아지별 추천 이력 필터링

 추천 즐겨찾기 기능

 React 프론트엔드 연동 (진행 중)

 PWA 앱 배포

👤 개발자
이름: 김주영

GitHub: @kimjuyoung1127

프로젝트명: DogFit / AI Pet Trainer


