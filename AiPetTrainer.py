from flask import Flask
from dotenv import load_dotenv
from db.db_utils import close_connection
from routes.dog_routes import dog_bp
from routes.recommend_routes import recommend_bp
import os

# 환경변수 로딩
load_dotenv()

# Flask 앱 초기화
app = Flask(__name__)

# 블루프린트 등록
app.register_blueprint(dog_bp)
app.register_blueprint(recommend_bp)

# DB 연결 종료 설정
app.teardown_appcontext(close_connection)

if __name__ == '__main__':
    print("✅ API KEY:", os.getenv("OPENAI_API_KEY"))
    app.run(debug=True)
