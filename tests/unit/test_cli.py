"""Tests for find_x.cli.

Uses Typer's CliRunner to invoke commands in-process (no subprocess), so
these run at unit-test speed while still exercising real arg parsing.
"""

import json

from typer.testing import CliRunner

from find_x.cli import app

runner = CliRunner()


def test_search_command_reports_no_results_on_current_pipeline(sample_repo):
    result = runner.invoke(app, ["search", str(sample_repo), "anything"])
    assert result.exit_code == 0
    assert "No results" in result.stdout


def test_search_command_json_output_is_valid_empty_json(sample_repo):
    result = runner.invoke(app, ["search", str(sample_repo), "anything", "--json"])
    assert result.exit_code == 0
    assert json.loads(result.stdout) == []


def test_search_command_fails_cleanly_on_nonexistent_path():
    result = runner.invoke(app, ["search", "/definitely/does/not/exist", "anything"])
    assert result.exit_code == 1
    assert "not a directory" in result.stdout


def test_search_command_accepts_top_k_flag(sample_repo):
    result = runner.invoke(app, ["search", str(sample_repo), "anything", "--top-k", "3"])
    assert result.exit_code == 0


def test_search_requires_both_positional_arguments():
    result = runner.invoke(app, ["search"])
    assert result.exit_code != 0
