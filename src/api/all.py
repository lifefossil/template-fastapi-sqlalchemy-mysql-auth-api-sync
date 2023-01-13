from fastapi.routing import APIRouter

from src.api.user_api import rt as user_router

ApiRouter = APIRouter()

ApiRouter.include_router(user_router)
