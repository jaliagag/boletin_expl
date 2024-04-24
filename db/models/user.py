from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    #id: Optional[str] #str | None # es opcional; en mongodb, id son strings para que puedan ser mas largos
    id: str = None
    username: str
    email: str
