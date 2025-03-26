
import sqlite3

DATABASE = 'db/dog_trainer.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db
