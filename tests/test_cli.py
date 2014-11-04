import unittest

from stun import cli


class TestCLI(unittest.TestCase):
    """Test the CLI API."""

    def test_cli_parser(self):
        cli.make_argument_parser()
        # TODO: Verify default arguments
        # TODO: Verify user arguments


if __name__ == '__main__':
    unittest.main()
