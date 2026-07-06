#!/usr/bin/env python

from array import array

import pyipmi.msgs.dcmi

from pyipmi.msgs import encode_message, decode_message


def test_getdcmicapabilities_encode_valid_req():
    m = pyipmi.msgs.dcmi.GetDcmiCapabilitiesReq()
    m.parameter_selector = 1
    data = encode_message(m)
    assert m.__netfn__ == 0x2c
    assert m.__cmdid__ == 1
    assert data == b'\xdc\x01'


def test_getdcmicapabilities_decode_valid_rsp():
    m = pyipmi.msgs.dcmi.GetDcmiCapabilitiesRsp()
    decode_message(m, b'\x00\xdc\x01\x05\x02\xaa\xbb')
    assert m.completion_code == 0x00
    assert m.group_extension_id == 0xdc
    assert m.specification_conformence.major == 1
    assert m.specification_conformence.minor == 5
    assert m.parameter_revision == 2
    assert m.parameter_data == array('B', [0xaa, 0xbb])


def test_getpowerreading_encode_valid_req():
    m = pyipmi.msgs.dcmi.GetPowerReadingReq()
    m.mode = 1
    data = encode_message(m)
    assert m.__netfn__ == 0x2c
    assert m.__cmdid__ == 2
    assert data == b'\xdc\x01\x00\x00'


def test_getpowerreading_decode_valid_rsp():
    m = pyipmi.msgs.dcmi.GetPowerReadingRsp()
    decode_message(
        m, b'\x00\xdc\x01\x00\x02\x00\x03\x00\x04\x00'
           b'\x05\x00\x00\x00\x06\x00\x00\x00\x07')
    assert m.completion_code == 0x00
    assert m.group_extension_id == 0xdc
    assert m.current_power == 1
    assert m.minimum_power == 2
    assert m.maximum_power == 3
    assert m.average_power == 4
    assert m.timestamp == 5
    assert m.period == 6
    assert m.reading_state == 7


def test_getpowerlimit_encode_valid_req():
    m = pyipmi.msgs.dcmi.GetPowerLimitReq()
    data = encode_message(m)
    assert m.__netfn__ == 0x2c
    assert m.__cmdid__ == 3
    assert data == b'\xdc'


def test_getpowerlimit_decode_valid_rsp():
    m = pyipmi.msgs.dcmi.GetPowerLimitRsp()
    decode_message(
        m, b'\x00\xdc\x00\x00\x01\xf4\x01\xe8\x03\x00\x00\x00\x00\x0a\x00')
    assert m.completion_code == 0x00
    assert m.group_extension_id == 0xdc
    assert m.exception_actions == 1
    assert m.power_limit_requested == 500
    assert m.correction_time_limit == 1000
    assert m.statistics_sampling_period == 10


def test_setpowerlimit_encode_valid_req():
    m = pyipmi.msgs.dcmi.SetPowerLimitReq()
    m.exception_actions = 1
    m.power_limit_requested = 500
    m.correction_time_limit = 1000
    m.statistics_sampling_period = 10
    data = encode_message(m)
    assert m.__netfn__ == 0x2c
    assert m.__cmdid__ == 4
    assert data == \
        b'\xdc\x00\x00\x00\x01\xf4\x01\xe8\x03\x00\x00\x00\x00\x0a\x00'


def test_setpowerlimit_decode_valid_rsp():
    m = pyipmi.msgs.dcmi.SetPowerLimitRsp()
    decode_message(m, b'\x00\xdc')
    assert m.completion_code == 0x00
    assert m.group_extension_id == 0xdc


def test_activatedeactivatepowerlimit_encode_valid_req():
    m = pyipmi.msgs.dcmi.GetActivateDeactivatePowerLimitReq()
    m.power_limit_activation.activate = 1
    data = encode_message(m)
    assert m.__netfn__ == 0x2c
    assert m.__cmdid__ == 5
    assert data == b'\xdc\x01'


def test_activatedeactivatepowerlimit_decode_valid_rsp():
    m = pyipmi.msgs.dcmi.GetActivateDeactivatePowerLimitRsp()
    decode_message(m, b'\x00\xdc')
    assert m.completion_code == 0x00
    assert m.group_extension_id == 0xdc


def test_getassettag_encode_valid_req():
    m = pyipmi.msgs.dcmi.GetAssetTagReq()
    m.offset_to_read = 0
    m.bytes_to_read = 10
    data = encode_message(m)
    assert m.__netfn__ == 0x2c
    assert m.__cmdid__ == 6
    assert data == b'\xdc\x00\x0a'


def test_getassettag_decode_valid_rsp():
    m = pyipmi.msgs.dcmi.GetAssetTagRsp()
    decode_message(m, b'\x00\xdc\x05Hello')
    assert m.completion_code == 0x00
    assert m.group_extension_id == 0xdc
    assert m.total_asset_tag_length == 5
    assert m.data == array('B', b'Hello')


def test_getdcmisensorinfo_encode_valid_req():
    m = pyipmi.msgs.dcmi.GetDcmiSensorInfoReq()
    m.sensor_type = 1
    m.entity_id = 2
    m.entity_instance = 3
    data = encode_message(m)
    assert m.__netfn__ == 0x2c
    assert m.__cmdid__ == 7
    assert data == b'\xdc\x01\x02\x03\x00'


def test_getdcmisensorinfo_decode_valid_rsp():
    m = pyipmi.msgs.dcmi.GetDcmiSensorInfoRsp()
    decode_message(m, b'\x00\xdc\x03\x02\x10\x20')
    assert m.completion_code == 0x00
    assert m.group_extension_id == 0xdc
    assert m.total_number_of_instances == 3
    assert m.number_of_record_ids == 2
    assert m.record_ids == array('B', [0x10, 0x20])


def test_setassettag_encode_valid_req():
    m = pyipmi.msgs.dcmi.SetAssetTagReq()
    m.offset_to_write = 0
    m.bytes_to_write = 3
    m.data = array('B', b'abc')
    data = encode_message(m)
    assert m.__netfn__ == 0x2c
    assert m.__cmdid__ == 8
    assert data == b'\xdc\x00\x03abc'


def test_setassettag_decode_valid_rsp():
    m = pyipmi.msgs.dcmi.SetAssetTagRsp()
    decode_message(m, b'\x00\xdc\x05')
    assert m.completion_code == 0x00
    assert m.group_extension_id == 0xdc
    assert m.total_asset_tag_length == 5


def test_getmanagementcontrolleridstring_encode_valid_req():
    m = pyipmi.msgs.dcmi.GetManagementControllerIdStringReq()
    m.offset_to_read = 0
    m.bytes_to_read = 16
    data = encode_message(m)
    assert m.__netfn__ == 0x2c
    assert m.__cmdid__ == 9
    assert data == b'\xdc\x00\x10'


def test_getmanagementcontrolleridstring_decode_valid_rsp():
    m = pyipmi.msgs.dcmi.GetManagementControllerIdStringRsp()
    decode_message(m, b'\x00\xdc\x04Test')
    assert m.completion_code == 0x00
    assert m.group_extension_id == 0xdc
    assert m.total_length == 4
    assert m.data == array('B', b'Test')


def test_setmanagementcontrolleridstring_encode_valid_req():
    m = pyipmi.msgs.dcmi.SetManagementControllerIdStringReq()
    m.offset_to_write = 0
    m.data = array('B', b'Test')
    data = encode_message(m)
    assert m.__netfn__ == 0x2c
    assert m.__cmdid__ == 0x0a
    assert data == b'\xdc\x00Test'


def test_setmanagementcontrolleridstring_decode_valid_rsp():
    m = pyipmi.msgs.dcmi.SetManagementControllerIdStringRsp()
    decode_message(m, b'\x00\xdc\x04')
    assert m.completion_code == 0x00
    assert m.group_extension_id == 0xdc
    assert m.last_offset_written == 4
