from dataclasses import dataclass
from typing import Literal

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from starlette import status

router = APIRouter(
    prefix="/health",
    tags=["Health"],
    route_class=DishkaRoute,
)


@dataclass(frozen=True, slots=True)
class HealthResponse:
    status: Literal["ok"] = "ok"


@router.get("", status_code=status.HTTP_200_OK)
async def get_health_status() -> HealthResponse:
    return HealthResponse()
