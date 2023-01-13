from typing import Any


def response(code: int, msg: str, data: Any = None):
    """
    返回格式
    :param code: 返回代码
    :param msg: 返回信息
    :param data: 返回数据
    :return: JSON格式 {"code": code, "message": msg, "data": data}
    """
    if data is None:
        data = []
    return {"code": code, "message": msg, "data": data}


def success(data: Any = None, msg: str = ''):
    """
    操作成功返回格式
    :param msg: 返回信息
    :param data: 返回数据
    :return: JSON格式 {"code": code, "message": msg, "data": data}
    """
    return response(200, msg, data)


def fail(code: int = -1, msg: str = '', data: Any = ''):
    """
    操作错误返回格式
    :param code: 返回代码
    :param msg: 返回信息
    :param data: 返回数据
    :return: JSON格式 {"code": code, "message": msg, "data": data}
    """
    return response(code, msg, data)
