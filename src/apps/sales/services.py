"""File containing business logic for sales app."""

import pandas as pd

from typing import Optional, Union

from src.apps.sales.dto import Filters


def filter_data(data: pd.DataFrame, filters: Optional[Filters]) -> pd.DataFrame:
    """Apply filters to the sales data using a dynamic mapping approach."""

    if not filters:
        return data

    filter_map = {
        "date_range": lambda data_frame, value: data_frame[
            (data_frame["date"] >= value.start_date.isoformat())
            & (data_frame["date"] <= value.end_date.isoformat())
        ],
        "category": lambda data_frame, value: data_frame[
            data_frame["category"].isin(value)
        ],
        "product_ids": lambda data_frame, value: data_frame[
            data_frame["product_id"].isin(value)
        ],
    }

    for filter_field, apply_filter in filter_map.items():
        filter_value = getattr(filters, filter_field, None)
        if filter_value:
            data = apply_filter(data, filter_value)

    return data


def compute_statistics(
    data: pd.DataFrame, columns: list[str]
) -> dict[str, dict[str, Union[float, None]]]:
    """Compute summary statistics for the specified columns in the data."""

    statistics = {}

    for column in columns:
        # skip columns not present in the DataFrame
        if column not in data.columns:
            continue

        # drop NaN values to avoid errors and crashes, coerce non-numeric to NaN
        column_data = pd.to_numeric(data[column], errors="coerce").dropna()

        if not column_data.empty:
            statistics[column] = {
                "mean": column_data.mean(),
                "median": column_data.median(),
                "mode": column_data.mode()[0],
                "std_dev": column_data.std(),
                "percentile_25": column_data.quantile(0.25),
                "percentile_75": column_data.quantile(0.75),
            }

    return statistics
