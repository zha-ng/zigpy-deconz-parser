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
    pass


class ApsDataIndicationFlags(t.uint8_t, enum.Enum):
    SRC_ADDR_NWK = 0x01
    LAST_HOP = 0x02
    INCLUDE_IEEE = 0x04
