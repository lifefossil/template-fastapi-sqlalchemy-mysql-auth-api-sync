from pydantic import BaseSettings

from src.core.constants import PROJECT_ROOT_DIR


class ProjectConfig(BaseSettings):
    """
    项目配置参数类
    """
    # 调试模式
    APP_DEBUG: bool = True
    # 项目信息
    VERSION: str = "0.0.1"
    PROJECT_NAME: str = "project-fastapi-sqlalchemy-mysql-auth-api"
    DESCRIPTION: str = 'fastapi, sqlalchemy, mysql, jwt auth 的模板'

    # 跨域请求
    CORS_ORIGINS: list[str] = ['*']
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ['*']
    CORS_ALLOW_HEADERS: list[str] = ['*']

    # Session
    SECRET_KEY = "session"
    SESSION_COOKIE = "session_id"
    SESSION_MAX_AGE = 14 * 24 * 60 * 60

    # Jwt
    JWT_SECRET_KEY = "12d45e094faa6ca1556c818166a7a9563b93f7199f6f0f4caa6cf63b88e9d3e7"
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60

    # Enable Cache
    ENABLE_CACHE: bool = False

    # 是否初始化数据库开关
    ENABLE_INIT_DATABASE: bool = False


class MysqlConfig(BaseSettings):
    """
    数据库配置参数类
    """
    host: str = 'localhost'
    port: int = 3306
    username: str = 'root'
    password: str = ''
    database: str = ''
    timezone: str = 'Asia/Shanghai'

    class Config:
        # 设置.env中配置参数的前置(如.env中是MYSQL_USERNAME
        # 添加env_prefix后会去掉MYSQL_后和上面username对应).
        env_prefix = 'mysql_'
        env_file = PROJECT_ROOT_DIR / '.env'
        env_file_encoding = 'utf-8'


class RedisConfig(BaseSettings):
    """缓存Redis配置参数类"""
    host: str = 'localhost'
    port: int = 6379

    class Config:
        # 设置.env中配置参数的前置(如.env中是REDIS_HOST
        # 添加env_prefix后会去掉REDIS_后和上面host对应).
        env_prefix = 'redis_'
        env_file = PROJECT_ROOT_DIR / '.env'
        env_file_encoding = 'utf-8'


# 实例化mysql配置信息
mysql_config: MysqlConfig = MysqlConfig()

# 实例化redis配置信息
redis_config: RedisConfig = RedisConfig()

# 实例化项目配置信息
project_config: ProjectConfig = ProjectConfig()
