from src.database.mysqldb import engine
from src.database.sqlitedb import Base


def init_database_table():
    """
    This function will generate database's table.
    If database doesn't contain the corresponding model,
    which is declared in model library.
    :return: None
    """
    # 初始化数据库
    Base.metadata.create_all(bind=engine)
