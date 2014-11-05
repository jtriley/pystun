from __future__ import print_function
import argparse
import logging
import sys

import stun


def make_argument_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='Enable debug logging'
    )
    parser.add_argument(
        '-H', '--host', dest='stun_host',
        help='STUN host to use'
    )
    parser.add_argument(
        '-P', '--host-port', dest='stun_port', type=int, default=3478,
        help='STUN host port to use'
    )
    parser.add_argument(
        '-i', '--interface', dest='source_ip', default='0.0.0.0',
        help='network interface for client'
    )
    parser.add_argument(
        '-p', '--port', dest='source_port', type=int, default=54320,
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

        kwargs = dict(source_ip=options.source_ip,
                      source_port=options.source_port,
                      stun_host=options.stun_host,
                      stun_port=options.stun_port)
        nat_type, external_ip, external_port = stun.get_ip_info(**kwargs)
        print('NAT Type:', nat_type)
        print('External IP:', external_ip)
        print('External Port:', external_port)
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    main()
