import unittest

from stun import cli


class TestCLI(unittest.TestCase):
    """Test the CLI API."""

    def test_cli_parser_default(self):
        parser = cli.make_argument_parser()
        options = parser.parse_args([])

        self.assertEqual(options.source_ip, cli.DEFAULTS['source_ip'])
        self.assertEqual(options.source_port, cli.DEFAULTS['source_port'])
        self.assertEqual(options.stun_port, cli.DEFAULTS['stun_port'])

        # TODO: Verify user arguments


if __name__ == '__main__':
    unittest.main()
