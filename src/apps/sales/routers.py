"""Contains the routes and url for the sales app."""

from fastapi import APIRouter

__all__ = ("router",)

router = APIRouter()


@router.post("/summary")
async def generate_sales_summary() -> None: ...
