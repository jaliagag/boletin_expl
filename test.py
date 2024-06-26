from fastapi import Depends, FastAPI
from typing import Annotated

app = FastAPI() # instancia de fatapi

#async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons
