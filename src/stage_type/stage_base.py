from abc import ABC, abstractmethod

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMessageBox


class ErrorPopup(QWidget):
    def __init__(self, message):
        super().__init__()
        self.message = message
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

        self.open_msg_box()

    def open_msg_box(self):
        QMessageBox.information(self, "Info", self.message, QMessageBox.Ok)

    def close_popup(self):
        self.close()


class StageBase(ABC):

    @abstractmethod
    def open_connection(self, serialnumber: str) -> bool:
        """Opens a connection to the controller device using the provided serial number. This method initializes a
        connection to the controller device specified by the serial number. Upon successful connection, it activates
        reference mode and servo control.

        :param serialnumber: The serial number used to establish the connection.
        :return: True if the connection is successfully established; otherwise, False.
        """
        pass

    @abstractmethod
    def close_connection(self, serialnumber: str) -> bool:
        """Closes the connection to the controller device.  This method terminates the connection to the controller
        device. It checks if the connection was closed and returns the status accordingly.

        :return: True if the connection is successfully closed; otherwise, False.
        """
        pass

    @abstractmethod
    def start_reference(self, reference_mode: int):
        """Initiates a reference operation based on the provided mode. This method starts a reference operation based on
        the given mode. It sets velocity, performs the specified reference mode action, waits for movement, and sets the
        home position. Finally, it retrieves and returns the final reference position attained.

        :param reference_mode: An integer representing the reference mode:
                               0 - Manual Reference
                               1 - Find Negative Limit (FNL)
                               2 - Find Positive Limit (FPL)
                               3 - Find Reference (FRF)
        :return: The final reference position attained.
        """
        pass

    @abstractmethod
    def set_home_position(self):
        """Sets the home position for the device. This method triggers the command to define the home position. It
        retrieves and sets the minimum and maximum position ranges for subsequent movements.
        """
        pass

    @abstractmethod
    def move_to_home_position(self):
        """Moves the device to the defined home position. Initiates movement to the previously defined home position."""
        pass

    @abstractmethod
    def move_relative(self, position: float):
        """Moves the device to a relative position. This method calculates the absolute position based on the current
        position and the provided relative position. It checks if the calculated position is within the device's range
        and moves accordingly.

        :param position: The relative position to move.
        :return: True if the movement is successful within the device's range; otherwise, False.
        """
        pass

    @abstractmethod
    def move_absolut(self, position: float):
        """ Moves the device to an absolute position. This method checks if the provided absolute position is within
        the device's range and moves accordingly.

        :param position: The absolute position to move.
        :return: True if the movement is successful within the device's range; otherwise, False.
        """
        pass

    @abstractmethod
    def move(self, movement: str, axes: int, position: float):
        """ This function executes absoult and relative movements of the stage and handles errors. If an error occurs it
        opens a pop-up window to the user with tipps to solve the problem.

        :param movement: kind of ovement can be absolut ot relative
        :param axes:     axes of the stage
        :param position: postion to reach
        :return:
        """
        pass

    @abstractmethod
    def move_to_negative_limit(self):
        """Moves the device to the negative limit. Initiates movement to the negative limit of the device's range."""
        pass

    @abstractmethod
    def move_to_positive_limit(self):
        """Moves the device to the positive limit. Initiates movement to the positive limit of the device's range."""
        pass

    @abstractmethod
    def wait_for_move(self):
        """Waits for the device to complete movement. This method pauses execution until the device completes its
        ongoing movement."""
        pass

    @abstractmethod
    def get_move(self) -> float:
        """Retrieves the current position of the device. This method queries and returns the current position of the
        device.

        :return: The current position of the device as a floating-point value.
        """
        pass

    @abstractmethod
    def get_home_position(self) -> float:
        """Retrieves the defined home position of the device. This method queries and returns the defined home position
        of the device.

        :return: The defined home position of the device.
        """
        pass

    @abstractmethod
    def get_velocity(self) -> float:
        """Retrieves the current velocity setting of the device. This method queries and returns the current velocity
        setting of the device.

        :return: The current velocity setting of the device as a floating-point value.
        """
        pass

    @abstractmethod
    def set_velocity(self, velocity: float):
        """Sets the velocity for device movements. This method sets the velocity for the device movements,
        ensuring it doesn't exceed the maximum velocity limit.

        :param velocity: The velocity to set for device movements.
        """
        pass

    @abstractmethod
    def stop_movement(self):
        """Stops the ongoing movement of the device. This method halts the ongoing movement of the device."""
        pass

    @abstractmethod
    def stop_all(self):
        """Stops all ongoing actions of the device. This method halts all ongoing actions or movements of the device."""
        pass
