from fastapi import FastAPI
from routes.project_route import router as project_router
from routes.user_route import router as user_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Garagino API", description="API do Garagino web app", version="1.0.0")

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(project_router, tags=['Project'])
app.include_router(user_router, tags=['User'])