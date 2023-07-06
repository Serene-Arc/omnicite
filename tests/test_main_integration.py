import pytest
from click.testing import CliRunner

from omnicite.__main__ import cli


def test_basic_integration():
    runner = CliRunner()
    result = runner.invoke(cli, ["-v", "single", "10.1177/00045632211066777"])
    assert result.exit_code == 0
    assert "10.1177/00045632211066777" in result.output
