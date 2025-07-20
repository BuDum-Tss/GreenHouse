from fastapi import APIRouter
from pydantic import BaseModel
import logging

from src.depends import get_db_connection, get_recommendation_agent

router = APIRouter(prefix="/users", tags=["users"])

class UserRequest(BaseModel):
    id: str
    restrictions: str

@router.post("")
def create_user(user_request: UserRequest):
    with get_db_connection() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_request.id,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            # Обновляем существующего пользователя
            cursor.execute(
                "UPDATE users SET restrictions = ? WHERE user_id = ?",
                (user_request.restrictions, user_request.id)
            )
            logging.info("User updated successfully")
        else:
            # Создаем нового пользователя
            cursor.execute(
                "INSERT INTO users (user_id, restrictions) VALUES (?, ?)",
                (user_request.id, user_request.restrictions)
            )
            logging.info("User created successfully")
        db.commit()
