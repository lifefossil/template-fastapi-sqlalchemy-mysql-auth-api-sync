import uvicorn
from fastapi import FastAPI

from src.api.all import ApiRouter
from src.core.config import project_config
from src.core.events import register_event_handler
from src.core.exception import register_exception_handler
from src.core.initialization import init_database_table
from src.core.midlleware import register_middleware

# 初始化数据库, 默认不初始化
if project_config.ENABLE_INIT_DATABASE:
    init_database_table()

# Fastapi 初始化
app = FastAPI(
    debug=project_config.APP_DEBUG,
    description=project_config.DESCRIPTION,
    version=project_config.VERSION,
    title=project_config.PROJECT_NAME
)

# 向FastAPI添加事件监听事件
register_event_handler(app=app)

# 向FastAPI添加全局异常拦截处理
register_exception_handler(app=app)

# 注册api路由
app.include_router(ApiRouter)

# 设置中间件 (跨域拦截在此里面)
register_middleware(app=app)


def start():
    """
    Launched with `poetry run dev` at root level
    :return: None
    """
    uvicorn.run("src.main:app", port=9090, reload=True)
