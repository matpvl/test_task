"""File containing business logic for sales app."""

import pandas as pd

from typing import Optional, Union

from src.apps.sales.const import EXPECTED_COLUMNS
from src.apps.sales.dto import Filters
from src.core.settings import settings


def load_data() -> pd.DataFrame:
    """Load sales data from CSV file."""

    try:
        data = pd.read_csv(settings.sales_data)

    except FileNotFoundError as err:
        raise FileNotFoundError(
            f"Sales data file not found at {settings.sales_data}"
        ) from err

    except pd.errors.EmptyDataError as err:
        message = "Sales data file is empty"
        raise ValueError(message) from err

    _validate_correct_columns(data)
    return data


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


def _validate_correct_columns(data: pd.DataFrame) -> None:
    """Validate that the sales DataFrame contains the required columns."""

    expected_columns = EXPECTED_COLUMNS
    if not expected_columns.issubset(data.columns):
        error_data = "Sales data file does not contain the required columns"
        raise ValueError(error_data)
