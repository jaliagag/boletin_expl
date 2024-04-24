from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta


router = APIRouter(prefix="/jwtauth",
                   tags=["jwtauth"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 60
SECRET = "60cb2be5a2ff3e8d5a129dea12edbfe210d13520b0a4008f99cc68b58c21e9cc"

#router = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "conan": {
        "username": "conan",
        "fullname": "conan aliaga",
        "email": "conan@gmail.com",
        "disabled": False,
        "password": "$2a$12$xoMk8OHuas083Mx11DZeo.jyZKK6jeeTuDx/WxhdSRxr2cYKDjy1W"# 123456
    },
    "paula": {
        "username": "paula",
        "fullname": "paula centanni",
        "email": "pmcentanni@gmail.com",
        "disabled": False,
        "password": "$2a$12$PlaCA6v3NGDE8YhX33BGQewv9U7tBI2Jj6yap4nhyzo4eFjZ8Xzja" #amorcis
    },
    "jose": {
        "username": "jose",
        "fullname": "jose aliaga",
        "email": "jmfaliaga@gmail.com",
        "disabled": False,
        "password": "$2a$12$oTJI3/CTTz8LWvcXSNC1Mug6wSUSkoaq1v7WK7oOnKEF3bVySRqwa"#noselaverad1234
    },
    "simba": {
        "username": "simba",
        "fullname": "simba centanni",
        "email": "apestoso@gmail.com",
        "disabled": True,
        "password": "$2a$12$K7drL8pfymLz5je0qm9j8e3PEKfjcQUg00/SSCN3D.sZ8fNX4uCfK"#lloroporqueconanesmejor
    },
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="usuario no autorizado", 
            headers={"WWW-Authenticate": "Bearer"}
        )
 
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception

    return search_user(username)


## criterio de dependencia
async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="usuario inactivo")

    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="usuario incorrecto")

    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password): # <<<<
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password incorrecta")

    access_token = {
        "sub" : user.username,
        "exp" : datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION),
    }

    return {"access_token": jwt.encode(access_token, key=SECRET, algorithm=ALGORITHM), "token_type": "bearer"} #<<<<

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    try:
        return user
    except Exception as error:
        print("An error occurred:", error)
#
#
#
