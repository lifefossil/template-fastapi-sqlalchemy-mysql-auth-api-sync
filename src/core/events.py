from typing import Callable

from fastapi import FastAPI


# from src.database.redis import sys_cache


def startup(app: FastAPI) -> Callable:
    """
    FastApi 启动完成事件
    :param app: FastAPI
    :return: start_app
    """

    async def app_start() -> None:
        # APP启动完成后触发
        print("fastapi已启动")
        # 注入缓存到app state
        # if project_config.ENABLE_CACHE:
        #     app.state.cache = await sys_cache()

    return app_start


def stopping(app: FastAPI) -> Callable:
    """
    FastApi 停止事件
    :param app: FastAPI
    :return: stop_app
    """

    async def stop_app() -> None:
        # APP停止时触发
        print("fastapi已停止")
        # if project_config.ENABLE_CACHE:
        #     cache = await app.state.cache
        #     await cache.close()

    return stop_app


def register_event_handler(app: FastAPI) -> None:
    """
    注册Fastapi事件监听
    :param app: Fastapi
    :return: None
    """
    # 事件监听
    app.add_event_handler("startup", startup(app))
    app.add_event_handler("shutdown", stopping(app))
