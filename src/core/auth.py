from datetime import datetime, timedelta
from typing import Any

import jwt
from fastapi import Request, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jwt import PyJWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status

from src.core.config import project_config
from src.database.sqlitedb import get_db
from src.service import user_service

OAuth2 = OAuth2PasswordBearer("/user/login")


def create_access_token(payload: dict) -> str:
    token_data = payload.copy()
    # 设置token的超时时长
    expire = datetime.utcnow() + timedelta(minutes=project_config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    # 向jwt中写入超时时长
    token_data.update({"exp": expire})
    # 返回 jwt 加密内容
    return jwt.encode(token_data, project_config.JWT_SECRET_KEY, algorithm=project_config.JWT_ALGORITHM)


async def check_permissions(req: Request, token=Depends(OAuth2), db: Session = Depends(get_db)):
    # -------------------------------------------- 严重 token 是否合法 ---------------------------------------
    try:
        payload: dict[str, Any] = jwt.decode(
            token,
            project_config.JWT_SECRET_KEY,
            algorithms=[project_config.JWT_ALGORITHM]
        )
        if payload:
            # 获得用户ID
            user_id = payload.get("user_id", None)
            # 获得用户类型
            user_type = payload.get("user_type", None)
            if user_id is None or user_type is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="无效凭证",
                    headers={"WWW-Authenticate": f"Bearer{token}"},
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效凭证",
                headers={"WWW-Authenticate": f"Bearer {token}"},
            )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="凭证已过期",
            headers={"WWW-Authenticate": f"Bearer {token}"}
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效凭证",
            headers={"WWW-Authenticate": f"Bearer {token}"},
        )
    except (PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效凭证",
            headers={"WWW-Authenticate": f"Bearer {token}"},
        )

    # -------------------------------------------- 严重 token 是否合法 ---------------------------------------
    # 查询用户是否真实有效
    check_user = await user_service.get_user_by_id(user_id, db)
    if not check_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在或已经被管理员禁用!",
            headers={"WWW-Authenticate": f"Bearer {token}"},
        )
    # 将用户信息存入request中, 在路由函数中可以直接使用.
    req.state.user_id = user_id
    req.state.user_type = user_type
