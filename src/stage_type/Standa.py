import os
import sys
from pathlib import Path

from src.stage_type.STANDA_bindings import *


class Standa:
    """
    load alle Standa dlls
    """
    if getattr(sys, 'frozen', False):
        application_path: str = sys._MEIPASS
    else:
        application_path: str = Path(__file__).parents[1]

    dll_file = os.path.join(application_path, "libs\\libximc.dll")
    lib = WinDLL(dll_file)
    lib_cdecl = CDLL(dll_file)

    @staticmethod
    def get_device_handles():
        """
        Erstellt für jede Achse ein handle (Identifikationsschlüssel) mit dem ein Objekt der Achsen erstellt werden kann
        :return: handels
        """
        flags = EnumerateFlags.ENUMERATE_PROBE + EnumerateFlags.ENUMERATE_ALL_COM
        Standa.lib.enumerate_devices.restype = POINTER(device_enumeration_t)
        devenum = Standa.lib.enumerate_devices(c_int(flags), None)
        dev_count = Standa.lib.get_device_count(devenum)
        print("dev_count", dev_count)

        controller_name = controller_name_t()
        list_handle = []
        for dev_ind in range(0, dev_count):
            Standa.lib.get_device_name.restype = c_char_p
            enum_name = Standa.lib.get_device_name(devenum, dev_ind)
            Standa.lib.get_enumerate_device_controller_name(devenum, dev_ind, byref(controller_name))
            handle = Standa.lib.open_device(enum_name)
            print("enum_name:", enum_name, "dev_ind:", dev_ind)
            list_handle.append(handle)
        return list_handle

    def __init__(self, handle: object) -> object:
        """
        :param handle: id für die Ansteuerung der Achsen
        """
        self.handle = handle
        self._last_error = 0
        self._interval = 20
        self.lib = Standa.lib
        self._init_structures()

    def get_serial_number(self) -> str:
        serial = c_uint()
        self._last_error = self.lib.get_serial_number(self.handle, byref(serial))
        if self._last_error == Result.Ok:
            return repr(serial.value)

    def set_default_settings(self, settings: dict):
        self.set_engine_settings_calb(settings["engine_settings_calb"])
        self.set_user_unit(settings["unit_multiplier"])
        self.set_speed(settings["speed"])

    def close_connection(self):  # funktioniert
        self.lib.close_device(byref(cast(self.handle, POINTER(c_int))))
        return True

    def get_position_calb(self) -> float:
        self._last_error = self.lib.get_position_calb(self.handle, byref(self.get_position_calb_t),
                                                      byref(self.calibration_t))
        if self._last_error == Result.Ok:
            return self.get_position_calb_t.Position
        else:
            return 0.0

    def set_home(self):
        self._last_error = self.lib.command_zero(self.handle)

    def stop(self):
        self._last_error = self.lib.command_sstp(self.handle)

    def move_absolut(self, value: float):
        self._set_move_direction(value)
        self._last_error = self.lib.command_move_calb(self.handle, c_float(value), byref(self.calibration_t))
        self._last_error = self.lib.command_wait_for_stop(self.handle, self._interval)  # self._intervalms

    def move_towards(self, value: float):
        self._set_move_direction(value)
        self._last_error = self.lib.command_move_calb(self.handle, c_float(value), byref(self.calibration_t))

    def move_relative(self, value: float):
        current_position = self.get_position_calb()
        new_position = current_position + value
        self._set_move_direction(new_position)
        self._last_error = self.lib.command_move_calb(self.handle, c_float(new_position), byref(self.calibration_t))
        self._last_error = self.lib.command_wait_for_stop(self.handle, self._interval)  # self._intervalms

    def _set_move_direction(self, value: float):
        if value < 0.0:
            self._last_error = self.lib.command_left(self.handle)  # move left
        else:
            self._last_error = self.lib.command_right(self.handle)  # move rigth

    def get_speed(self) -> int:
        self._last_error = self.lib.get_move_settings(self.handle, byref(self.move_settings_t))
        if self._last_error == Result.Ok:
            return self.move_settings_t.Speed

    def set_speed(self, speed: int):
        self.move_settings_t.Speed = int(speed)
        self._last_error = self.lib.set_move_settings(self.handle, byref(self.move_settings_t))

    def set_engine_settings_calb(self, mode: int):  # funktioniert
        self._last_error = self.lib.get_engine_settings_calb(self.handle, byref(self.engine_settings_calb_t),
                                                             byref(self.calibration_t))
        self.engine_settings_calb_t.MicrostepMode = mode
        self._last_error = self.lib.set_engine_settings_calb(self.handle, byref(self.engine_settings_calb_t),
                                                             byref(self.calibration_t))

    def set_user_unit(self, multiplier: int):  # testen
        """Definierte Werte für Conversion nach: user_value = A*(step + mstep/pow(2,MicrostepMode-1))
        :param multiplier: Multiplikationsfaktor
        :return:
        """
        self._last_error = self.lib.get_engine_settings_calb(self.handle, byref(self.engine_settings_calb_t),
                                                             byref(self.calibration_t))
        self.calibration_t.MicrostepMode = self.engine_settings_calb_t.MicrostepMode

        self.calibration_t.A = 1 / multiplier

    def _init_structures(self):
        self.device_information_t = device_information_t()
        self.status_t = status_t()

        self.engine_settings_t = engine_settings_t()
        self.engine_settings_calb_t = engine_settings_calb_t()

        self.calibration_t = calibration_t()
        self.calibration_settings_t = calibration_settings_t()

        self.get_position_t = get_position_t()
        self.get_position_calb_t = get_position_calb_t()

        self.move_settings_t = move_settings_t()
