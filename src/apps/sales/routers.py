"""Contains the routes and url for the sales app."""
from http.client import OK, NOT_FOUND

import pandas as pd

from typing import Optional, Annotated
from fastapi import APIRouter, HTTPException, Depends

from src.apps.sales.dto import (
    SummaryRequest,
    ColumnStatistics,
)
from src.apps.sales.services import filter_data, compute_statistics
from src.apps.sales.data_utils import load_data

__all__ = ("router",)
router = APIRouter()


@router.post(
    "/summary",
    response_model=dict[str, ColumnStatistics],
    summary="Generate sales summary",
    description=(
        "Generates a summary of sales data based on the provided filters and columns. "
        "The response includes statistics like mean, median, mode, standard deviation, "
        "and percentiles."
    ),
    response_description="A dictionary where keys are column names and values are ColumnStatistics.",
    responses={
        OK: {
            "description": "Successfully computed statistics.",
            "content": {
                "application/json": {
                    "example": {
                        "quantity_sold": {
                            "mean": 125.5,
                            "median": 120.0,
                            "mode": 115.0,
                            "std_dev": 10.0,
                            "percentile_25": 110.0,
                            "percentile_75": 130.0,
                        },
                        "price_per_unit": {
                            "mean": 19.99,
                            "median": 19.5,
                            "mode": 19.0,
                            "std_dev": 1.5,
                            "percentile_25": 18.5,
                            "percentile_75": 21.0,
                        },
                    }
                }
            },
        },
        NOT_FOUND: {
            "description": "No statistics found for the given filters and columns.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "filters", "date_range"],
                                "msg": "No statistics found for the given filters and columns.",
                                "type": "not_found",
                                "ctx": {},
                            }
                        ]
                    }
                }
            },
        },
    },
)
async def generate_sales_summary_router(
    summary_request: SummaryRequest,
    sales_data: Annotated[pd.DataFrame, Depends(load_data)],
) -> Optional[dict[str, ColumnStatistics]]:
    """Generate a summary of sales data based on the provided filters and columns."""

    # apply provided filters if any
    filtered_data = filter_data(sales_data, summary_request.filters)

    # compute statistics for the specified columns
    statistics = compute_statistics(filtered_data, summary_request.columns or [])

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
