
from pydantic import BaseModel



class Dog(BaseModel):
    dog_name: str
    breed: str
    gender: str
    birth_date: str
    weight: float
    neutered: bool
    activity_level: str
    health_conditions: str = ""
    exercise_preferences: str = ""
    available_equipment: str = ""
