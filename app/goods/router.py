from fastapi import APIRouter

from app.goods.schemas import SGoods, SNewGoods, SUpdateGoods
from app.goods.service import add_good, find_good_by_name, update_good

router = APIRouter(prefix="/goods", tags=["Goods"])


@router.get("")
async def find_good(name: str) -> list[SGoods]:
    return await find_good_by_name(name)


@router.post("", status_code=201)
async def add_item(data: SNewGoods) -> SGoods:
    return await add_good(data)


@router.patch("/{product_id}", status_code=200)
async def update_item(product_id: int, data: SUpdateGoods) -> SGoods:
    return await update_good(product_id, data)
