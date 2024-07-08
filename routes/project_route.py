from fastapi import APIRouter, UploadFile, HTTPException, Depends, status, File, Form
from fastapi.responses import JSONResponse, StreamingResponse
from bson import ObjectId
import gridfs
from schema.schemas import project_list_serial, to_dict
from config.database import db
from models.projects import Project
from schema.auth import auth_wrapper

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
    projects = project_list_serial(collection_name.find())
    return JSONResponse(status_code=status.HTTP_200_OK, content=projects)

# Post request to add a project
@router.post("/projects", dependencies=[Depends(auth_wrapper)])
async def add_project(
    name: str = Form(...),
    short_description: str = Form(...),
    long_description: str = Form(...),
    file: UploadFile = File(...)
    ):

    try:
        file_id = fs.put(file.file, filename=file.filename)
        project = Project(
            name=name,
            image_id=str(file_id),
            short_description=short_description,
            long_description=long_description
        )

        project_dict = to_dict(project)
        collection_name.insert_one(project_dict)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Project added successfully"})
    except Exception as e:
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

