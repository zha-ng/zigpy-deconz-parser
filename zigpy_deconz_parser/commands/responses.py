import attr
import binascii

import zigpy.types as t
import zigpy_deconz.types as dt
import zigpy_deconz_parser.types as pt


@attr.s
class Version(pt.Command):
    SCHEMA = (t.uint32_t, )
    version = attr.ib(factory=SCHEMA[0])

    def pretty_print(self, *args):
        self.print("Version: 0x{:08x}".format(self.version))


@attr.s
class ReadParameter(pt.Command):
    SCHEMA = (t.uint16_t, pt.DeconzParameter, pt.Bytes)

    payload_length = attr.ib(factory=SCHEMA[0])
    parameter = attr.ib(factory=SCHEMA[1])
    value = attr.ib(factory=SCHEMA[2])

    def pretty_print(self, *args):
        self.print("Payload length: {}".format(self.payload_length))
        self.print(str(self.parameter))
        self.print("Value: {}".format(binascii.hexlify(self.value)))


@attr.s
class WriteParameter(pt.Command):
    SCHEMA = (t.uint16_t, pt.DeconzParameter, )

    payload_length = attr.ib(factory=SCHEMA[0])
    parameter = attr.ib(factory=SCHEMA[1])

    def pretty_print(self, *args):
        self.print("Payload length: {}".format(self.payload_length))
        self.print(str(self.parameter))


@attr.s
class DeviceState(pt.Command):
    SCHEMA = (t.uint8_t, t.uint8_t, t.uint8_t, )

    device_state = attr.ib(factory=SCHEMA[0])
    reserved_2 = attr.ib(factory=SCHEMA[1])
    reserved_3 = attr.ib(factory=SCHEMA[2])

    def pretty_print(self, *args):
        self.print("Device State: {}".format(self.device_state))
        self.print("Reserved: {} Shall be ignored".format(self.reserved_2))
        self.print("Reserved: {} Shall be ignored".format(self.reserved_3))


@attr.s
class ChangeNetworkState(pt.Command):
    SCHEMA = (pt.NetworkState, )

    network_state = attr.ib(factory=SCHEMA[0])

    def pretty_print(self, *args):
        self.print(str(self.network_state))


@attr.s
class DeviceStateChanged(pt.Command):
    SCHEMA = (pt.DeviceState, )

    device_state = attr.ib(factory=SCHEMA[0])

    def pretty_print(self, *args):
        self.print("Device State: {}".format(str(self.device_state)))


@attr.s
class ApsDataIndication(pt.Command):
    SCHEMA = (t.uint16_t, pt.DeviceState, dt.DeconzAddress, t.uint8_t,
              dt.DeconzAddress, t.uint8_t, t.uint16_t, t.uint16_t,
              t.LongOctetString, t.uint8_t, t.uint8_t, t.uint8_t, t.uint8_t,
              t.uint8_t, t.uint8_t, t.uint8_t, t.int8s, )

    payload_length = attr.ib(factory=SCHEMA[0])
    device_state = attr.ib(factory=SCHEMA[1])
    dst_addr = attr.ib(factory=SCHEMA[2])
    dst_ep = attr.ib(factory=SCHEMA[3])
    src_addr = attr.ib(factory=SCHEMA[4])
    src_ep = attr.ib(factory=SCHEMA[5])
    profile = attr.ib(factory=SCHEMA[6])
    cluster_id = attr.ib(factory=SCHEMA[7])
    asdu = attr.ib(factory=SCHEMA[8])
    reserved_1 = attr.ib(factory=SCHEMA[9])
    reserved_2 = attr.ib(factory=SCHEMA[10])
    lqi = attr.ib(factory=SCHEMA[11])
    reserved_3 = attr.ib(factory=SCHEMA[12])
    reserved_4 = attr.ib(factory=SCHEMA[13])
    reserved_5 = attr.ib(factory=SCHEMA[14])
    reserved_6 = attr.ib(factory=SCHEMA[15])
    rssi = attr.ib(factory=SCHEMA[16])

    def pretty_print(self, *args):
        self.print("Payload length: {}".format(self.payload_length))
        self.print("Device State: {}".format(self.device_state))
        self.print("Dst address: {}".format(self.dst_addr))
        self.print("Dst endpoint {}".format(self.dst_ep))
        self.print("Src address: {}".format(self.src_addr))
        self.print("Src endpoint: {}".format(self.src_ep))
        self.print("Profile id: 0x{:04x}".format(self.profile))
        self.print("Cluster id: 0x{:04x}".format(self.cluster_id))
        self.print("ASDU: {}".format(self.asdu))
        r = "reserved_1: 0x{:02x} Shall be ignored/Last hop since prot. ver 0x0108"
        self.print(r.format(self.reserved_1))
        r = "reserved_2: 0x{:02x} Shall be ignored/Last hop since prot. ver 0x0108"
        self.print(r.format(self.reserved_2))
        self.print("LQI: {}".format(self.lqi))
        self.print("reserved_3: 0x{:02x} Shall be ignored".format(self.reserved_3))
        self.print("reserved_4: 0x{:02x} Shall be ignored".format(self.reserved_4))
        self.print("reserved_5: 0x{:02x} Shall be ignored".format(self.reserved_5))
        self.print("reserved_6: 0x{:02x} Shall be ignored".format(self.reserved_6))
        self.print("RSSI: {}".format(self.rssi))

