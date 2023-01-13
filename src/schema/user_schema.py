from pydantic import BaseModel, Field


class CreateUserSchema(BaseModel):
    username: str = Field(min_length=4, max_length=15)
    password: str = Field(min_length=8, max_length=16)


class UserLoginSchema(BaseModel):
    username: str = Field(min_length=4, max_length=15)
    password: str = Field(min_length=8, max_length=16)
