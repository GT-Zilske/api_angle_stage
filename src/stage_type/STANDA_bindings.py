import enum
from ctypes import *


class Result:
    """
    Interpretierung der Antworten der funktionen
    """
    Ok = 0
    Error = -1
    NotImplemented = -2
    ValueError = -3
    NoDevice = -4


class EnumerateFlags(enum.IntEnum):
    ENUMERATE_PROBE = 0x01
    ENUMERATE_ALL_COM = 0x02
    ENUMERATE_NETWORK = 0x04


class MicrostepMode(enum.IntEnum):
    MICROSTEP_MODE_FULL = 0x01
    MICROSTEP_MODE_FRAC_2 = 0x02
    MICROSTEP_MODE_FRAC_4 = 0x03
    MICROSTEP_MODE_FRAC_8 = 0x04
    MICROSTEP_MODE_FRAC_16 = 0x05
    MICROSTEP_MODE_FRAC_32 = 0x06
    MICROSTEP_MODE_FRAC_64 = 0x07
    MICROSTEP_MODE_FRAC_128 = 0x08
    MICROSTEP_MODE_FRAC_256 = 0x09


class calibration_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('A', c_double),
        ('MicrostepMode', c_uint)
    ]


class calibration_settings_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('CSS1_A', c_float),
        ('CSS1_B', c_float),
        ('CSS2_A', c_float),
        ('CSS2_B', c_float),
        ('FullCurrent_A', c_float),
        ('FullCurrent_B', c_float)
    ]


class device_enumeration_t(LittleEndianStructure):  # stimmt nicht
    _pack_ = 1
    _fields_ = [
        ('A', c_int),
        ('MicrostepMode', c_uint)
    ]


class device_network_information_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('ipv4', c_uint32),
        ('nodename', c_char * 16),
        ('axis_state', c_uint),
        ('locker_username', c_char * 16),
        ('locker_nodename', c_char * 16),
        ('locked_time', c_ulonglong),
    ]


class device_information_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Manufacturer', c_char * 5),
        ('ManufacturerId', c_char * 3),
        ('ProductDescription', c_char * 9),
        ('Major', c_uint),
        ('Minor', c_uint),
        ('Release', c_uint),
    ]


class controller_name_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('ControllerName', c_char * 17),
        ('CtrlFlags', c_uint),
    ]


class status_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('MoveSts', c_uint),
        ('MvCmdSts', c_uint),
        ('PWRSts', c_uint),
        ('EncSts', c_uint),
        ('WindSts', c_uint),
        ('CurPosition', c_int),
        ('uCurPosition', c_int),
        ('EncPosition', c_long),
        ('CurSpeed', c_int),
        ('uCurSpeed', c_int),
        ('Ipwr', c_int),
        ('Upwr', c_int),
        ('Iusb', c_int),
        ('Uusb', c_int),
        ('Upwr', c_int),
        ('CurT', c_int),
        ('Flags', c_uint),
        ('GPIOFlags', c_uint),
        ('CmdBufFreeSpace', c_uint),
    ]


class status_calb_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('MoveSts', c_uint),
        ('MvCmdSts', c_uint),
        ('PWRSts', c_uint),
        ('EncSts', c_uint),
        ('WindSts', c_uint),
        ('CurPosition', c_float),
        ('EncPosition', c_long),
        ('CurSpeed', c_float),
        ('Ipwr', c_int),
        ('Upwr', c_int),
        ('Iusb', c_int),
        ('Uusb', c_int),
        ('Upwr', c_int),
        ('CurT', c_int),
        ('Flags', c_uint),
        ('GPIOFlags', c_uint),
        ('CmdBufFreeSpace', c_uint),
    ]


class get_position_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Position', c_int),
        ('uPosition', c_int),
        ('EncPosition', c_long),
    ]


class get_position_calb_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Position', c_float),
        ('EncPosition', c_long),
    ]


class set_position_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Position', c_int),
        ('uPosition', c_int),
        ('EncPosition', c_long),
        ('PosFlags', c_uint),
    ]


class set_position_calb_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Position', c_float),
        ('EncPosition', c_long),
        ('PosFlags', c_uint),
    ]


class engine_settings_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('NomVoltage', c_uint),
        ('NomCurrent', c_uint),
        ('NomSpeed', c_uint),
        ('uNomSpeed', c_uint),
        ('EngineFlags', c_uint),
        ('Antiplay', c_int),
        ('MicrostepMode', c_uint),
        ('StepsPerRev', c_uint),
    ]


class engine_settings_calb_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('NomVoltage', c_uint),
        ('NomCurrent', c_uint),
        ('NomSpeed', c_uint),
        ('EngineFlags', c_uint),
        ('Antiplay', c_int),
        ('MicrostepMode', c_uint),
        ('StepsPerRev', c_uint),
    ]


class move_settings_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Speed', c_uint),
        ('uSpeed', c_uint),
        ('Accel', c_uint),
        ('Decel', c_uint),
        ('AntiplaySpeed', c_uint),
        ('uAntiplaySpeed', c_int),
        ('MoveFlags', c_uint),
    ]


class move_settings_calb_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('Speed', c_float),
        ('Accel', c_float),
        ('Decel', c_float),
        ('AntiplaySpeed', c_float),
        ('MoveFlags', c_uint),
    ]
