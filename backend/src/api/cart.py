from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from src.depends import get_db_connection

router = APIRouter(prefix="/cart", tags=["cart"])

class CartItem(BaseModel):
    product_id: int
    quantity: int

# Добавить продукт в корзину
@router.post("/add")
def add_to_cart(item: CartItem):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Здесь логика добавления, например:
        # Проверяем есть ли продукт уже в корзине
        cursor.execute("SELECT quantity FROM cart WHERE product_id = ?", (item.product_id,))
        row = cursor.fetchone()
        if row:
            new_quantity = row["quantity"] + item.quantity
            cursor.execute("UPDATE cart SET quantity = ? WHERE product_id = ?", (new_quantity, item.product_id))
        else:
            cursor.execute("INSERT INTO cart (product_id, quantity) VALUES (?, ?)", (item.product_id, item.quantity))
        conn.commit()
    return {"message": "Product added to cart"}

# Удалить продукт из корзины
@router.delete("/remove/{product_id}")
def remove_from_cart(product_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart WHERE product_id = ?", (product_id,))
        conn.commit()
    return {"message": "Product removed from cart"}
