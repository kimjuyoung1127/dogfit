# db/init_db.py
import sqlite3

def init_db():
    conn = sqlite3.connect('db/dog_trainer.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dog_name TEXT NOT NULL,
            breed TEXT NOT NULL,
            gender TEXT NOT NULL,
            birth_date DATE NOT NULL,
            weight REAL NOT NULL,
            neutered BOOLEAN NOT NULL,
            activity_level TEXT NOT NULL,
            health_conditions TEXT,
            exercise_preferences TEXT,
            available_equipment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ dogs 테이블 생성 완료")

if __name__ == "__main__":
    init_db()
