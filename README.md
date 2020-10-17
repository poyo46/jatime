# Jatime: Time Expression Analyzer for Japanese

[![PyPI Version](https://img.shields.io/pypi/v/jatime.svg)](https://pypi.org/pypi/jatime/)
[![Python Versions](https://img.shields.io/pypi/pyversions/jatime.svg)](https://pypi.org/pypi/jatime/)
[![License](https://img.shields.io/pypi/l/jatime.svg)](https://pypi.org/pypi/jatime/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Test Status](https://github.com/poyo46/jatime/workflows/Test/badge.svg)](https://github.com/poyo46/jatime/actions?query=workflow%3ATest) 

Jatime is a Python library to extract Japanese time expressions from a given text and turning them into objects. 
[Try Jatime now from your browser!](https://poyo46.github.io/jatime/)

## Installing jatime

Install with `pip` or your favorite PyPI package manager.

```
$ pip install jatime
```

## Using jatime

Here's how to analyze Japanese text using jatime. 
Note that "dow" means the day of the week.

**From within Python**

```python
from jatime.analyzer import analyze


result = analyze("それは令和２年十月十七日の出来事でした。")
print(result)
```

```
['それは', {'string': '令和２年十月十七日', 'year': 2020, 'month': 10, 'day': 17, 'dow': 5, 'hour': None, 'minute': None}, 'の出来事でした。']
```

**From the command line**

```console
$ jatime analyze --format-json それは令和２年十月十七日の出来事でした。
[
  "それは",
  {
    "string": "令和２年十月十七日",
    "year": 2020,
    "month": 10,
    "day": 17,
    "dow": 5,
    "hour": null,
    "minute": null
  },
  "の出来事でした。"
]
```

**Over HTTP communication**
```console
$ jatime serve
```

```
$ curl --get "http://localhost:1729/analysis" --data-urlencode "string=それは令和２年十月十七日の出来事でした。"
["それは",{"day":17,"dow":5,"hour":null,"minute":null,"month":10,"string":"令和２年十月十七日","year":2020},"の出来事でした。"]
```

## Features
* Jatime does not change the given string at all. It just objectifies the extracted time expressions.
* Jatime supports a variety of time expressions. `22:30`, `午後十時半` and `P.M.10:30` are all interpreted as the same time as we want.
* Jatime tries to make up for the missing time information whenever possible. That is, jatime calculates the year given the month, day and day of the week.
* Jatime will tell us why the time information is inconsistent if it is inconsistent.
