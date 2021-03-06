#!/usr/bin/env python

"""Tests for `pycs` package."""


import unittest
from click.testing import CliRunner

from pycs import cli


class TestPycs(unittest.TestCase):
    """Tests for `pycs` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        help_result = runner.invoke(cli.main, ["--help"])
        assert help_result.exit_code == 0
        assert "Show this message and exit." in help_result.output
