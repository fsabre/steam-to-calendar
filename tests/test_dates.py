from datetime import datetime

import pytest

from src.drawing import range_year_month


@pytest.mark.parametrize(
    "start,end,expected", [
        (
                datetime(2022, 9, 16),
                datetime(2022, 12, 16),
                [(2022, 9), (2022, 10), (2022, 11), (2022, 12)]
        ),
        (
                datetime(2022, 9, 16),
                datetime(2023, 2, 16),
                [(2022, 9), (2022, 10), (2022, 11), (2022, 12), (2023, 1), (2023, 2)]
        ),
    ]
)
def test_range_year_month(start, end, expected):
    assert list(range_year_month(start, end)) == expected
