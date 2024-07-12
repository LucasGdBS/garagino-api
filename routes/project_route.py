from fastapi import APIRouter, UploadFile, HTTPException, Depends, status, File, Form
from fastapi.responses import JSONResponse, StreamingResponse
from bson import ObjectId
import gridfs
from config.database import db
from models.projects import Project, Status
from schema.auth import auth_wrapper
from datetime import date
from typing import List, Optional

collection_name = db["garagino_projects_collection"]

fs = gridfs.GridFS(db)

router = APIRouter()

# GET request to test connection
@router.get("/")
async def test_connection():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Connection successful"})

# GET request to get all projects
@router.get("/projects")
async def get_projects():
    try:
        projects = list(collection_name.find())

        for project in projects :
            project["_id"] = str(project["_id"]) # Convert ObjectId to string

        return JSONResponse(status_code=status.HTTP_200_OK, content=projects)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Post request to add a project
@router.post("/projects", dependencies=[Depends(auth_wrapper)])
async def add_project(
    project_title: str = Form(...),
    description: str = Form(...),
    start_date: date = Form(...),
    end_date: date = Form(None),
    project_status: Status = Form(...),
    technologies: List[str] = Form(...),
    category: Optional[str] = Form(None),
    keywords: Optional[List[str]] = Form(None),
    documentation: Optional[str] = Form(None),
    additional_comments: Optional[str] = Form(None),
    file: UploadFile = File(...)
    ):

    try:
        start_date_str = start_date.isoformat()
        end_date_str = end_date.isoformat() if end_date else None

        file_id = fs.put(file.file, filename=file.filename)

        
        project = Project(
            project_title=project_title,
            description=description,
            start_date=start_date_str,
            end_date=end_date_str,
            status=project_status,
            technologies=technologies,
            project_image=str(file_id),
            category=category,
            keywords=keywords,
            documentation=documentation,
            additional_comments=additional_comments
        )

        project_dict = project.model_dump()
        collection_name.insert_one(project_dict)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Project added successfully"})
    except Exception as e:
        collection_name.delete_one({"_id": ObjectId(file_id)})
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/image/{file_id}")
async def get_image(file_id: str):
    try:
        file = fs.get(ObjectId(file_id))
        return StreamingResponse(file, media_type="image/jpeg", headers={"Content-Disposition": f"inline; filename={file.filename}"})
    except gridfs.errors.NoFile:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        print(f"Erro ao obter imagem: {e}")
        raise HTTPException(status_code=500, detail="Erro ao obter imagem")

# Delete request to delete a project
@router.delete("/projects/{id}", dependencies=[Depends(auth_wrapper)])
async def delete_project(id: str):
    collection_name.delete_one({"_id": ObjectId(id)})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Project deleted successfully"})

