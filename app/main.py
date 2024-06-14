import sys

import uvicorn
from fastapi import FastAPI

sys.path.append(".")
from app.goods.router import router as router_goods  # noqa
from app.journal.router import router as router_journal  # noqa
from app.users.auth_router import router as router_auth  # noqa

app = FastAPI()
app.include_router(router_auth)
app.include_router(router_goods)
app.include_router(router_journal)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
