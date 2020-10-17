import re

import pytest

from jatime.analyzer import _split, analyze, split


@pytest.mark.parametrize(
    "strings",
    [
        [],
        ["あ"],
        ["あ" * 5, "12日", "あ" * 7, "２３日", "あ" * 11, "5日"],
        ["あ" * 5, "12日", "あ" * 7, "２３日", "あ" * 11, "5日", "あ" * 17],
    ],
)
def test__split(strings):
    string = "".join(strings)
    pattern = re.compile(r"(?P<day>\d{1,2})日")
    pieces = _split(string, pattern)
    for i, m in enumerate(pieces):
        if type(m) == str:
            assert m == strings[i]
        else:
            assert m.group() == strings[i]


def test_split():
    strings = ["昨日は", "17日", "です。今日は", "１０月１８日", "です。明日は", "１９日", "です。"]
    string = "".join(strings)
    patterns = [
        re.compile(r"((?P<month>\d{1,2})月(?P<day>\d{1,2})日)"),
        re.compile(r"(?P<day>\d{1,2})日"),
    ]
    pieces = split(string, patterns)
    for i, m in enumerate(pieces):
        if type(m) == str:
            assert m == strings[i]
        else:
            assert m.group() == strings[i]


def test_analyze():
    result = analyze("あああ令和２年十月十七日あああ平成一九年(2007年)１０月１８日あああ")
    for i, r in enumerate(result):
        if i in (1, 3):
            assert type(r) == dict
        else:
            assert type(r) == str


def test_example():
    result = analyze("それは令和２年十月十七日の出来事でした。")
    print(result)
