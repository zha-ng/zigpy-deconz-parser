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
    SCHEMA = (pt.DeviceState, t.uint8_t, t.uint8_t, )

    device_state = attr.ib(factory=SCHEMA[0])
    reserved_2 = attr.ib(factory=SCHEMA[1])
    reserved_3 = attr.ib(factory=SCHEMA[2])

    def pretty_print(self, *args):
        self.device_state.pretty_print()
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
        self.device_state.pretty_print()


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
        self.device_state.pretty_print()

        if self.profile == 0 and self.dst_ep == 0:
            # ZDO
            request_id = t.uint8_t.deserialize(self.asdu)[0]
        else:
            # ZCL
            frame_control = self.asdu[0]
            if frame_control & 0b0100:
                request_id = self.asdu[3]
            else:
                request_id = self.asdu[1]
        headline = "\t\t    Request id: [0x{:02x}] ". \
            format(request_id).ljust(self._lpad, '<')
        print(headline + ' Dst Addr: {}'.format(self.dst_addr))

        if self.dst_addr.address_mode in (1, 2, 4):
            self.print("Dst address: 0x{:04x}".format(self.dst_addr.address))
        self.print("Dst endpoint {}".format(self.dst_ep))
        self.print("Src address: {}".format(self.src_addr))
        if self.src_addr.address_mode in (1, 2, 4):
            self.print("Src address: 0x{:04x}".format(self.src_addr.address))
        self.print("Src endpoint: {}".format(self.src_ep))
        self.print("Profile id: 0x{:04x}".format(self.profile))
        self.print("Cluster id: 0x{:04x}".format(self.cluster_id))
        self.print("ASDU: {}".format(binascii.hexlify(self.asdu)))
        r = "reserved_1: 0x{:02x} Shall be ignored/Last hop since proto ver 0x0108"
        self.print(r.format(self.reserved_1))
        r = "reserved_2: 0x{:02x} Shall be ignored/Last hop since proto ver 0x0108"
        self.print(r.format(self.reserved_2))
        self.print("LQI: {}".format(self.lqi))
        self.print("reserved_3: 0x{:02x} Shall be ignored".format(self.reserved_3))
        self.print("reserved_4: 0x{:02x} Shall be ignored".format(self.reserved_4))
        self.print("reserved_5: 0x{:02x} Shall be ignored".format(self.reserved_5))
        self.print("reserved_6: 0x{:02x} Shall be ignored".format(self.reserved_6))
        self.print("RSSI: {}".format(self.rssi))


@attr.s
class ApsDataRequest(pt.Command):
    _lpad = pt.LPAD

    SCHEMA = (
        t.uint16_t,  # payload length
        pt.DeviceState,  # Device state
        t.uint8_t,  # request_id
    )

    payload_length = attr.ib(factory=SCHEMA[0])
    device_state = attr.ib(factory=SCHEMA[1])
    request_id = attr.ib(factory=SCHEMA[2])

    def pretty_print(self, *args):
        self.print("Payload length: {}".format(self.payload_length))

        headline = "\t\t    Request id: [0x{:02x}] ". \
            format(self.request_id).ljust( self._lpad, '<')
        print(headline + ' ' + '^^^ Above status ^^^')

        self.device_state.pretty_print()


@attr.s
class ApsDataConfirm(pt.Command):
    SCHEMA = (
        t.uint16_t,  # payload length
        pt.DeviceState,  # Device State
        t.uint8_t,  # Request ID
        dt.DeconzAddressEndpoint,  # Destination address
        t.uint8_t,  # Source endpoint
        pt.ConfirmStatus,  # Confirm Status
        t.uint8_t,  # Reserved below
        t.uint8_t,
        t.uint8_t,
        t.uint8_t,
    )

    payload_length = attr.ib(factory=SCHEMA[0])
    device_state = attr.ib(factory=SCHEMA[1])
    request_id = attr.ib(factory=SCHEMA[2])
    dst_addr = attr.ib(factory=SCHEMA[3])
    src_ep = attr.ib(factory=SCHEMA[4])
    confirm_status = attr.ib(factory=SCHEMA[5])
    reserved_1 = attr.ib(factory=SCHEMA[6])
    reserved_2 = attr.ib(factory=SCHEMA[7])
    reserved_3 = attr.ib(factory=SCHEMA[8])
    reserved_4 = attr.ib(factory=SCHEMA[9])

    def pretty_print(self, *args):
        self.print("Payload length: {}".format(self.payload_length))
        self.device_state.pretty_print()

        headline = "\t\t    Request id: [0x{:02x}] ". \
            format(self.request_id).ljust(self._lpad, '<')
        print(headline + ' ' + str(self.dst_addr))
        if self.dst_addr.address_mode in (1, 2, 4):
            self.print("NWK: 0x{:04x}".format(self.dst_addr.address))

        self.print("Src endpoint: {}".format(self.src_ep))
        self.print("TX Status: {}".format(str(self.confirm_status)))
        r = "reserved_1: 0x{:02x} Shall be ignored"
        self.print(r.format(self.reserved_1))
        r = "reserved_2: 0x{:02x} Shall be ignored"
        self.print(r.format(self.reserved_2))
        r = "reserved_3: 0x{:02x} Shall be ignored"
        self.print(r.format(self.reserved_3))
        r = "reserved_4: 0x{:02x} Shall be ignored"
        self.print(r.format(self.reserved_4))


@attr.s
class MacPoll(pt.Command):
    SCHEMA = (t.uint16_t, dt.DeconzAddress, t.uint8_t, t.int8s, )

    payload_length = attr.ib(factory=SCHEMA[0])
    some_address = attr.ib(factory=SCHEMA[1])
    lqi = attr.ib(factory=SCHEMA[2])
    rssi = attr.ib(factory=SCHEMA[3])

    def pretty_print(self, *args):
        self.print("Payload length: {}".format(self.payload_length))
        self.print("Address: {}".format(self.some_address))
        if self.some_address.address_mode in (1, 2, 4):
            self.print("Address: 0x{:04x}".format(self.some_address.address))
        self.print("LQI: {}".format(self.lqi))
        self.print("RSSI: {}".format(self.rssi))


@attr.s
class ZGPDataInd(pt.Command):
    SCHEMA = (t.LongOctetString, )

    payload = attr.ib(factory=t.LongOctetString)

    def pretty_print(self, *args):
        self.print('Payload: {}'.format(binascii.hexlify(self.payload)))


@attr.s
class SimpleBeacon(pt.Command):
    SCHEMA = (t.uint16_t, t.NWK, t.NWK, t.uint8_t, t.uint8_t, t.uint8_t, )

    payload_length = attr.ib(factory=SCHEMA[0])
    SrcNWK = attr.ib(factory=SCHEMA[1])
    PanId = attr.ib(factory=SCHEMA[2])
    channel = attr.ib(factory=SCHEMA[3])
    flags = attr.ib(factory=SCHEMA[4])
    updateId = attr.ib(factory=SCHEMA[5])

    def pretty_print(self, *args):
        self.print("Payload length: {}".format(self.payload_length))
        self.print("Source NWK: {}".format(self.SrcNWK))
        self.print("PAN ID: {}".format(self.PanId))
        self.print("Channel: {}".format(self.channel))
        self.print("Flags: 0x{:02x}".format(self.flags))
        self.print("Update id: 0x{:02x}".format(self.updateId))
