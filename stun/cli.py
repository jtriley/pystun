from __future__ import print_function
import argparse
import logging
import sys

import stun

DEFAULTS = {
    'stun_port': 3478,
    'source_ip': '0.0.0.0',
    'source_port': 54320
}


def make_argument_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='Enable debug logging'
    )
    parser.add_argument(
        '-H', '--stun-host',
        help='STUN host to use'
    )
    parser.add_argument(
        '-P', '--stun-port', type=int,
        default=DEFAULTS['stun_port'],
        help='STUN host port to use'
    )
    parser.add_argument(
        '-i', '--source-ip',
        default=DEFAULTS['source_ip'],
        help='network interface for client'
    )
    parser.add_argument(
        '-p', '--source-port', type=int,
        default=DEFAULTS['source_port'],
        help='port to listen on for client'
    )

    parser.add_argument('--version', action='version', version=stun.__version__)

    return parser


def main():
    try:
        options = make_argument_parser().parse_args()

        if options.debug:
            logging.basicConfig()
            stun.log.setLevel(logging.DEBUG)

        kwargs = vars(options)
        nat_type, external_ip, external_port = stun.get_ip_info(**kwargs)
        print('NAT Type:', nat_type)
        print('External IP:', external_ip)
        print('External Port:', external_port)
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    main()
