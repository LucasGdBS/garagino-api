from pydantic import BaseModel
from typing import Optional, List
from pydantic import BaseModel, HttpUrl, EmailStr
from datetime import date
from enum import Enum

class Status(str, Enum):
    active = "active"
    inactive = "inactive"
    completed = "completed"
    paused = "paused"
    cancelled = "cancelled"

class Creator(BaseModel):
    name: str
    email: EmailStr
    portifolio: Optional[HttpUrl] = None
    role: Optional[str] = None

class Project(BaseModel):
    project_title: str
    description: str
    start_date: str
    end_date: Optional[str] = None
    status: Status
    technologies: List[str]

    project_image: Optional[str] = None

    repository_link: Optional[HttpUrl] = None
    video_link: Optional[HttpUrl] = None
    category: Optional[str] = None
    keywords: Optional[List[str]] = None
    documentation: Optional[HttpUrl] = None
    additional_comments: Optional[str] = None
    