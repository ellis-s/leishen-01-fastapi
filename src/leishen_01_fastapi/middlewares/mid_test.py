from fastapi import Request, Response
from fastapi.applications import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint


class Mid_A(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # return await super().dispatch(request, call_next)

        print("[mid a]: start")
        result = await call_next(request)
        print("[mid a]: end")
        return result


class Mid_B(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # return await super().dispatch(request, call_next)

        print("[mid b]: start")
        result = await call_next(request)
        print("[mid b]: end")
        return result


class Mid_C(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # return await super().dispatch(request, call_next)

        print("[mid c]: start")
        result = await call_next(request)
        print("[mid c]: end")
        return result
