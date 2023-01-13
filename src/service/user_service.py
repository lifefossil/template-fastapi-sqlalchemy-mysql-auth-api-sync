from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.model import User
from src.schema import CreateUserSchema
from src.utils.cryptogram import encode_password


async def create_user(create_user: CreateUserSchema, db: Session) -> User:
    get_user = await get_user_by_username(create_user.username, db)
    if get_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已经存在")
    user = User()
    user.username = create_user.username
    user.hashed_password = encode_password(create_user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def get_user_by_username(username: str, db: Session) -> User | None:
    stmt = select(User).where(User.username == username)
    return db.scalars(stmt).one_or_none()


async def get_user_by_id(user_id: int, db: Session) -> User | None:
    return db.scalars(select(User).where(User.id == user_id)).one_or_none
