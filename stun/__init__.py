# coding=utf-8

import logging
import random
import socket
import struct

__version__ = "0.0.5"

log = logging.getLogger("pystun")


def enable_logging():
    logging.basicConfig()
    log.setLevel(logging.DEBUG)

stun_servers_list = (
    "stun.ekiga.net",
    'stunserver.org',
    'stun.ideasip.com',
    'stun.softjoys.com',
    'stun.voipbuster.com',
)

# TODO: Enum would be perfect here, instead of all this
# manual mapping between numbers and names.

# stun attributes
MappedAddress = 0x0001
ResponseAddress = 0x0002
ChangeRequest = 0x0003
SourceAddress = 0x0004
ChangedAddress = 0x0005
Username = 0x0006
Password = 0x0007
MessageIntegrity = 0x0008
ErrorCode = 0x0009
UnknownAttribute = 0x000A
ReflectedFrom = 0x000B
XorOnly = 0x0021
XorMappedAddress = 0x8020
ServerName = 0x8022
SecondaryAddress = 0x8050  # Non standard extention

# types for a stun message
BindRequestMsg = 0x0001
BindResponseMsg = 0x0101
BindErrorResponseMsg = 0x0111
SharedSecretRequestMsg = 0x0002
SharedSecretResponseMsg = 0x0102
SharedSecretErrorResponseMsg = 0x0112

dictAttrToVal = {'MappedAddress': MappedAddress,
                 'ResponseAddress': ResponseAddress,
                 'ChangeRequest': ChangeRequest,
                 'SourceAddress': SourceAddress,
                 'ChangedAddress': ChangedAddress,
                 'Username': Username,
                 'Password': Password,
                 'MessageIntegrity': MessageIntegrity,
                 'ErrorCode': ErrorCode,
                 'UnknownAttribute': UnknownAttribute,
                 'ReflectedFrom': ReflectedFrom,
                 'XorOnly': XorOnly,
                 'XorMappedAddress': XorMappedAddress,
                 'ServerName': ServerName,
                 'SecondaryAddress': SecondaryAddress}

dictMsgTypeToVal = {
    'BindRequestMsg': BindRequestMsg,
    'BindResponseMsg': BindResponseMsg,
    'BindErrorResponseMsg': BindErrorResponseMsg,
    'SharedSecretRequestMsg': SharedSecretRequestMsg,
    'SharedSecretResponseMsg': SharedSecretResponseMsg,
    'SharedSecretErrorResponseMsg': SharedSecretErrorResponseMsg}

dictValToMsgType = {}

dictValToAttr = {}

Blocked = "Blocked"
OpenInternet = "Open Internet"
FullCone = "Full Cone"
SymmetricUDPFirewall = "Symmetric UDP Firewall"
RestricNAT = "Restric NAT"
RestricPortNAT = "Restric Port NAT"
SymmetricNAT = "Symmetric NAT"
ChangedAddressError = "Meet an error, when do Test1 on Changed IP and Port"


def _initialize():
    global dictValToArray, dictValToMsgType
    dictValToArray = dict((v, k) for k, v in dictAttrToVal.items())
    dictValToMsgType = dict((v, k) for k, v in dictMsgTypeToVal.items())


def gen_tran_id():
    return bytearray(random.randrange(256) for _ in range(16))


def unpack_port_ip(buf):
    port_ipbits = struct.unpack('>H4B', buf)
    ip = '.'.join(map(str, port_ipbits[1:]))
    return port_ipbits[0], ip


def make_change_request(a, b):
    return struct.pack('>HHI', ChangeRequest, a, b)


def stun_test(sock, host, port, source_ip, source_port, send_data=b""):
    retVal = {'Resp': False, 'ExternalIP': None, 'ExternalPort': None,
              'SourceIP': None, 'SourcePort': None, 'ChangedIP': None,
              'ChangedPort': None}
    str_len = len(send_data) // 2
    tranid = gen_tran_id()
    data = struct.pack('>HH', BindRequestMsg, str_len) + tranid + send_data
    recvCorr = False
    while not recvCorr:
        recieved = False
        count = 3
        while not recieved:
            log.debug("sendto %s" % str((host, port)))
            try:
                sock.sendto(data, (host, port))
            except socket.gaierror:
                retVal['Resp'] = False
                return retVal
            try:
                buf, addr = sock.recvfrom(2048)
                log.debug("recvfrom: %s" % str(addr))
                recieved = True
            except Exception:
                recieved = False
                if count > 0:
                    count -= 1
                else:
                    retVal['Resp'] = False
                    return retVal
        msgtype, = struct.unpack('>H', buf[0:2])
        bind_resp_msg = dictValToMsgType[msgtype] == "BindResponseMsg"
        tranid_match = tranid == buf[4:20]
        if bind_resp_msg and tranid_match:
            recvCorr = True
            retVal['Resp'] = True
            len_message, = struct.unpack('>H', buf[2:4])
            len_remain = len_message
            base = 20
            while len_remain:
                attr_type, attr_len = struct.unpack('>HH', buf[base:base+4])
                if attr_type == MappedAddress:
                    port, ip = unpack_port_ip(buf[base+6:base+12])
                    retVal['ExternalIP'] = ip
                    retVal['ExternalPort'] = port
                if attr_type == SourceAddress:
                    port, ip = unpack_port_ip(buf[base+6:base+12])
                    retVal['SourceIP'] = ip
                    retVal['SourcePort'] = port
                if attr_type == ChangedAddress:
                    port, ip = unpack_port_ip(buf[base+6:base+12])
                    retVal['ChangedIP'] = ip
                    retVal['ChangedPort'] = port
                # if attr_type == ServerName:
                    # serverName = buf[(base+4):(base+4+attr_len)]
                base = base + 4 + attr_len
                len_remain = len_remain - (4 + attr_len)
    # s.close()
    return retVal


def get_nat_type(s, source_ip, source_port, stun_host=None, stun_port=3478):
    _initialize()
    port = stun_port
    log.debug("Do Test1")
    resp = False
    if stun_host:
        ret = stun_test(s, stun_host, port, source_ip, source_port)
        resp = ret['Resp']
    else:
        for stun_host in stun_servers_list:
            log.debug('Trying STUN host: %s' % stun_host)
            ret = stun_test(s, stun_host, port, source_ip, source_port)
            resp = ret['Resp']
            if resp:
                break
    if not resp:
        return Blocked, ret
    log.debug("Result: %s" % ret)
    exIP = ret['ExternalIP']
    exPort = ret['ExternalPort']
    changedIP = ret['ChangedIP']
    changedPort = ret['ChangedPort']
    if ret['ExternalIP'] == source_ip:
        changeRequest = make_change_request(4, 6)
        ret = stun_test(s, stun_host, port, source_ip, source_port,
                        changeRequest)
        if ret['Resp']:
            typ = OpenInternet
        else:
            typ = SymmetricUDPFirewall
    else:
        changeRequest = make_change_request(4, 6)
        log.debug("Do Test2")
        ret = stun_test(s, stun_host, port, source_ip, source_port,
                        changeRequest)
        log.debug("Result: %s" % ret)
        if ret['Resp']:
            typ = FullCone
        else:
            log.debug("Do Test1")
            ret = stun_test(s, changedIP, changedPort, source_ip, source_port)
            log.debug("Result: %s" % ret)
            if not ret['Resp']:
                typ = ChangedAddressError
            else:
                if exIP == ret['ExternalIP'] and exPort == ret['ExternalPort']:
                    changePortRequest = make_change_request(4, 2)
                    log.debug("Do Test3")
                    ret = stun_test(s, changedIP, port, source_ip, source_port,
                                    changePortRequest)
                    log.debug("Result: %s" % ret)
                    if ret['Resp']:
                        typ = RestricNAT
                    else:
                        typ = RestricPortNAT
                else:
                    typ = SymmetricNAT
    return typ, ret


def get_ip_info(source_ip="0.0.0.0", source_port=54320, stun_host=None,
                stun_port=3478):
    socket.setdefaulttimeout(2)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((source_ip, source_port))
    nat_type, nat = get_nat_type(s, source_ip, source_port,
                                 stun_host=stun_host, stun_port=stun_port)
    external_ip = nat['ExternalIP']
    external_port = nat['ExternalPort']
    s.close()
    return (nat_type, external_ip, external_port)


def main():
    nat_type, external_ip, external_port = get_ip_info()
    print("NAT Type: {0}".format(nat_type))
    print("External IP: {0}".format(external_ip))
    print("External Port: {0}".format(external_port))

if __name__ == '__main__':
    main()
