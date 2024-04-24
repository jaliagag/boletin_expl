from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from fastapi.responses import FileResponse

router = APIRouter(prefix="/user",tags=["user"])

# uvicorn users:router --reload

@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


user_list = [User(id=0,name="jose",surname="aliaga",url="www.google.com",age=34),
             User(id=1,name="paula",surname="centanni",url="www.google.com",age=34),
             User(id=2,name="conan",surname="aliaga",url="www.google.com",age=1)
             ]

@router.get("/usersjson")
async def users_json():
    return [{"id":0, "name": "jose","surname": "aliaga","url": "https://www.google.com","age":34},
            {"id":1, "name": "paula","surname": "centanni","url": "https://www.google.com","age":34},
            {"id":2, "name": "conan","surname": "aliaga","url": "https://www.google.com","age":1}]

#@router.get("/usersclass")
#async def users_class():
#    return User(name="jose",surname="aliaga",url="www.google.com",age=34)

@router.get("/users")
async def users():
    return user_list

# get user by path
#@router.get("/userpath/{id}")
#async def user(id: int):
#    return search_user(id)
#    users = filter(lambda user: user.id == id, user_list)
#    try:
#        return list(users)[0]
#    except IndexError:
#        return {"error": "list index out of range"}

    #return user_list[id]

# get user by query
# parametro por query
#@router.get("/userquery")
#async def userquery(id: int):
#    return search_user(id)

@router.get("/{id}")
async def user(id: int): # query
    return search_user(id)

@router.post("/", response_model=User, status_code=201)
async def create_user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=204, detail="user already exists")
    else:
        user_list.routerend(user)
        return {"status": "OK - user successfully added"}

@router.put("/")
async def update_user(user: User):
    for index, existing_user in enumerate(user_list):
        if existing_user.id == user.id:
            user_list[index] = user
            return {"status": f"OK - user {user.name} successfully updated","user": user}

    return HTTPException(status_code=404)

@router.delete("/{id}")
async def delete_user(id: int):
    for index, existing_id in enumerate(user_list):
        if existing_id.id == id:
            del user_list[index]
            return {"status": f"OK - user successfully deleted"}

    return {"error": "user not found"}


def search_user(id:int):
    users = filter(lambda user: user.id == id, user_list)
    try:
        return list(users)[0]
    except IndexError:
        return {"error": "list index out of range"}

