import datetime
import json

import pytest

from jatime.errors import InvalidValueError
from jatime.times import DateTime


class TestDateTime:
    @pytest.mark.parametrize(
        "kwargs, expect",
        [
            ({"relative_year": "来年"}, 2022),
            ({"relative_year": "あ"}, None),
        ],
    )
    def test_relative_year(self, kwargs, expect):
        assert DateTime(base=datetime.datetime(2021, 1, 1), **kwargs).year == expect

    @pytest.mark.parametrize(
        "kwargs, expect",
        [
            ({}, None),
            ({"ad_year": "2020"}, 2020),
            ({"ad_year": "あ"}, None),
            ({"jp_year": "令和2"}, 2020),
            ({"jp_year": "あ"}, None),
            ({"ad_year": "2020", "jp_year": "令和2"}, 2020),
            ({"ad_year": "2020", "jp_year": "あ"}, 2020),
            ({"ad_year": "あ", "jp_year": "令和2"}, 2020),
            ({"ad_year": "あ", "jp_year": "あ"}, None),
        ],
    )
    def test_given_year(self, kwargs, expect):
        assert DateTime(base=datetime.datetime(2021, 1, 1), **kwargs).year == expect

    def test_invalid_year(self):
        with pytest.raises(InvalidValueError):
            DateTime(ad_year="2021", jp_year="令和2")

    @pytest.mark.parametrize(
        "kwargs, expect",
        [
            ({"month": "4", "day": "27", "dow": "月"}, 2020),
        ],
    )
    def test_estimated_year(self, kwargs, expect):
        assert DateTime(base=datetime.datetime(2021, 1, 1), **kwargs).year == expect

    @pytest.mark.parametrize(
        "kwargs, expect",
        [
            ({"relative_month": "先月"}, (2020, 12)),
            ({"relative_month": "あ"}, (None, None)),
        ],
    )
    def test_relative_month(self, kwargs, expect):
        dt = DateTime(base=datetime.datetime(2021, 1, 1), **kwargs)
        assert dt.year == expect[0]
        assert dt.month == expect[1]

    @pytest.mark.parametrize(
        "kwargs, expect",
        [
            ({"relative_day": "昨日"}, (2020, 12, 31)),
            ({"relative_day": "あ"}, (None, None, None)),
        ],
    )
    def test_relative_day(self, kwargs, expect):
        dt = DateTime(base=datetime.datetime(2021, 1, 1), **kwargs)
        assert dt.year == expect[0]
        assert dt.month == expect[1]
        assert dt.day == expect[2]

    @pytest.mark.parametrize(
        "kwargs, expect",
        [
            ({}, None),
            ({"month": "1"}, 1),
            ({"month": "12"}, 12),
            ({"month": "あ"}, None),
        ],
    )
    def test_given_month(self, kwargs, expect):
        assert DateTime(base=datetime.datetime(2021, 1, 1), **kwargs).month == expect

    def test_invalid_month(self):
        with pytest.raises(InvalidValueError):
            DateTime(month="0")

        with pytest.raises(InvalidValueError):
            DateTime(month="13")

    @pytest.mark.parametrize(
        "kwargs, expected_year, expected_month",
        [
            ({"day": "13", "dow": "金"}, 2020, 11),
        ],
    )
    def test_estimated_year_month(self, kwargs, expected_year, expected_month):
        dt = DateTime(base=datetime.datetime(2021, 1, 1), **kwargs)
        assert dt.year == expected_year
        assert dt.month == expected_month

    @pytest.mark.parametrize(
        "kwargs, expect",
        [
            ({}, None),
            ({"day": "1"}, 1),
            ({"day": "31"}, 31),
            ({"day": "あ"}, None),
        ],
    )
    def test_given_day(self, kwargs, expect):
        assert DateTime(base=datetime.datetime(2021, 1, 1), **kwargs).day == expect

    def test_invalid_day(self):
        with pytest.raises(InvalidValueError):
            DateTime(day="0")

        with pytest.raises(InvalidValueError):
            DateTime(day="32")

    @pytest.mark.parametrize(
        "kwargs, expect",
        [
            ({}, None),
            ({"dow": "月"}, 0),
            ({"dow": "火"}, 1),
            ({"dow": "水"}, 2),
            ({"dow": "木"}, 3),
            ({"dow": "金"}, 4),
            ({"dow": "土"}, 5),
            ({"dow": "日"}, 6),
            ({"ad_year": "2021", "month": "1", "day": "1", "dow": "金"}, 4),
        ],
    )
    def test_given_dow(self, kwargs, expect):
        assert DateTime(base=datetime.datetime(2021, 1, 1), **kwargs).dow == expect

    def test_invalid_dow(self):
        with pytest.raises(InvalidValueError):
            DateTime(ad_year="2021", month="1", day="1", dow="月")

    @pytest.mark.parametrize(
        "kwargs, expect",
        [
            ({}, None),
            ({"ampm": "午前", "hour": "0"}, 0),
            ({"ampm": "午後", "hour": "5"}, 17),
            ({"ampm": "午後", "hour": "17"}, 29),
            ({"hour": "あ"}, None),
            ({"hour": "5"}, 5),
        ],
    )
    def test_given_hour(self, kwargs, expect):
        assert DateTime(base=datetime.datetime(2021, 1, 1), **kwargs).hour == expect

    def test_invalid_hour(self):
        with pytest.raises(InvalidValueError):
            DateTime(hour="-1")

        with pytest.raises(InvalidValueError):
            DateTime(hour="30")

    @pytest.mark.parametrize(
        "kwargs, expect",
        [
            ({}, None),
            ({"minute": "0"}, 0),
            ({"minute": ""}, None),
            ({"minute": "半"}, 30),
            ({"minute": "59"}, 59),
            ({"minute": "あ"}, None),
        ],
    )
    def test_given_minute(self, kwargs, expect):
        assert DateTime(base=datetime.datetime(2021, 1, 1), **kwargs).minute == expect

    def test_invalid_minute(self):
        with pytest.raises(InvalidValueError):
            DateTime(minute="-1")

        with pytest.raises(InvalidValueError):
            DateTime(minute="60")

    def test_dict_can_be_parsed_into_json_format(self):
        dt = DateTime(ad_year="2021", month="1", day="1")
        json.dumps(dt.to_dict(), indent=2, ensure_ascii=False)
