from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, datasets, queries

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
api_router.include_router(datasets.file_router, prefix="/files", tags=["files"])
api_router.include_router(queries.router, prefix="/queries", tags=["queries"])
api_router.include_router(queries.access_router, prefix="/accesses", tags=["accesses"])
