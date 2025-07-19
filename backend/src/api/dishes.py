from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, List
from pydantic import BaseModel
import sqlite3

from src.agent import AgentState, Metadata, RecommendationAgent
from src.depends import get_db_connection, get_recommendation_agent

router = APIRouter(prefix="/dishes", tags=["dishes"])

class Dish(BaseModel):
    id: str
    name: str
    price: float
    tags: list[str]

@router.get("/{user_id}")
def get_dishes(user_id: str,
            prompt: Optional[str] = Query(None),
            tags: Optional[List[str]] = Query(None),
            agent: RecommendationAgent = Depends(get_recommendation_agent)) -> list[Dish]:
    """Рекоммендация"""
    if prompt == None or prompt == "":
        return get_all_dishes()
    else:
        ids: list[str] = agent.process(AgentState(user_id=user_id, message=prompt, metadata=Metadata(tags=tags)))
        return get_dishes_by_ids(ids)

def get_all_dishes() -> List[Dish]:
    with get_db_connection() as db:  # Укажите имя вашей БД
        cursor = db.cursor()
        
        # Получаем все блюда
        cursor.execute("""
            SELECT id, name, price FROM dishes
        """)
        dishes_data = cursor.fetchall()
        
        dishes = []
        for dish_id, name, price in dishes_data:
            # Получаем теги для текущего блюда
            cursor.execute("""
                SELECT t.name 
                FROM tags t
                JOIN dish_tags dt ON t.id = dt.tag_id
                WHERE dt.dish_id = ?
            """, (dish_id,))
            tags = [tag[0] for tag in cursor.fetchall()]
            
            # Создаем объект Dish и добавляем в список
            dishes.append(Dish(
                id=str(dish_id),  # Конвертируем в str, если в модели указан строковый тип
                name=name,
                price=price,
                tags=tags
            ))
        
        return dishes

def get_dishes_by_ids(ids: List[str]) -> List[Dish]:
    if not ids:
        return []
    
    with get_db_connection() as db:
        cursor = db.cursor()
        
        dish_ids = [int(id_) for id_ in ids]
        placeholders = ','.join('?' for _ in dish_ids)
        
        # Получаем все блюда и их теги одним запросом
        cursor.execute(f"""
            SELECT d.id, d.name, d.price, t.name
            FROM dishes d
            LEFT JOIN dish_tags dt ON d.id = dt.dish_id
            LEFT JOIN tags t ON dt.tag_id = t.id
            WHERE d.id IN ({placeholders})
        """, dish_ids)
        
        # Группируем результаты
        dishes_dict = {}
        for row in cursor.fetchall():
            dish_id, name, price, tag_name = row
            if dish_id not in dishes_dict:
                dishes_dict[dish_id] = {
                    'id': str(dish_id),
                    'name': name,
                    'price': price,
                    'tags': []
                }
            if tag_name:  # Если есть тег, добавляем его
                dishes_dict[dish_id]['tags'].append(tag_name)
        
        return [Dish(**dish) for dish in dishes_dict.values()]


# === DEPRECATED ===

class DishCreate(BaseModel):
    name: str
    price: float
    ingredients: List[str]
    tags: List[str]

@router.post("/", status_code=201, description="DEPRECATED - был использован для заполнения бд")
async def create_dish(dish: DishCreate):
    """"""
    try:
        with get_db_connection() as db:
            cursor = db.cursor()
            cursor.execute("BEGIN TRANSACTION")
            
            # 1. Добавляем блюдо
            cursor.execute(
                "INSERT INTO dishes (name, price) VALUES (?, ?)",
                (dish.name, dish.price)
            )
            dish_id = cursor.lastrowid
            
            # 2. Обрабатываем ингредиенты
            for ingredient_name in dish.ingredients:
                # Добавляем ингредиент если его нет
                cursor.execute(
                    "INSERT OR IGNORE INTO ingredients (name) VALUES (?)",
                    (ingredient_name.lower(),)
                )
                
                # Получаем ID ингредиента
                ingredient_row = cursor.execute(
                    "SELECT id FROM ingredients WHERE name = ?",
                    (ingredient_name.lower(),)
                ).fetchone()
                
                if not ingredient_row:
                    db.rollback()
                    raise HTTPException(status_code=400, detail=f"Ingredient {ingredient_name} not found after insert")
                
                ingredient_id = ingredient_row['id']
                
                # Связываем с блюдом
                cursor.execute(
                    "INSERT INTO dish_ingredients (dish_id, ingredient_id) VALUES (?, ?)",
                    (dish_id, ingredient_id)
                )
            
            # 3. Обрабатываем теги
            for tag_name in dish.tags:
                # Добавляем тег если его нет
                cursor.execute(
                    "INSERT OR IGNORE INTO tags (name) VALUES (?)",
                    (tag_name.lower(),)
                )
                
                # Получаем ID тега
                tag_row = cursor.execute(
                    "SELECT id FROM tags WHERE name = ?",
                    (tag_name.lower(),)
                ).fetchone()
                
                if not tag_row:
                    db.rollback()
                    raise HTTPException(status_code=400, detail=f"Tag {tag_name} not found after insert")
                
                tag_id = tag_row['id']
                
                # Связываем с блюдом
                cursor.execute(
                    "INSERT INTO dish_tags (dish_id, tag_id) VALUES (?, ?)",
                    (dish_id, tag_id)
                )
            
            db.commit()
            return {"status": "success", "dish_id": dish_id}
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))