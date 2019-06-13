import binascii
import re

import zigpy_deconz_parser.types as pt
from zigpy_deconz_parser.commands import REQUESTS, RESPONSES


MATCH = re.compile(("^(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})"   # Timestamp
                    "\s"
                    "DEBUG"                                   # Debug
                    "\s"
                    "\(\w+\)"                                 # Mainthread
                    "\s"
                    "\[zigpy_deconz.uart\]"                   # we care about uart only
                    "\s"
                    "(Send|Frame\sreceived):"
                    "\s"
                    "0x([\dabcdef]+)"), re.VERBOSE)


def parse(line):
    result = MATCH.match(line)
    if result is None:
        return
    ts, txrx, data = result.groups()
    data = binascii.unhexlify(data)
    if txrx == 'Frame received':
        is_response = True
    else:
        is_response = False

    hdr, rest = pt.Header.deserialize(data)
    hdr.pretty_print(is_response)
    if is_response:
        cmd = RESPONSES.get(hdr.command)
    else:
        cmd = REQUESTS.get(hdr.command)

    if cmd and hdr.payload:
        cmd, rest = cmd.deserialize(hdr.payload)
        cmd.pretty_print()


