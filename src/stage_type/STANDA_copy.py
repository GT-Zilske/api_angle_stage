import os
import sys
from pathlib import Path

from src.stage_type.STANDA_bindings import *


class STANDA:
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

    @staticmethod  # funktioniert
    def CreateInstance():
        """
        Erstellt für jede Achse ein handle (Identifikationsschlüssel) mit dem ein Objekt der Achsen erstellt werden kann
        :return: handels
        """
        flags = EnumerateFlags.ENUMERATE_PROBE + EnumerateFlags.ENUMERATE_ALL_COM
        STANDA.lib.enumerate_devices.restype = POINTER(device_enumeration_t)
        devenum = STANDA.lib.enumerate_devices(c_int(flags), None)
        dev_count = STANDA.lib.get_device_count(devenum)
        print("Anzahl der Geräte: " + repr(dev_count))

        controller_name = controller_name_t()
        list_handle = []
        for dev_ind in range(0, dev_count):
            STANDA.lib.get_device_name.restype = c_char_p
            enum_name = STANDA.lib.get_device_name(devenum, dev_ind)
            STANDA.lib.get_enumerate_device_controller_name(devenum, dev_ind, byref(controller_name))

            print(f"\nInformationen Gerät {dev_ind}:\nPort: {enum_name.decode()}\n"
                  f"Name: {controller_name.ControllerName.decode()}")
            handle = STANDA.lib.open_device(enum_name)
            print(f"Verbinde mit {repr(enum_name)} über Handle {repr(handle)}.")
            list_handle.append(handle)

        return list_handle

    def __init__(self, handle: object) -> object:
        """
        :param handle: id für die Ansteuerung der Achsen
        """
        self.handle = handle
        self._last_error = 0
        self.lib = STANDA.lib
        self.init_structures()

    def init_structures(self):
        self.device_information_t = device_information_t()
        self.status_t = status_t()

        self.engine_settings_t = engine_settings_t()
        self.engine_settings_calb_t = engine_settings_calb_t()

        self.calibration_t = calibration_t()
        self.calibration_settings_t = calibration_settings_t()

        self.get_position_t = get_position_t()
        self.get_position_calb_t = get_position_calb_t()

        self.move_settings_t = move_settings_t()

    def close_connection(self):  # funktioniert
        self.lib.close_device(byref(cast(self.handle, POINTER(c_int))))
        return False

    def get_version(self):  # funktioniert
        """
        Abruf der Versionsnummer

        :return: Nichts
        """
        sbuf = create_string_buffer(64)
        self.lib.ximc_version(sbuf)

    def get_serial_number(self):  # funktioniert
        print("\nSeriennummer abrufen...")
        serial = c_uint()
        self._last_error = self.lib.get_serial_number(self.handle, byref(serial))
        if self._last_error == Result.Ok:
            print("Seriennummer: " + repr(serial.value))

    def set_bindy_key(self):  # testen
        """
        Wird bei ein Netzwerk Verbindung benötigt.
        :return:
        """

        self._last_error = self.lib.set_bindy_key(
            os.path.join(self.ximc_dir, "win32", "keyfile.sqlite").encode("utf-8"))
        if self._last_error != Result.Ok:
            self.lib.set_bindy_key(
                "keyfile.sqlite".encode("utf-8"))  # Search for the key file in the current directory.

    def device_info(self):  # funktioniert
        """
        Siehe Doku oder Klasse mit Structures für mehr infos
        :return:
        """
        print("\nGeräteinformationen:")
        self._last_error = self.lib.get_device_information(self.handle, byref(self.device_information_t))
        if self._last_error == Result.Ok:
            print("Manufacturer: " +
                  repr(string_at(self.device_information_t.Manufacturer).decode()))
            print("ManufacturerId: " +
                  repr(string_at(self.device_information_t.ManufacturerId).decode()))
            print("ProductDescription: " +
                  repr(string_at(self.device_information_t.ProductDescription).decode()))
            print("Major: " + repr(self.device_information_t.Major))
            print("Minor: " + repr(self.device_information_t.Minor))
            print("Release: " + repr(self.device_information_t.Release))

    def device_status(self):  # funktioniert
        """
        Siehe Doku oder Klasse mit Structures für mehr infos

        :return:
        """
        print("\nGerätestatus:")
        self._last_error = self.lib.get_status(self.handle, byref(self.status_t))
        if self._last_error == Result.Ok:
            print("Status.Ipwr: " + repr(self.status_t.CurPosition))
            print("Status.Upwr: " + repr(self.status_t.Upwr))
            print("Status.Iusb: " + repr(self.status_t.Iusb))
            print("Status.Flags: " + repr(hex(self.status_t.Flags)))

    def get_position(self):  # funktioniert
        print("\nPosition abrufen...")

        self._last_error = self.lib.get_position(self.handle, byref(self.get_position_t))
        if self._last_error == Result.Ok:
            print(
                f"Position Achse {self.handle}: {self.get_position_t.Position} Steps, {self.get_position_t.uPosition} Microsteps")
        return self.get_position_t.Position, self.get_position_t.uPosition

    def get_speed(self):  # funktioniert
        print("\nGeschwindigkeit abrufen...")
        self._last_error = self.lib.get_move_settings(self.handle, byref(self.move_settings_t))
        print(f"Speed: {self.move_settings_t.Speed}")
        return self.move_settings_t.Speed

    def set_speed(self, speed):  # funktioniert
        print("\nGeschwindigkeit ändern...")
        self.move_settings_t.Speed = int(speed)
        print(f"Speed: {speed}")
        self._last_error = self.lib.set_move_settings(self.handle, byref(self.move_settings_t))

    def move(self, value: float):
        if value < 0.0:
            self.move_left()
            self.move_calb(value)
            self.wait_for_stop(50)
        else:
            self.move_right()
            self.move_calb(value)
            self.wait_for_stop(50)

    def move_left(self):  # funktioniert
        print("\nBewegung nach links...")
        self._last_error = self.lib.command_left(self.handle)
        print("Result: " + repr(self._last_error))

    def move_right(self):  # funktioniert
        print("\nBewegung nach rechts...")
        self._last_error = self.lib.command_right(self.handle)
        print("Result: " + repr(self._last_error))

    def move_uncalb(self, distance, udistance):  # funktioniert
        print("\nGoing to {0} steps, {1} microsteps".format(distance, udistance))
        self._last_error = self.lib.command_move(self.handle, distance, udistance)
        print("Result: " + repr(self._last_error))

    def move_calb(self, distance):  # funktioniert
        print("\nMove to {0}".format(round(distance, 3)))
        self._last_error = self.lib.command_move_calb(self.handle, c_float(distance), byref(self.calibration_t))
        print("Result: " + repr(self._last_error))

    def wait_for_stop(self, interval):  # funktioniert
        print("\nWarte bis die Bewegung ausgeführt wird.")
        self._last_error = self.lib.command_wait_for_stop(self.handle, interval)
        print("Result: " + repr(self._last_error))

    def get_device_information(self):  # testen
        print("\nKalibrierungseinstellungen abrufen...")
        self.lib.get_device_information(self.handle, byref(self.device_information_t))
        print(f"Manufacturer: {self.device_information_t.Manufacturer}")
        print(f"ManufacturerId: {self.device_information_t.ManufacturerId}")
        print(f"ProductDescription: {self.device_information_t.ProductDescription}")
        print(f"Major: {self.device_information_t.Major}")
        print(f"Minor: {self.device_information_t.Minor}")
        print(f"Release: {self.device_information_t.Release}")

    def get_calibration_settings(self):  # testen
        print("\nKalibrierungseinstellungen abrufen...")
        self.lib.get_calibration_settings(self.handle, byref(self.calibration_settings_t))
        print(f"CSS1_A: {self.calibration_settings_t.CSS1_A}")
        print(f"CSS1_B: {self.calibration_settings_t.CSS1_B}")
        print(f"CSS2_A: {self.calibration_settings_t.CSS2_A}")
        print(f"CSS2_B: {self.calibration_settings_t.CSS2_B}")
        print(f"FullCurrent_A: {self.calibration_settings_t.FullCurrent_A}")
        print(f"FullCurrent_B: {self.calibration_settings_t.FullCurrent_B}")

    def get_engine_settings(self):  # testen
        print("\nMotoreinstellungen abrufen...")
        self.lib.get_engine_settings(self.handle, byref(self.engine_settings_t))
        print(f"MicrostepMode: {self.engine_settings_t.MicrostepMode}")

    def get_move_settings(self):  # testen
        print("\nMotoreinstellungen abrufen...")
        self.lib.get_move_settings(self.handle, byref(self.move_settings_t))
        print(f"MicrostepMode: {self.engine_settings_t.MicrostepMode}")

    def set_OpenSettings(self, A=860):
        self.set_engine_settings_calb(9)
        self.set_user_unit(A)

    def set_engine_settings_calb(self, mode=9):  # funktioniert
        """
        Im Programm mit ComboBox für alle Modes erstellen.
        :return:
        """
        print("\nSet microstep mode...")
        self._last_error = self.lib.get_engine_settings_calb(self.handle, byref(self.engine_settings_calb_t),
                                                             byref(self.calibration_t))
        self.engine_settings_calb_t.MicrostepMode = mode
        self._last_error = self.lib.set_engine_settings_calb(self.handle, byref(self.engine_settings_calb_t),
                                                             byref(self.calibration_t))

    def set_user_unit(self, multiplier=860):  # testen
        """
        Definierte Werte für Conversion nach:
        user_value = A*(step + mstep/pow(2,MicrostepMode-1))

        :param multiplier: Multiplikationsfaktor
        :return:
        """
        print("\nEinheit ändern...")
        self._last_error = self.lib.get_engine_settings_calb(self.handle, byref(self.engine_settings_calb_t),
                                                             byref(self.calibration_t))
        self.calibration_t.MicrostepMode = self.engine_settings_calb_t.MicrostepMode
        print("MicrostepMode = ", self.calibration_t.MicrostepMode)

        self.calibration_t.A = 1 / multiplier
        print("User unit coordinate multiplier = ", self.calibration_t.A)

    def get_position_calb(self):  # funktioniert
        print("\nPosition abrufen...")
        self._last_error = self.lib.get_position_calb(self.handle, byref(self.get_position_calb_t),
                                                      byref(self.calibration_t))
        if self._last_error == Result.Ok:
            print(f"Position Achse {self.handle}: {self.get_position_calb_t.Position} Grad")
        return self.get_position_calb_t.Position

    def set_command_zero(self):
        self._last_error = self.lib.command_zero(self.handle)
