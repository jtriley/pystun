PyStun
======
A Python STUN client for getting NAT type and external IP

This is a fork of pystun originally created by gaohawk (http://code.google.com/p/pystun/)

PyStun follows RFC 3489: http://www.ietf.org/rfc/rfc3489.txt

A server following STUN-bis hasn't been found on internet so RFC3489 is the
only implementation.

Installation
------------
To install the latest stable version::

    $ easy_install pystun

or download/clone the source and install manually using::

    $ cd /path/to/pystun/src
    $ python setup.py install

If you're hacking on pystun you should use the 'develop' command instead::

    $ python setup.py develop

This will make a link to the sources inside your site-packages directory so
that any changes are immediately available for testing.

Usage
-----
From command line::

    $ pystun
    NAT Type: Full Cone
    External IP: <your-ip-here>
    External Port: 54320

Pass --help for more options::

    % pystun --help
    Usage: pystun [options]

    Options:
      -h, --help            show this help message and exit
      -d, --debug           Enable debug logging
      -H STUN_HOST, --host=STUN_HOST
                            STUN host to use
      -i SOURCE_IP, --interface=SOURCE_IP
                            network interface for client (default: 0.0.0.0)
      -p SOURCE_PORT, --port=SOURCE_PORT
                            port to listen on for client (default: 54320)

From Python::

    import stun
    nat_type, external_ip, external_port = stun.get_ip_info()

This will rotate through an internal list of STUN servers until a response is
found. If no response is found you will get "Blocked" as the *nat_type* and
**None** for *external_ip* and *external_port*.

If you prefer to use a specific STUN server::

    nat_type, external_ip, external_port = stun.get_ip_info(stun_host='stun.ekiga.net')

You may also specify the client interface and port that is used although this
is not needed::

    sip = "0.0.0.0" # interface to listen on (all)
    port = 54320 # port to listen on
    nat_type, external_ip, external_port = stun.get_ip_info(sip, port)

Read the code for more details...

LICENSE
-------
MIT
