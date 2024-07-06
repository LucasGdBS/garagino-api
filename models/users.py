from pydantic import BaseModel

class UserAuth(BaseModel):
    username: str
    password: str

class User(UserAuth):
    email: str
    full_name: str