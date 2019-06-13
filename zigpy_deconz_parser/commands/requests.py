import attr

import zigpy.types as t
import zigpy_deconz_parser.types as pt


@attr.s
class Version(pt.Command):
    @staticmethod
    def pretty_print():
        pass


@attr.s
class ReadParameter(pt.Command):
    SCHEMA = (t.uint16_t, pt.DeconzParameter,)

    payload_length = attr.ib(factory=SCHEMA[0])
    parameter = attr.ib(factory=SCHEMA[1])

    def pretty_print(self, *args):
        self.print("Payload length: {}".format(self.payload_length))
        self.print(str(self.parameter))


@attr.s
class WriteParameter(pt.Command):
    SCHEMA = (t.uint16_t, pt.DeconzParameter, pt.Bytes)

    payload_length = attr.ib(factory=SCHEMA[0])
    parameter = attr.ib(factory=SCHEMA[1])
    value = attr.ib(factory=SCHEMA[2])

    def pretty_print(self, *args):
        self.print("Payload length: {}".format(self.payload_length))
        self.print(str(self.parameter))
        self.print("Value: {}".format(self.value))


@attr.s
class DeviceState(pt.Command):
    SCHEMA = (t.uint8_t, t.uint8_t, t.uint8_t, )

    reserved_1 = attr.ib(factory=SCHEMA[0])
    reserved_2 = attr.ib(factory=SCHEMA[1])
    reserved_3 = attr.ib(factory=SCHEMA[2])

    def pretty_print(self, *args):
        self.print("Reserved: {} shall be set to 0".format(self.reserved_1))
        self.print("Reserved: {} shall be set to 0".format(self.reserved_2))
        self.print("Reserved: {} shall be set to 0".format(self.reserved_3))


@attr.s
class ChangeNetworkState(pt.Command):
    SCHEMA = (pt.NetworkState, )

    network_state = attr.ib(factory=SCHEMA[0])

    def pretty_print(self, *args):
        self.print(str(self.network_state))


@attr.s
class ApsDataIndication(pt.Command):
    SCHEMA = (pt.ApsDataIndicationFlags, )

    flags = attr.ib(factory=pt.ApsDataIndicationFlags)

    def pretty_print(self, *args):
        self.print("Flags: {}".format(self.flags))

