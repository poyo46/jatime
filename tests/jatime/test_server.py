from typing import Optional

import pytest
from webtest import TestApp, app
from webtest.response import TestResponse

from jatime import server
from jatime.analyzer import analyze


@pytest.fixture(scope="session", autouse=True)
def webapp() -> app.TestApp:
    return TestApp(server.app)


def test_get_root_should_be_accessible(webapp: app.TestApp):
    response = webapp.get("/")
    assert response.status_code == 200


_GET_PARSE_STRING = "あああ令和２年十月十七日あああ"


def get_analysis(webapp: app.TestApp, string: Optional[str] = None) -> TestResponse:
    if string is None:
        string = _GET_PARSE_STRING
    return webapp.get("/analysis", {"string": string})


def test_get_analysis_should_return_a_normal_response(webapp: app.TestApp):
    assert get_analysis(webapp).status_code == 200


def test_get_analysis_should_be_allowed_to_be_accessed_from_any_origin(
    webapp: app.TestApp,
):
    assert get_analysis(webapp).headers["Access-Control-Allow-Origin"] == "*"


def test_get_analysis_should_return_the_same_result_as_function_parse(
    webapp: app.TestApp,
):
    assert get_analysis(webapp, _GET_PARSE_STRING).json == analyze(_GET_PARSE_STRING)


def test_get_analysis_requires_string_parameter(webapp: app.TestApp):
    with pytest.raises(app.AppError):
        webapp.get("/analysis")
