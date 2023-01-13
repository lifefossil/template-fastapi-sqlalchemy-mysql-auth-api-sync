from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import project_config


def register_middleware(app: FastAPI) -> None:
    """
    向FastAPI中添加中间件
    :param app:
    :return:
    """
    # 添加跨域支持
    app.add_middleware(
        CORSMiddleware,
        allow_origins=project_config.CORS_ORIGINS,
        allow_credentials=project_config.CORS_ALLOW_CREDENTIALS,
        allow_methods=project_config.CORS_ALLOW_METHODS,
        allow_headers=project_config.CORS_ALLOW_HEADERS,
    )
