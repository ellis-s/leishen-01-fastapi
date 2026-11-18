from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware

from leishen_01_fastapi.core.exceptions import (
    handle_default_exception,
    handle_http_exception,
    handle_starlette_http_exception,
)
from leishen_01_fastapi.middlewares.mid_test import Mid_A, Mid_B, Mid_C

from .api.v1 import users


# fastapi 服务器的生命周期
@asynccontextmanager
async def life_cycle(app: FastAPI):
    print("服务启动了...")
    yield
    print("服务停止了...")


def create_app() -> FastAPI:

    app = FastAPI(lifespan=life_cycle)

    # 添加路由
    app.include_router(users.router)

    # 添加中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:8000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(Mid_A)
    app.add_middleware(Mid_B)
    app.add_middleware(Mid_C)

    # 添加异常处理
    app.add_exception_handler(HTTPException, handle_http_exception)
    app.add_exception_handler(StarletteHTTPException, handle_starlette_http_exception)
    app.add_exception_handler(Exception, handle_default_exception)

    return app


app = create_app()


@app.get("/")
def get_root():
    return "Hello, this is demo project!"
