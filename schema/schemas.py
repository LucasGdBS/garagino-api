from typing import Any
from pydantic import BaseModel

def creator_serial(creator) -> dict:
    return {
        "name": creator["name"],
        "github_url": creator["github_url"]
    }

def creator_list_serial(creators) -> list:
    return [creator_serial(creator) for creator in creators]

def individual_project_serial(project) -> dict:
    return {
        "id": str(project["_id"]),
        "name": project["name"],
        "image_url": f"/image/{project['image_id']}" if "image_id" in project else None,
        "short_description": project["short_description"],
        "long_description": project["long_description"],
    }

def project_list_serial(projects) -> list:
    return [individual_project_serial(project) for project in projects]

def to_dict(obj: Any) -> Any:
    if isinstance(obj, BaseModel):
        return obj.model_dump()
    if isinstance(obj, list):
        return [to_dict(item) for item in obj]
    if isinstance(obj, dict):
        return {key: to_dict(value) for key, value in obj.items()}
    return obj

