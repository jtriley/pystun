#coding=utf-8
import optparse

import stun


def main():
    parser = optparse.OptionParser(version=stun.__version__)
    parser.add_option("-d", "--debug", dest="DEBUG", action="store_true",
                      default=False, help="Enable debug logging")
    parser.add_option("-H", "--host", dest="stun_host", default=None,
                      help="STUN host to use")
    parser.add_option("-i", "--interface", dest="source_ip", default="0.0.0.0",
                      help="network interface for client (default: 0.0.0.0)")
    parser.add_option("-p", "--port", dest="source_port", type="int",
                      default=54320, help="port to listen on for client "
                      "(default: 54320)")
    (options, args) = parser.parse_args()
    if options.DEBUG:
        stun.enable_logging()
    kwargs = dict(source_ip=options.source_ip,
                  source_port=int(options.source_port),
                  stun_host=options.stun_host)
    nat_type, external_ip, external_port = stun.get_ip_info(**kwargs)
    print "NAT Type:", nat_type
    print "External IP:", external_ip
    print "External Port:", external_port

if __name__ == '__main__':
    main()
