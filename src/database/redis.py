# --------------------------- Read Me First -------------------------
# 如果需要使用Redis缓存:
# 1. 需要先安装依赖, 在命令行输入 `poetry add aioredis`
# 2. 安装成功后, 在.env中添加你的Redis链接参数
#       REDIS_HOST=localhost
#       REDIS_PORT=6379
# 3. 打开下面注释
# 4. 在项目目录 src.core.events 中打开缓存注解


# import os
#
# from aioredis import Redis, ConnectionPool
#
# from src.core.config import redis_config
#
#
# async def sys_cache() -> Redis:
#     """
#     系统Redis缓存
#     :return: cache 连接池
#     """
#     # 拼接Redis链接url
#     redis_url: str = f"redis://{redis_config.host}:{redis_config.port}"
#
#     sys_cache_pool = ConnectionPool.from_url(
#         redis_url,
#         db=os.getenv('CACHE_DB', 0),
#         encoding='utf-8',
#         decode_responses=True
#     )
#     return Redis(connection_pool=sys_cache_pool)
