import json
from typing import Optional

from click.testing import CliRunner, Result

from jatime.cui import cli


def command(*args) -> Result:
    runner = CliRunner()
    return runner.invoke(cli, args, terminal_width=256)


def cli_analyze(
    format_json: Optional[bool] = None, string: Optional[str] = None
) -> Result:
    if string is None:
        string = "あああ令和２年十月十七日あああ"

    if format_json is None:
        return command("analyze", string)
    else:
        return command("analyze", "--format-json", string)


def test_cli_parse_should_exit_normally():
    assert cli_analyze().exit_code == 0


def test_cli_parse_should_echo_result():
    assert "2020" in cli_analyze().output
    assert "10" in cli_analyze().output
    assert "17" in cli_analyze().output


def test_cli_parse_can_be_output_in_json_format():
    result = cli_analyze(format_json=True).output
    json.loads(result)
