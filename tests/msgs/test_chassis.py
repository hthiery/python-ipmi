#!/usr/bin/env python

from array import array

import pyipmi.msgs.chassis

from pyipmi.msgs import encode_message, decode_message


def test_getchassisstatus_encode_valid_req():
    m = pyipmi.msgs.chassis.GetChassisStatusReq()
    data = encode_message(m)
    assert m.__netfn__ == 0
    assert m.__cmdid__ == 1
    assert data == b''


def test_getchassisstatus_decode_valid_rsp():
    m = pyipmi.msgs.chassis.GetChassisStatusRsp()
    decode_message(m, b'\x00\xea\xaa\xaa')
    assert m.completion_code == 0x00
    assert m.current_power_state.power_on == 0
    assert m.current_power_state.power_overload == 1
    assert m.current_power_state.interlock == 0
    assert m.current_power_state.power_fault == 1
    assert m.current_power_state.power_control_fault == 0
    assert m.current_power_state.power_restore_policy == 3

    assert m.last_power_event.ac_failed == 0
    assert m.last_power_event.power_overload == 1
    assert m.last_power_event.power_interlock == 0
    assert m.last_power_event.power_fault == 1
    assert m.last_power_event.power_is_on_via_ipmi_command == 0

    assert m.misc_chassis_state.chassis_intrusion_active == 0
    assert m.misc_chassis_state.front_panel_lockout_active == 1
    assert m.misc_chassis_state.drive_fault == 0
    assert m.misc_chassis_state.cooling_fault_detected == 1


def test_getchassisstatus_decode_valid_optional_byte_rsp():
    m = pyipmi.msgs.chassis.GetChassisStatusRsp()
    decode_message(m, b'\x00\x00\x00\00\xaa')
    assert m.completion_code == 0x00
    assert m.front_panel_button_capabilities == 0xaa


def test_chassiscontrol_encode_valid_req():
    m = pyipmi.msgs.chassis.ChassisControlReq()
    m.control.option = 1
    data = encode_message(m)
    assert m.__netfn__ == 0
    assert m.__cmdid__ == 2
    assert data == b'\x01'


def test_getsystembootoptions_encode_valid_req():
    m = pyipmi.msgs.chassis.GetSystemBootOptionsReq()
    m.parameter_selector.boot_option_parameter_selector = 5
    data = encode_message(m)
    assert m.__netfn__ == 0
    assert m.__cmdid__ == 9
    assert data == b'\x05\x00\x00'


def test_getsystembootoptions_decode_valid_rsp():
    m = pyipmi.msgs.chassis.GetSystemBootOptionsRsp()
    decode_message(m, b'\x00\x01\x85\x00\x08\x00\x00\x00')

    assert m.completion_code == 0x00
    assert m.parameter_version.parameter_version == 1
    assert m.parameter_valid.boot_option_parameter_selector == 5
    assert m.parameter_valid.parameter_validity == 1
    assert m.data == array('B', b'\x00\x08\x00\x00\x00')


def test_setsystembootoptions_encode_valid_req():
    m = pyipmi.msgs.chassis.SetSystemBootOptionsReq()
    m.parameter_selector.boot_option_parameter_selector = 5
    m.parameter_selector.parameter_validity = 1
    m.data = array('B', b'\x70\x08\x00\x00\x00')
    data = encode_message(m)

    assert m.__netfn__ == 0
    assert m.__cmdid__ == 8
    assert data == b'\x85\x70\x08\x00\x00\x00'


def test_setsystembootoptions_decode_valid_rsp():
    m = pyipmi.msgs.chassis.SetSystemBootOptionsRsp()
    decode_message(m, b'\x00')

    assert m.completion_code == 0x00


def test_chassisreset_encode_valid_req():
    m = pyipmi.msgs.chassis.ChassisResetReq()
    data = encode_message(m)
    assert m.__netfn__ == 0
    assert m.__cmdid__ == 3
    assert data == b''


def test_chassisreset_decode_valid_rsp():
    m = pyipmi.msgs.chassis.ChassisResetRsp()
    decode_message(m, b'\x00')
    assert m.completion_code == 0x00


def test_chassisidentify_encode_valid_req_no_data():
    m = pyipmi.msgs.chassis.ChassisIdentifyReq()
    data = encode_message(m)
    assert m.__netfn__ == 0
    assert m.__cmdid__ == 4
    assert data == b''


def test_chassisidentify_encode_valid_req_interval_only():
    m = pyipmi.msgs.chassis.ChassisIdentifyReq()
    m.identify_interval = 10
    data = encode_message(m)
    assert data == b'\x0a'


def test_chassisidentify_encode_valid_req_force_on():
    m = pyipmi.msgs.chassis.ChassisIdentifyReq()
    m.identify_interval = 0
    m.force_identify_on = 1
    data = encode_message(m)
    assert data == b'\x00\x01'


def test_chassisidentify_decode_valid_req_no_data():
    m = pyipmi.msgs.chassis.ChassisIdentifyReq()
    decode_message(m, b'')
    assert m.identify_interval is None
    assert m.force_identify_on is None


def test_chassisidentify_decode_valid_req_full():
    m = pyipmi.msgs.chassis.ChassisIdentifyReq()
    decode_message(m, b'\x0a\x01')
    assert m.identify_interval == 10
    assert m.force_identify_on == 1


def test_chassisidentify_decode_valid_rsp():
    m = pyipmi.msgs.chassis.ChassisIdentifyRsp()
    decode_message(m, b'\x00')
    assert m.completion_code == 0x00


def test_setchassiscapabilities_encode_valid_req():
    m = pyipmi.msgs.chassis.SetChassisCapabilitiesReq()
    m.capabilities_flags.intrusion_sensor = 1
    m.capabilities_flags.diagnostic_interrupt = 1
    m.fru_info_device_address = 0x10
    m.sdr_device_address = 0x11
    m.sel_device_address = 0x12
    m.system_management_device_address = 0x13
    data = encode_message(m)
    assert m.__netfn__ == 0
    assert m.__cmdid__ == 5
    assert data == b'\x05\x10\x11\x12\x13'


def test_setchassiscapabilities_encode_valid_req_with_bridge():
    m = pyipmi.msgs.chassis.SetChassisCapabilitiesReq()
    m.fru_info_device_address = 0x10
    m.sdr_device_address = 0x11
    m.sel_device_address = 0x12
    m.system_management_device_address = 0x13
    m.bridge_device_address = 0x14
    data = encode_message(m)
    assert data == b'\x00\x10\x11\x12\x13\x14'


def test_setchassiscapabilities_decode_valid_req():
    m = pyipmi.msgs.chassis.SetChassisCapabilitiesReq()
    decode_message(m, b'\x05\x10\x11\x12\x13')
    assert m.capabilities_flags.intrusion_sensor == 1
    assert m.capabilities_flags.frontpanel_lockout == 0
    assert m.capabilities_flags.diagnostic_interrupt == 1
    assert m.capabilities_flags.power_interlock == 0
    assert m.fru_info_device_address == 0x10
    assert m.sdr_device_address == 0x11
    assert m.sel_device_address == 0x12
    assert m.system_management_device_address == 0x13
    assert m.bridge_device_address is None


def test_setchassiscapabilities_decode_valid_rsp():
    m = pyipmi.msgs.chassis.SetChassisCapabilitiesRsp()
    decode_message(m, b'\x00')
    assert m.completion_code == 0x00


def test_setpowerrestorepolicy_encode_valid_req():
    m = pyipmi.msgs.chassis.SetPowerRestorePolicyReq()
    m.power_restore_policy.policy = \
        pyipmi.msgs.chassis.POWER_RESTORE_POLICY_ALWAYS_POWER_UP
    data = encode_message(m)
    assert m.__netfn__ == 0
    assert m.__cmdid__ == 6
    assert data == b'\x02'


def test_setpowerrestorepolicy_decode_valid_rsp():
    m = pyipmi.msgs.chassis.SetPowerRestorePolicyRsp()
    decode_message(m, b'\x00\x05')
    assert m.completion_code == 0x00
    assert m.power_restore_policy_support.stay_powered_off_supported == 1
    assert m.power_restore_policy_support.restore_previous_state_supported == 0
    assert m.power_restore_policy_support.always_power_up_supported == 1


def test_getsystemrestartcause_encode_valid_req():
    m = pyipmi.msgs.chassis.GetSystemRestartCauseReq()
    data = encode_message(m)
    assert m.__netfn__ == 0
    assert m.__cmdid__ == 7
    assert data == b''


def test_getsystemrestartcause_decode_valid_rsp():
    m = pyipmi.msgs.chassis.GetSystemRestartCauseRsp()
    decode_message(m, b'\x00\x04\x02')
    assert m.completion_code == 0x00
    assert m.restart_cause.cause == \
        pyipmi.msgs.chassis.RESTART_CAUSE_WATCHDOG_EXPIRATION
    assert m.channel.channel_number == 2
