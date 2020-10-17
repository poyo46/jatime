import itertools
import re
from typing import List

import pytest

from jatime.patterns import datetime_patterns


def extract_time_string(strings: List[str]) -> List[str]:
    string = "あああ".join(strings)

    result = []
    for pattern in datetime_patterns():
        for m in re.finditer(pattern, string):
            string = string.replace(m.group(), "")
            result.append(m.group())
    return sorted(result)


@pytest.mark.parametrize(
    "ad_year",
    [
        "1234年",
        "1567年",
        "2890年",
        "2020年",
        "１２３４年",
        "１５６７年",
        "２８９０年",
        "２０２０年",
        "1２3４年",
        "一二三四年",
        "一五六七年",
        "二八九〇年",
        "二〇二〇年",
    ],
)
def test_ad_years(ad_year):
    assert extract_time_string([ad_year]) == [ad_year]


@pytest.mark.parametrize(
    "ad_year",
    [
        "123年",
        "4567年",
        "１２３年",
        "４５６７年",
        "一二三年",
        "四五六七年",
    ],
)
def test_ad_years_out_of_range(ad_year):
    assert extract_time_string([ad_year]) == []


@pytest.mark.parametrize(
    "era, year",
    itertools.product(
        (
            "明治",
            "大正",
            "昭和",
            "平成",
            "令和",
        ),
        (
            "1年",
            "11年",
            "25年",
            "１年",
            "１１年",
            "２５年",
            "2５年",
            "一年",
            "十年",
            "一〇年",
            "十一年",
            "一一年",
            "二十年",
            "二〇年",
            "二十五年",
            "二五年",
            "元年",
        ),
    ),
)
def test_jp_years(era, year):
    jp_year = str(era) + str(year)
    assert extract_time_string([jp_year]) == [jp_year]


@pytest.mark.parametrize(
    "jp_year",
    [
        "明治100年",
        "大正七十年",
        "昭和〇年",
    ],
)
def test_jp_years_out_of_range(jp_year):
    assert extract_time_string([jp_year]) == []


@pytest.mark.parametrize(
    "relative_year",
    ["一昨年", "昨年", "去年", "今年", "再来年", "来年"],
)
def test_relative_years(relative_year):
    assert extract_time_string([relative_year]) == [relative_year]


@pytest.mark.parametrize(
    "year",
    [
        "平成4 年 ( 1992 年 )",
        "平成14 年 ( ２００２ )",
        "令和元 （ 2019 ） 年",
        "令和二 （ ２０２０ ）",
        "一九八九 年 ( 昭和６４ 年 )",
        "１９４５ 年（ 昭和二〇 ）",
        "1999 ( 平成11 ) 年",
        "２０００ （ 平成一二 ）",
    ],
)
def test_years(year):
    assert extract_time_string([year]) == [year]


@pytest.mark.parametrize(
    "month",
    [
        "1月",
        "2月",
        "3月",
        "4月",
        "5月",
        "6月",
        "7月",
        "8月",
        "9月",
        "10月",
        "11月",
        "12月",
        "１月",
        "２月",
        "３月",
        "４月",
        "５月",
        "６月",
        "７月",
        "８月",
        "９月",
        "１０月",
        "１１月",
        "１２月",
        "一月",
        "二月",
        "三月",
        "四月",
        "五月",
        "六月",
        "七月",
        "八月",
        "九月",
        "十月",
        "一〇月",
        "十一月",
        "一一月",
        "十二月",
        "一二月",
        "先月",
        "今月",
        "来月",
        "再来月",
    ],
)
def test_months(month):
    assert extract_time_string([month]) == [month]


@pytest.mark.parametrize(
    "month, expect",
    [
        ("0月", []),
        ("13月", ["3月"]),
        ("０月", []),
        ("１３月", ["３月"]),
        ("〇月", []),
        ("十三月", ["三月"]),
        ("一三月", ["三月"]),
    ],
)
def test_months_out_of_range(month, expect):
    assert extract_time_string([month]) == expect


@pytest.mark.parametrize(
    "day",
    [
        "1日",
        "9日",
        "10日",
        "19日",
        "20日",
        "29日",
        "30日",
        "31日",
        "１日",
        "９日",
        "１０日",
        "１９日",
        "２０日",
        "２９日",
        "３０日",
        "３１日",
        "一日",
        "九日",
        "十日",
        "一〇日",
        "十九日",
        "一九日",
        "二十日",
        "二〇日",
        "二十九日",
        "二九日",
        "三十日",
        "三〇日",
        "三十一日",
        "三一日",
        "一昨日",
        "昨日",
        "今日",
        "本日",
        "明日",
        "明後日",
    ],
)
def test_days(day):
    assert extract_time_string([day]) == [day]


@pytest.mark.parametrize(
    "day, expect",
    [
        ("0日", []),
        ("32日", ["2日"]),
        ("０日", []),
        ("３２日", ["２日"]),
        ("〇日", []),
        ("三十二日", ["十二日"]),
        ("三二日", ["二日"]),
    ],
)
def test_days_out_of_range(day, expect):
    assert extract_time_string([day]) == expect


@pytest.mark.parametrize(
    "s, suffix",
    itertools.product(
        ("月", "火", "水", "木", "金", "土", "日"),
        ("曜日", "曜", ""),
    ),
)
def test_enclosed_dow(s, suffix):
    enclosed_dow = "(" + str(s) + str(suffix) + "）"
    assert extract_time_string([enclosed_dow]) == [enclosed_dow]


@pytest.mark.parametrize(
    "s, suffix",
    itertools.product(
        ("月", "火", "水", "木", "金", "土", "日"),
        ("曜日", "曜"),
    ),
)
def test_dow(s, suffix):
    dow = str(s) + str(suffix)
    assert extract_time_string([dow]) == [dow]


@pytest.mark.parametrize(
    "time_kanji",
    [
        "午前〇時〇分",
        "午前〇時半",
        "午前〇時",
        "午後九時九分",
        "午後九時半",
        "午後九時",
        "十時十分",
        "十時半",
        "十時",
        "午前一〇時一〇分",
        "午前一〇時半",
        "午前一〇時",
        "十九時二十分",
        "十九時半",
        "十九時",
        "一九時二〇分",
        "一九時半",
        "一九時",
        "二十時五十九分",
        "二十時半",
        "二十時",
        "二〇時五九分",
        "二〇時半",
        "二〇時",
        "二十四時〇分",
        "二十四時半",
        "二十四時",
        "二四時九分",
        "二四時半",
        "二四時",
    ],
)
def test_time_kanji(time_kanji):
    assert extract_time_string([time_kanji]) == [time_kanji]


@pytest.mark.parametrize(
    "time",
    [
        "午前0時0分",
        "午前0時半",
        "午前0時",
        "午前00時00分",
        "午前00時半",
        "午前00時",
        "午前9時9分",
        "午前9時半",
        "午前9時",
        "午前09時09分",
        "午前09時半",
        "午前09時",
        "午前10時10分",
        "午前10時半",
        "午前10時",
        "午前０時59分",
        "午前０時半",
        "午前０時",
        "午前００時０分",
        "午前００時半",
        "午前００時",
        "午前９時００分",
        "午前９時半",
        "午前９時",
        "午前０９時９分",
        "午前０９時半",
        "午前０９時",
        "午前１０時０９分",
        "午前１０時半",
        "午前１０時",
        "午後0時0分",
        "午後0時半",
        "午後0時",
        "午後00時00分",
        "午後00時半",
        "午後00時",
        "午後9時9分",
        "午後9時半",
        "午後9時",
        "午後09時09分",
        "午後09時半",
        "午後09時",
        "午後10時10分",
        "午後10時半",
        "午後10時",
        "午後０時59分",
        "午後０時半",
        "午後０時",
        "午後００時０分",
        "午後００時半",
        "午後００時",
        "午後９時００分",
        "午後９時半",
        "午後９時",
        "午後０９時９分",
        "午後０９時半",
        "午後０９時",
        "午後１０時０９分",
        "午後１０時半",
        "午後１０時",
        "am 00:00",
        "ａｍ 09:09",
        "AM 10:10",
        "ＡＭ 00:59",
        "pm 00:00",
        "ｐｍ 09:09",
        "PM 10:10",
        "ＰＭ 00:59",
        "A.M. 00:00",
        "A.M 09:09",
        "AM. 10:10",
        "A.M. 00:59",
        "00:00",
        "09:09",
        "10:10",
        "19:59",
        "20:00",
        "24:09",
        "００:００",
        "０９:０９",
        "１０:１０",
        "１９:５９",
        "２０:００",
        "２４:０９",
    ],
)
def test_time(time):
    assert extract_time_string([time]) == [time]


@pytest.mark.parametrize(
    "string",
    [
        "２０２０年１０月１７日（土）１３時１５分",
        "２０２０年１０月１７日１３時１５分",
        "２０２０年１０月１７日（土）",
        "２０２０年１０月１７日",
        "２０２０年１０月",
        "２０２０年",
        "１０月１７日（土）１３時１５分",
        "１０月１７日１３時１５分",
        "１０月１７日（土）",
        "１０月１７日",
        "１０月",
        "１７日（土）１３時１５分",
        "１７日１３時１５分",
        "１７日（土）",
        "１７日",
        "土曜日の１３時１５分",
        "１３時１５分",
        "土曜日",
    ],
)
def test_combined(string):
    assert extract_time_string([string]) == [string]
