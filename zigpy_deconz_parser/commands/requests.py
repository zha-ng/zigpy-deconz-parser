import attr
import binascii

import zigpy.types as t
import zigpy_deconz.types as dt
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


@attr.s
class ApsDataRequest(pt.Command):
    _lpad = pt.LPAD

    SCHEMA = (t.uint16_t,  # payload length
              t.uint8_t,  # request_id
              t.uint8_t,  # flags
              dt.DeconzAddressEndpoint,  # destination address and ep
              t.uint16_t,  # profile id
              t.uint16_t,  # cluster id
              t.uint8_t,  # source endpoint
              t.LongOctetString,  # ASDU
              pt.ApsTxOptions,  # tx options
              t.uint8_t,  # radius
    )

    payload_length = attr.ib(factory=SCHEMA[0])
    request_id = attr.ib(factory=SCHEMA[1])
    flags = attr.ib(factory=SCHEMA[2])
    dst_addr = attr.ib(factory=SCHEMA[3])
    profile = attr.ib(factory=SCHEMA[4])
    cluster_id = attr.ib(factory=SCHEMA[5])
    src_ep = attr.ib(factory=SCHEMA[6])
    asdu = attr.ib(factory=SCHEMA[7])
    tx_options = attr.ib(factory=SCHEMA[8])
    radius = attr.ib(factory=SCHEMA[9])

    def pretty_print(self, *args):
        self.print("Payload length: {}".format(self.payload_length))

        headline = "\t\t    Request id: [0x{:02x}] ".\
            format(self.request_id).ljust(self._lpad, '>')
        print(headline + ' ' + str(self.dst_addr))
        if self.dst_addr.address_mode in (1, 2, 4):
            self.print("NWK: 0x{:04x}".format(self.dst_addr.address))

        self.print("flags: 0x{:02x}".format(self.flags))
        self.print("Profile id: 0x{:04x}".format(self.profile))
        self.print("Cluster id: 0x{:04x}".format(self.cluster_id))
        self.print("Src endpoint: {}".format(self.src_ep))
        self.print("ASDU: {}".format(binascii.hexlify(self.asdu)))
        self.tx_options.pretty_print()
        self.print("Radius: {}".format(self.radius))


@attr.s
class ApsDataConfirm(pt.Command):
    SCHEMA = (t.uint16_t, )

    payload_length = attr.ib(factory=SCHEMA[0])

    def pretty_print(self, *args):
        self.print("Payload length: {}".format(self.payload_length))
