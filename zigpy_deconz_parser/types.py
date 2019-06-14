import binascii
import enum

import attr
import zigpy.types as t

LPAD = 30


@attr.s(frozen=True)
class UndefEnum:
    name = attr.ib()
    value = attr.ib()

    cls_name = '_'

    @classmethod
    def deserialize(cls, data):
        cmd_id, data = t.uint8_t.deserialize(data)
        name = 'Unknown_0x{:02x}'.format(cmd_id)
        return cls(name, cmd_id), data

    def __str__(self):
        return "{}.{}".format(self.cls_name, self.name)

    def __repr__(self):
        return "<{}.{}: {}>".format(self.cls_name, self.name, self.value)


class UnknownCommand(UndefEnum):
    cls_name = 'DeConzCommand'


class UnknownStatus(UndefEnum):
    cls_name = 'Status'


class DeConzCommand(t.uint8_t, enum.Enum):
    APS_DATA_CONFIRM = 0x04
    DEVICE_STATE = 0x07
    CHANGE_NETWORK_STATE = 0x08
    READ_PARAMETER = 0x0a
    WRITE_PARAMETER = 0x0b
    DEVICE_STATE_CHANGED = 0x0e
    VERSION = 0x0d
    APS_DATA_REQUEST = 0x12
    APS_DATA_INDICATION = 0x17

    @classmethod
    def deserialize(cls, data):
        try:
            return super().deserialize(data)
        except ValueError:
            return UnknownCommand.deserialize(data)


class Status(t.uint8_t, enum.Enum):
    SUCCESS = 0x00
    FAILURE = 0x01
    BUSY = 0x02
    TIMEOUT = 0x03
    UNSUPPORTED = 0x04
    ERROR = 0x05
    NO_NETWORK = 0x06
    INVALID_VALUE = 0x07

    @classmethod
    def deserialize(cls, data):
        try:
            return super().deserialize(data)
        except ValueError:
            return UnknownStatus.deserialize(data)


class UnknownNetworkState(UndefEnum):
    cls_name = 'NetworkState'


class NetworkState(t.uint8_t, enum.Enum):
    OFFLINE = 0x00
    JOINING = 0x01
    CONNECTED = 0x02
    LEAVING = 0x03

    @classmethod
    def deserialize(cls, data):
        try:
            return super().deserialize(data)
        except ValueError:
            return UnknownNetworkState.deserialize(data)


class UnknownDeconzParameter(UndefEnum):
    cls_name = 'DeconzParameter'


class DeconzParameter(t.uint8_t, enum.Enum):
    MAC_Address = 0x01
    PAN_ID = 0x05
    NWK = 0x07
    EPID = 0x08
    COORDINATOR = 0x09
    CHANNEL_MASK = 0x0b
    TRUST_CENTER = 0x0e
    SECURITY_MODE = 0x10
    NETWORK_KEY = 0x18
    CURRENT_CHANNEL = 0x1c
    PROTOCOL_VERSION = 0x22
    NWK_UPDATE_ID = 0x24
    WATCHDOG_TTL = 0x26

    @classmethod
    def deserialize(cls, data):
        try:
            return super().deserialize(data)
        except ValueError:
            return UnknownDeconzParameter.deserialize(data)


class Header(t.Struct):
    _lpad = LPAD

    _fields = [
        ('command', DeConzCommand),
        ('seq', t.uint8_t),
        ('status', Status),
        ('length', t.uint16_t),
    ]

    @classmethod
    def deserialize(cls, data):
        r, data = super().deserialize(data)
        if len(data) < r.length - 5:
            raise ValueError("Data is too short for frame")
        r.payload = data[:r.length]
        return r, data[r.length:]

    def pretty_print(self, is_reply: bool) -> None:
        headline = "\t\tSequence: [0x{:02x}] ".format(self.seq).ljust(
            self._lpad, '<' if is_reply else '>')

        print(headline + ' ' + str(self.command))
        if is_reply:
            self.print(str(self.status))
        self.print("Frame length: {}".format(self.length))
        if self.length > 5:
            self.print("Payload: {}".format(binascii.hexlify(self.payload)))

    @classmethod
    def print(cls, line):
        print('\t\t' + ' ' * (cls._lpad - 1) + line)


@attr.s
class Command:
    SCHEMA = ()
    _lpad = LPAD

    @classmethod
    def deserialize(cls, data):
        args, data = t.deserialize(data, cls.SCHEMA)
        return cls(*args), data

    @classmethod
    def print(cls, line):
        print('\t\t' + ' ' * (cls._lpad - 1) + line)

    def pretty_print(self, *args):
        raise NotImplemented


class Bytes(bytes):
    @classmethod
    def deserialize(cls, data):
        return cls(data), b''


class DeviceState(t.uint8_t):
    _lpad = LPAD

    @classmethod
    def print(cls, line):
        print('\t\t' + ' ' * (cls._lpad - 1) + line)

    def pretty_print(self, *args):
        self.print("Device State: 0x{:02x}".format(self))


class ApsDataIndicationFlags(t.uint8_t, enum.Enum):
    SRC_ADDR_NWK = 0x01
    LAST_HOP = 0x02
    INCLUDE_IEEE = 0x04


class ApsTxOptions(t.uint8_t):
    _lpad = LPAD

    @classmethod
    def print(cls, line):
        print('\t\t' + ' ' * (cls._lpad - 1) + line)

    def pretty_print(self, *args):
        self.print("TX Options: 0x{:02x}".format(self))


class UnknownConfirmStatus(UndefEnum):
    cls_name = 'ConfirmStatus'


class ConfirmStatus(t.uint8_t, enum.Enum):
    @classmethod
    def deserialize(cls, data):
        try:
            return super().deserialize(data)
        except ValueError:
            return UnknownConfirmStatus.deserialize(data)

    # A request has been executed successfully
    SUCCESS = 0x00

    # An invalid or out-of-range parameter has been passed to a primitive from
    # the next higher layer
    INVALID_PARAMETER = 0xc1

    # The next higher layer has issued a request that is invalid or cannot be
    # executed given the current state of the NWK layer
    INVALID_REQUEST = 0xc2

    # An NLME-JOIN.request has been disallowed
    NOT_PERMITTED = 0xc3

    # An NLME-NETWORK-FORMATION.request has failed to start a network
    STARTUP_FAILURE = 0xc4

    # A device with the address supplied to the NLMEDIRECT-JOIN.request is
    # already present in the neighbor table of the device on which the
    # NLMEDIRECT-JOIN.request was issued
    ALREADY_PRESENT = 0xc5

    # Used to indicate that an NLME-SYNC.request has failed at the MAC layer
    SYNC_FAILURE = 0xc6

    # An NLME-JOIN-DIRECTLY.request has failed because there is no more room
    # in the neighbor table
    NEIGHBOR_TABLE_FULL = 0xc7

    # An NLME-LEAVE.request has failed because the device addressed in the
    # parameter list is not in the neighbor table of the issuing device
    UNKNOWN_DEVICE = 0xc8

    # An NLME-GET.request or NLME-SET.request has been issued with an unknown
    # attribute identifier
    UNSUPPORTED_ATTRIBUTE = 0xc9

    # An NLME-JOIN.request has been issued in an environment where no networks
    # are detectable
    NO_NETWORKS = 0xca

    RESERVED_0xCB = 0xcb

    # Security processing has been attempted on an outgoing frame, and has
    # failed because the frame counter has reached its maximum value
    MAX_FRM_COUNTER = 0xcc

    # Security processing has been attempted on an outgoing frame, and has
    # failed because no key was available with which to process it
    NO_KEY = 0xcd

    # Security processing has been attempted on an outgoing frame, and has
    # failed because the security engine produced erroneous output
    BAD_CCM_OUTPUT = 0xce

    RESERVED_0xCF = 0xcf

    # An attempt to discover a route has failed due to a reason other than a
    # lack of routing capacity
    ROUTE_DISCOVERY_FAILED = 0xd0

    # An NLDE-DATA.request has failed due to a routing failure on the sending
    # device or an NLMEROUTE-DISCOVERY.request has failed due to the cause
    # cited in the accompanying NetworkStatusCode
    ROUTE_ERROR = 0xd1

    # An attempt to send a broadcast frame or member mode multicast has failed
    # due to the fact that there is no room in the BTT
    BT_TABLE_FULL = 0xd2

    # An NLDE-DATA.request has failed due to insufficient buffering available.
    # A non-member mode multicast frame was discarded pending route discovery
    FRAME_NOT_BUFFERED = 0xd3

    # A transmit request failed since the ASDU is too large and fragmentation
    # is not supported
    ASDU_TOO_LONG = 0xa0

    # A received fragmented frame could not be defragmented at the current time
    DEFRAG_DEFERRED = 0xa1

    # A received fragmented frame could not be defragmented since the device
    # does not support fragmentation
    DEFRAG_UNSUPPORTED = 0xa2

    # A parameter value was out of range
    ILLEGAL_REQUEST = 0xa3

    # An APSME-UNBIND.request failed due to the requested binding link not
    # existing in the binding table
    INVALID_BINDING = 0xa4

    # An APSME-REMOVE-GROUP.request has been issued with a group identifier
    # that does not appear in the group table
    INVALID_GROUP = 0xa5

    # A parameter value was invalid or out of range
    APS_INVALID_PARAMETER = 0xa6

    # An APSDE-DATA.request requesting acknowledged transmission failed due to
    # no acknowledgement being received
    NO_ACK = 0xa7

    # An APSDE-DATA.request with a destination addressing mode set to 0x00
    # failed due to there being no devices bound to this device
    NO_BOUND_DEVICE = 0xa8

    # An APSDE-DATA.request with a destination addressing mode set to 0x03
    # failed due to no corresponding short address found in the address map
    # table
    NO_SHORT_ADDRESS = 0xa9

    # An APSDE-DATA.request with a destination addressing mode set to 0x00
    # failed due to a binding table not being supported on the device
    NOT_SUPPORTED = 0xaa

    # An ASDU was received that was secured using a link key
    SECURED_LINK_KEY = 0xab

    # An ASDU was received that was secured using a network key
    SECURED_NWK_KEY = 0xac

    #  An APSDE-DATA.request requesting security has resulted in an error
    #  during the corresponding security processing
    SECURITY_FAIL = 0xad

    # An APSME-BIND.request or APSME.ADDGROUP.request issued when the binding
    # or group tables, respectively, were full
    TABLE_FULL = 0xae

    # An ASDU was received without any security
    UNSECURED = 0xaf

    # An APSME-GET.request or APSMESET.request has been issued with an unknown
    # attribute identifier
    APS_UNSUPPORTED_ATTRIBUTE = 0xb0
