from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    email: str
    date_of_birth: str

