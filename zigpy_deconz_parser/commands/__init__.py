import zigpy_deconz_parser.types as pt
from . import requests
from . import responses

REQUESTS = {
    pt.DeConzCommand.VERSION: requests.Version,
    pt.DeConzCommand.READ_PARAMETER: requests.ReadParameter,
    pt.DeConzCommand.WRITE_PARAMETER: requests.WriteParameter,
    pt.DeConzCommand.DEVICE_STATE: requests.DeviceState,
    pt.DeConzCommand.CHANGE_NETWORK_STATE: requests.ChangeNetworkState,
    pt.DeConzCommand.APS_DATA_INDICATION: requests.ApsDataIndication,
}

RESPONSES = {
    pt.DeConzCommand.VERSION: responses.Version,
    pt.DeConzCommand.READ_PARAMETER: responses.ReadParameter,
    pt.DeConzCommand.WRITE_PARAMETER: responses.WriteParameter,
    pt.DeConzCommand.DEVICE_STATE: responses.DeviceState,
    pt.DeConzCommand.CHANGE_NETWORK_STATE: responses.ChangeNetworkState,
    pt.DeConzCommand.DEVICE_STATE_CHANGED: responses.DeviceStateChanged,
    pt.DeConzCommand.APS_DATA_INDICATION: responses.ApsDataIndication,
}

