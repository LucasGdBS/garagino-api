from pydantic import BaseModel
from typing import Optional
from pydantic.fields import Field

class Creator(BaseModel):
    name: str
    github_url: str

class Project(BaseModel):
    name: str
    image_id: Optional[str] = Field(default=None)
    short_description: str
    long_description: str