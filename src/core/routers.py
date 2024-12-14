"""Project routing."""

from fastapi import APIRouter

from src.apps.sales.routers import router as sales_router


router = APIRouter(prefix="v1/")
router.include_router(sales_router)
