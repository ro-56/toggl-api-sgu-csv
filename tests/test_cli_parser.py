import pytest

import src.togglreports.cli_parser as cli
import src.togglreports.core.app as app


@pytest.fixture()
def parser():
    base_app = app.Application()
    base_app._load_plugins()
    yield cli.create_parser()
    print("teardown")


class TestCliParser:

    @pytest.mark.parametrize("args", [
        (['config']),
        (['build', 'sgu']),
        (['build', 'sgu', '-p', 'thisweek']),
        (['build', 'sgu', '-p', 'thismonth']),
        (['build', 'sgu', '-p', 'lastweek']),
        (['build', 'sgu', '-p', 'today']),
        (['build', 'sgu', '-s', '2022-01-01']),
        (['build', 'sgu', '-s', '2022-01-01', '-e', '2022-01-01']),
    ])
    def test_args_commands(self, parser, args):
        cli._parse_args(parser, args)

    @pytest.mark.parametrize("args", [
        (['build']),
        (['dummy']),
        (['build', 'dummy']),
        (['build', 'sgu', '-p', 'dummy']),
        (['build', 'sgu', 'dummy']),
        (['build', 'sgu', '-s']),
        (['build', 'sgu', '-e']),
        (['build', 'sgu', '-e', '2022-01-01']),
    ])
    def test_error_args_combination(self, parser, args):
        with pytest.raises(SystemExit):
            cli._parse_args(parser, args)
