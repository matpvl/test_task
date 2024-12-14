"""Contains the routes and url for the sales app."""

from fastapi import APIRouter

__all__ = ("router",)

router = APIRouter()


# TODO Matija: update swagger ui with docs

# TODO Matija: update the endpoint logic
@router.post("/summary")
async def generate_sales_summary_router() -> None: ...
