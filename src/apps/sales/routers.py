"""Contains the routes and url for the sales app."""

from fastapi import APIRouter, HTTPException

__all__ = ("router",)

from src.apps.sales.dto import (
    SummaryRequest,
    ColumnStatistics,
    SalesSummaryResponse,
)
from src.apps.sales.services import load_data, filter_data, compute_statistics

router = APIRouter()


@router.post(
    "/summary",
    response_model=SalesSummaryResponse,
    summary="Generate sales summary",
    description=(
        "This endpoint generates a summary of sales data based on the provided filters and columns. "
        "The response includes statistics such as mean, median, mode, standard deviation, and percentiles."
    ),
    response_description="Sales summary statistics per column.",
)
async def generate_sales_summary_router(
    summary_request: SummaryRequest,
) -> SalesSummaryResponse:
    """Generate a summary of sales data based on the provided filters and columns."""

    try:
        data = load_data()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err)) from err
    except ValueError as err:
        raise HTTPException(status_code=422, detail=str(err)) from err

    # apply provided filters if any
    filtered_data = filter_data(data, summary_request.filters)

    # compute statistics for the specified columns
    statistics = compute_statistics(
        filtered_data, summary_request.columns or []
    )

    # convert the statistics dict into ColumnStatistics DTOs
    column_statistics = {
        column: ColumnStatistics(**stats_dict)
        for column, stats_dict in statistics.items()
    }

    return SalesSummaryResponse(summary=column_statistics)
