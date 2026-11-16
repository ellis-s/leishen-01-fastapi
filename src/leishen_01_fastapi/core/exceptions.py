from fastapi import HTTPException, Request
from fastapi.exceptions import StarletteHTTPException
from fastapi.routing import JSONResponse


# 1. 业务代码中主动抛出的 HTTP 异常（处理业务中 raise 的 HTTPException）
def handle_http_exception(req: Request, exc: HTTPException):
    print("handle_http_exception:", req.url)
    return JSONResponse(
        content={
            "msg": exc.detail,
            "code": exc.status_code,
        }
    )


"""
1. 自定义 HTTP 异常处理器
2. 捕获 Starlette 内部组建抛出的 HTTP 异常
3. 兼容 starlette 的第三方扩展
"""


def handle_starlette_http_exception(req: Request, exc: StarletteHTTPException):
    print("handle_sterlette_http_exception:", req.url)
    return JSONResponse(
        content={
            "msg": exc.detail,
            "code": exc.status_code,
        }
    )


def handle_default_exception(req: Request, exc: Exception):

    print("handle_default_exception", req.url, req.query_params, req.body)
    print(type(exc).__name__)

    return JSONResponse(
        content={
            "msg": "网络开小差了，请稍后再试！",
        },
        status_code=500,
    )
