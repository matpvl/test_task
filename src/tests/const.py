"""Constants for testing."""

from datetime import date

from src.apps.sales.dto import DateRange


class Some:
    """Class holding testing constants."""

    START_DATE = date(2023, 1, 1)
    END_DATE = date(2023, 1, 31)
    END_DATE_2 = date(2023, 1, 15)
    FUTURE_DATE = date(2500, 1, 15)

    DATE_RANGE = DateRange(start_date=START_DATE, end_date=END_DATE)

    CATEGORY = "Electronics"

    INVALID_CATEGORY = "InvalidCategory"
