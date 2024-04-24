from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from routers import products, users, basic_auth_users, jwt_auth, users_db

app = FastAPI() # instancia de fatapi
favicon_path = "favicon.ico"

# routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth.router)
app.include_router(users_db.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return "Hola mancito"

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

@app.get("/health")
async def health():
    return {"ping": "pong"}

@app.get("/url")
async def url():
    return {"url_curso": "https://github.com/jaliagag/100_days_of_py_v3" }

