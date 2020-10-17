import pytest

from jatime.converter import (
    _relative_to_absolute,
    ja_hour_to_24_hour,
    ja_num_to_int,
    jp_year_to_ad_year,
    relative_day_into_absolute,
    relative_month_into_absolute,
    relative_year_into_absolute,
)


@pytest.mark.parametrize(
    "ja_num, expect",
    [
        (123, 123),
        ("零", 0),
        ("十", 10),
        ("拾", 10),
        ("二十", 20),
        ("元", 1),
        ("45", 45),
        ("６７", 67),
        ("4７", 47),
        ("八九", 89),
        ("八十九", 89),
        ("八拾九", 89),
        ("一〇", 10),
        ("十二", 12),
        ("一九九二", 1992),
        ("二〇二〇", 2020),
        ("00123", 123),
        ("", None),
        ("あ", None),
        ("２００５年", None),
        (None, None),
    ],
)
def test_ja_num_to_int(ja_num, expect):
    assert ja_num_to_int(ja_num) == expect


@pytest.mark.parametrize(
    "jp_year, expect",
    [
        ("明治1", 1868),
        ("明治5", 1872),
        ("明治45", 1912),
        ("大正1", 1912),
        ("大正5", 1916),
        ("大正15", 1926),
        ("昭和1", 1926),
        ("昭和5", 1930),
        ("昭和64", 1989),
        ("平成1", 1989),
        ("平成5", 1993),
        ("平成31", 2019),
        ("令和1", 2019),
        ("令和5", 2023),
        ("ああ1", None),
        ("平成あ", None),
        ("平成50", None),
    ],
)
def test_jp_year_to_ad_year(jp_year, expect):
    assert jp_year_to_ad_year(jp_year) == expect


def test__relative_to_absolute():
    data = {"マイナス五": -5, "そのまま": 0, "プラス三": 3}
    converter = _relative_to_absolute(data)
    base = 100
    assert converter("マイナス五", base) == base - 5
    assert converter("そのまま", base) == base
    assert converter("プラス三", base) == base + 3
    assert converter("ほげほげ", base) is None


@pytest.mark.parametrize(
    "relative_year, base_year, expect",
    [
        ("一昨年", 2020, 2018),
        ("昨年", 2020, 2019),
        ("去年", 2020, 2019),
        ("今年", 2020, 2020),
        ("来年", 2020, 2021),
        ("再来年", 2020, 2022),
    ],
)
def test_relative_year_into_absolute(relative_year, base_year, expect):
    assert relative_year_into_absolute(relative_year, base_year) == expect


@pytest.mark.parametrize(
    "relative_month, base_year, base_month, expect",
    [
        ("先々月", 2020, 1, (2019, 11)),
        ("先月", 2020, 1, (2019, 12)),
        ("今月", 2020, 1, (2020, 1)),
        ("来月", 2020, 1, (2020, 2)),
        ("再来月", 2020, 1, (2020, 3)),
        ("先々月", 2020, 12, (2020, 10)),
        ("先月", 2020, 12, (2020, 11)),
        ("今月", 2020, 12, (2020, 12)),
        ("来月", 2020, 12, (2021, 1)),
        ("再来月", 2020, 12, (2021, 2)),
        ("あ", 2020, 8, None),
    ],
)
def test_relative_month_into_absolute(relative_month, base_year, base_month, expect):
    assert relative_month_into_absolute(relative_month, base_year, base_month) == expect


@pytest.mark.parametrize(
    "relative_day, base_year, base_month, base_day, expect",
    [
        ("一昨日", 2020, 1, 1, (2019, 12, 30)),
        ("一昨日", 2020, 2, 1, (2020, 1, 30)),
        ("一昨日", 2020, 1, 3, (2020, 1, 1)),
        ("昨日", 2020, 3, 1, (2020, 2, 29)),
        ("昨日", 2021, 3, 1, (2021, 2, 28)),
        ("今日", 2020, 1, 1, (2020, 1, 1)),
        ("本日", 2020, 1, 1, (2020, 1, 1)),
        ("明日", 2019, 12, 31, (2020, 1, 1)),
        ("明日", 2020, 2, 28, (2020, 2, 29)),
        ("明後日", 2021, 2, 28, (2021, 3, 2)),
        ("あ", 2020, 1, 1, None),
    ],
)
def test_relative_day_into_absolute(
    relative_day, base_year, base_month, base_day, expect
):
    assert (
        relative_day_into_absolute(relative_day, base_year, base_month, base_day)
        == expect
    )


@pytest.mark.parametrize(
    "ampm, hour, expect",
    [
        ("午前", 5, 5),
        ("午後", 5, 17),
        ("AM", 10, 10),
        ("PM", 10, 22),
        ("p.m.", 10, 22),
        ("ｐ.ｍ", 10, 22),
        ("ＰＭ.", 10, 22),
    ],
)
def test_ja_hour_to_24_hour(ampm, hour, expect):
    assert ja_hour_to_24_hour(ampm, hour) == expect
