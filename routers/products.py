
from fastapi import APIRouter

router = APIRouter(prefix="/products", 
                   tags=["products"], # para la documentacion
                   responses={ 404: { "message": "not found" } }
                   )

products_list = ["producto 1", "producto 2", "producto 1", "producto 4", "producto 5" ]

@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def products(id: int):
    return products_list[id]
