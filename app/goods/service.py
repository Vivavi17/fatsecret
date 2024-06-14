from app.exceptions import NotFoundException
from app.goods.dao import GoodsDao
from app.goods.schemas import SGoods, SNewGoods, SUpdateGoods


async def find_good_by_name(name: str) -> list[SGoods]:
    if not (goods := await GoodsDao.find_by_name(name)):
        raise NotFoundException
    return goods


async def add_good(data: SNewGoods) -> SGoods:
    if good := await GoodsDao.find_one_or_none(**data.model_dump()):
        return good
    return await GoodsDao.add_row(**data.model_dump())


async def update_good(product_id: int, data: SUpdateGoods) -> SGoods:
    data = data.model_dump(exclude_unset=True)
    return await GoodsDao.update_row(product_id, data)
