import pytest

from jatime.errors import NotFoundError
from jatime.finder import (
    _years_close_to,
    _years_months_close_to,
    year_from_month_day_dow,
    year_month_from_day_dow,
)


def test__years_close_to():
    years = [year for year in _years_close_to(2020, 5)]
    expected = [2020, 2021, 2019, 2022, 2018, 2023, 2017, 2024, 2016, 2025]
    assert years == expected


@pytest.mark.parametrize(
    "month, day, dow, base_year, expect",
    [
        (1, 1, 2, 2020, 2020),
        (1, 1, 0, 2020, 2018),
        (1, 1, 0, 2022, 2024),
        (2, 29, 1, 2020, 2028),
    ],
)
def test_find_year(month, day, dow, base_year, expect):
    assert year_from_month_day_dow(month, day, dow, base_year) == expect


def test_find_year_base_can_be_none():
    year_from_month_day_dow(1, 1, 0)


def test_find_year_raises_not_found_error():
    with pytest.raises(NotFoundError):
        year_from_month_day_dow(2, 30, 0)


def test__years_months_close_to():
    years = [year for year in _years_months_close_to(2020, 10, 5)]
    expected = [
        (2020, 10),
        (2020, 11),
        (2020, 9),
        (2020, 12),
        (2020, 8),
        (2021, 1),
        (2020, 7),
        (2021, 2),
        (2020, 6),
        (2021, 3),
    ]
    assert years == expected


@pytest.mark.parametrize(
    "day, dow, base_year, base_month, expect",
    [
        (1, 2, 2020, 1, (2020, 1)),
        (1, 0, 2020, 1, (2020, 6)),
        (1, 0, 2020, 7, (2020, 6)),
    ],
)
def test_find_year_month(day, dow, base_year, base_month, expect):
    assert year_month_from_day_dow(day, dow, base_year, base_month) == expect


def test_find_year_month_base_can_be_none():
    year_month_from_day_dow(1, 0)


def test_find_year_month_raises_not_found_error():
    with pytest.raises(NotFoundError):
        year_month_from_day_dow(0, 0)
