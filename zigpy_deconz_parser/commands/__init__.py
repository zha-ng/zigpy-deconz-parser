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
    pt.DeConzCommand.APS_DATA_REQUEST: requests.ApsDataRequest,
    pt.DeConzCommand.APS_DATA_CONFIRM: requests.ApsDataConfirm,
}

RESPONSES = {
    pt.DeConzCommand.VERSION: responses.Version,
    pt.DeConzCommand.READ_PARAMETER: responses.ReadParameter,
    pt.DeConzCommand.WRITE_PARAMETER: responses.WriteParameter,
    pt.DeConzCommand.DEVICE_STATE: responses.DeviceState,
    pt.DeConzCommand.CHANGE_NETWORK_STATE: responses.ChangeNetworkState,
    pt.DeConzCommand.DEVICE_STATE_CHANGED: responses.DeviceStateChanged,
    pt.DeConzCommand.APS_DATA_INDICATION: responses.ApsDataIndication,
    pt.DeConzCommand.APS_DATA_REQUEST: responses.ApsDataRequest,
    pt.DeConzCommand.APS_DATA_CONFIRM: responses.ApsDataConfirm,
    pt.DeConzCommand.MAC_POLL: responses.MacPoll,
    pt.DeConzCommand.ZGP_DATA_IND: responses.ZGPDataInd,
    pt.DeConzCommand.SIMPLE_BEACON: responses.SimpleBeacon,
}

