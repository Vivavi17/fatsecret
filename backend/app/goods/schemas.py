from typing import Optional

from pydantic import BaseModel


class SUpdateGoods(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    proteins: Optional[int] = None
    fats: Optional[int] = None
    carbohydrates: Optional[int] = None
    kcal: Optional[int] = None


class SNewGoods(BaseModel):
    name: str
    brand: str | None = None
    proteins: int = 0
    fats: int = 0
    carbohydrates: int = 0
    kcal: int = 0


class SGoods(SNewGoods):
    id: int
