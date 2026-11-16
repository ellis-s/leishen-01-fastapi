import uuid
from typing import Annotated

from fastapi import APIRouter, Path

router = APIRouter(prefix="/user", tags=["用户"])


@router.get("/{id}", description="获取用户信息")
def get_user_info(id: Annotated[str, Path(..., description="用户ID")]):
    return {"id": id, "name": str(uuid.uuid1())}
