from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from src.core.config import project_config
from src.core.constants import PROJECT_ROOT_DIR

# 拼接sqlite的url
SQLALCHEMY_DATABASE_URL: str = rf"sqlite:///{PROJECT_ROOT_DIR / 'sqlite.db'}"

# 创建sqlalchemy的链接引擎, 这里面会处理数据库链接和连接池等.
# echo: 是否在控制台打印sql语句
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=project_config.APP_DEBUG, future=True,
                       connect_args={"check_same_thread": False})

# 通过sessionmaker工厂创建Session工厂类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 声明Model父类.
Base = declarative_base()


def get_db() -> Session:
    """
    通过sessionmaker生成Sqlalchemy.orm.Session实例,
    用于Fastapi在路径函数中使用Depends注入.Fastapi会在
    路劲函数结束后自动执行yield db后面代码.

    如果不使用路径Depends注入,可以使用with语句:
    with Session() as session:
        result = session.execute()
        print(result.scalars().one_or_none())

    :return: Session实例
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
