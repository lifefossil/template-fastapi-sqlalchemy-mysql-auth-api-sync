from fastapi import Depends, Security
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from starlette.requests import Request

from src.core.auth import create_access_token, check_permissions
from src.core.config import project_config
from src.core.response import fail, success
from src.database.sqlitedb import get_db
from src.schema import CreateUserSchema, UserLoginSchema
from src.service import user_service
from src.utils import cryptogram

rt = APIRouter(prefix="/user")


@rt.post("")
async def create_user(create_user_model: CreateUserSchema, db: Session = Depends(get_db)):
    user = await user_service.create_user(create_user_model, db)
    return user


@rt.post("/login")
async def user_login(user_login: UserLoginSchema, db: Session = Depends(get_db)):
    get_user = await user_service.get_user_by_username(user_login.username, db)
    if not get_user:
        return fail(msg="用户验证失败")
    if not cryptogram.check_password(user_login.password, get_user.hashed_password):
        return fail(msg="用户验证失败")

    payload = {"user_id": get_user.id, "user_type": "100"}
    jwt_token = create_access_token(payload)
    data = {"token": jwt_token, "expires_in": project_config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60}
    return success(msg="登录成功", data=data)


@rt.get("", dependencies=[Security(check_permissions)])
async def list_user(request: Request, db: Session = Depends(get_db)):
    return request.state.user_id
