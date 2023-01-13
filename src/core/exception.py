from typing import Union

from fastapi import HTTPException, Request, status, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError


async def http_error_handler(_: Request, exc: HTTPException):
    """
    http异常处理
    :param _:
    :param exc:
    :return:
    """

    return JSONResponse({
        "code": exc.status_code,
        "message": exc.detail,
        "data": exc.detail
    }, status_code=exc.status_code)


class UnicornException(Exception):

    def __init__(self, code, errmsg, data=None):
        """
        失败返回格式
        :param code:
        :param errmsg:
        """
        if data is None:
            data = {}
        self.code = code
        self.errmsg = errmsg
        self.data = data


async def unicorn_exception_handler(_: Request, exc: UnicornException):
    """
    unicorn 异常处理
    :param _:
    :param exc:
    :return:
    """
    return JSONResponse({
        "code": exc.code,
        "message": exc.errmsg,
        "data": exc.data,
    })


async def http422_error_handler(_: Request, exc: Union[RequestValidationError, ValidationError], ) -> JSONResponse:
    """
    参数校验错误处理
    :param _:
    :param exc:
    :return:
    """
    return JSONResponse(
        {
            "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": f"参数校验错误 {exc.errors()}",
            "data": exc.errors(),
        },
        status_code=422,
    )


def register_exception_handler(app: FastAPI) -> None:
    """
    向FastAPI添加全局异常处理函数.
    :param app: FastAPI
    :return: None
    """
    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, http422_error_handler)
    app.add_exception_handler(UnicornException, unicorn_exception_handler)
