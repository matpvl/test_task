"""Contains the routes and url for the sales app."""

import pandas as pd

from typing import Optional, Annotated
from fastapi import APIRouter, HTTPException, Depends

from src.apps.sales.dto import (
    SummaryRequest,
    ColumnStatistics,
)
from src.apps.sales.services import load_data, filter_data, compute_statistics


__all__ = ("router",)
router = APIRouter()


@router.post(
    "/summary",
    response_model=dict[str, ColumnStatistics],
    summary="Generate sales summary",
    description=(
        "This endpoint generates a summary of sales data based on the provided filters and columns. "
        "The response includes statistics such as mean, median, mode, standard deviation, and percentiles."
    ),
    response_description="Sales summary statistics per column.",
)
async def generate_sales_summary_router(
    summary_request: SummaryRequest,
    sales_data: Annotated[pd.DataFrame, Depends(load_data)],
) -> Optional[dict[str, ColumnStatistics]]:
    """Generate a summary of sales data based on the provided filters and columns."""

    # apply provided filters if any
    filtered_data = filter_data(sales_data, summary_request.filters)

    # compute statistics for the specified columns
    statistics = compute_statistics(
        filtered_data, summary_request.columns or []
    )

    if statistics:
        # convert the statistics dict into ColumnStatistics DTOs
        return {
            column: ColumnStatistics(**stats_dict)  # type: ignore[arg-type]
            for column, stats_dict in statistics.items()
        }
    else:
        raise HTTPException(
            status_code=404,
            detail="No statistics found for the given filters and columns.",
        )
