from src.stage_type.Standa import Standa


class StandaTwoAxes:
    _axis1_settings = {
        "name": "Roll",
        "engine_settings_calb": 9,
        "unit_multiplier": 949,
        "speed": 30000
    }

    _axis2_settings = {
        "name": "Nick",
        "engine_settings_calb": 9,
        "unit_multiplier": 934,
        "speed": 30000
    }

    def __init__(self):
        self.stage_name = "standa116563"
        self.axis1 = None  # Roll
        self.axis2 = None  # Nick

        self.axis1_id = 1
        self.axis2_id = 2

        self._decimals = 5

    def open_connection(self):
        standa_handles = Standa.get_device_handles()
        if not standa_handles:  # gerät nicht gefunden
            print("Gerät wurde nicht gefunden! Überprüfe, ob angeschlossen!")
            return False
        else:  # gerät gefunden
            try:
                print("Handles:", standa_handles)
                axis2 = Standa(standa_handles[0])
                axis1 = Standa(standa_handles[1])
                if axis1.get_serial_number() == "30314":
                    self.axis1 = axis1
                    self.axis2 = axis2
                else:
                    self.axis1 = axis2
                    self.axis2 = axis1

                self.axis1.set_default_settings(self._axis1_settings)
                self.axis2.set_default_settings(self._axis2_settings)
                return True
            except Exception as e:
                self.close_connection()
                print(f"Es konnten nicht alle Achsen gefunden werden!\n"
                      f"Gefundene Handles: {standa_handles}\n"
                      f"Fehler: {e}")

    def close_connection(self):
        try:
            self.axis1.close_connection()
            self.axis2.close_connection()
            return True
        except Exception as e:
            return False

    def set_home(self):
        self.axis1.set_home()
        self.axis2.set_home()

    def go_home(self):
        self.axis1.move_absolut(0.0)
        self.axis2.move_absolut(0.0)

    def get_angle(self, axis: int):
        if isinstance(axis, (str, float)):
            try:
                axis = int(axis)
            except AttributeError:
                axis = 1
        position = eval(f"self.axis{axis}").get_position_calb()
        return round(position, self._decimals)

    def move_absolut(self, axis: int, position: float):
        if isinstance(axis, (str, float)):
            try:
                axis = int(axis)
            except AttributeError:
                axis = 1
        eval(f"self.axis{axis}").move_absolut(position)

    def move_relative(self, axis: int, position: float):
        if isinstance(axis, (str, float)):
            try:
                axis = int(axis)
            except AttributeError:
                print(f"Axis {axis} does not exist!")
        eval(f"self.axis{axis}").move_relative(position)

    def move_towards(self, axis: int, position: float):
        if isinstance(axis, (str, float)):
            try:
                axis = int(axis)
            except AttributeError:
                axis = 1
        eval(f"self.axis{axis}").move_towards(position)

    def stop_movement(self):
        self.axis1.stop()
        self.axis2.stop()
