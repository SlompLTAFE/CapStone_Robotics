"""Arm controller wrapper for the Hiwonder xArm."""

import xarm


class ArmController:
    """Provides a simplified interface to the xArm controller."""

    MIN_POSITION = 0
    MAX_POSITION = 1000

    MIN_SERVO_ID = 1
    MAX_SERVO_ID = 6

    # Initial movement mapping.
    CENTRE_POSITION = 500
    POSITION_RANGE = 250

    def __init__(self, controller=None):
        """Connect to the xArm or accept an injected controller."""

        if controller is None:
            try:
                controller = xarm.Controller("USB")
            except Exception as error:
                raise RuntimeError(
                    f"Could not connect to the xArm: {error}"
                ) from error

        if controller is None:
            raise RuntimeError("No xArm controller was provided.")

        self._controller = controller
        self._closed = False

    def _validate_servo_id(self, servo_id):
        """Check that the servo ID is valid."""

        if not isinstance(servo_id, int) or isinstance(servo_id, bool):
            raise ValueError("Servo ID must be an integer.")

        if not self.MIN_SERVO_ID <= servo_id <= self.MAX_SERVO_ID:
            raise ValueError("Servo ID must be between 1 and 6.")

    def _validate_position(self, position):
        """Check that a servo position is within range."""

        if not isinstance(position, int) or isinstance(position, bool):
            raise ValueError("Position must be an integer.")

        if not self.MIN_POSITION <= position <= self.MAX_POSITION:
            raise ValueError("Position must be between 0 and 1000.")

    def _ensure_open(self):
        """Prevent commands after the controller is closed."""

        if self._closed:
            raise RuntimeError("ArmController is closed.")

    def move_servo(self, servo_id, position, duration_ms):
        """Move one servo to a requested position."""

        self.move_servos([(servo_id, position)], duration_ms)

    def move_servos(self, moves, duration_ms):
        """Move multiple servos simultaneously."""

        self._ensure_open()

        if not isinstance(duration_ms, int) or duration_ms <= 0:
            raise ValueError("Duration must be a positive integer.")

        servos = []

        for servo_id, position in moves:
            self._validate_servo_id(servo_id)
            self._validate_position(position)

            servos.append(xarm.Servo(servo_id, position))

        if not servos:
            raise ValueError("At least one servo movement is required.")

        self._controller.setPosition(
            servos,
            duration=duration_ms,
            wait=False
        )

    def read_servo_positions(self, servo_ids):
        """Read the current position of each requested servo."""

        self._ensure_open()

        positions = {}

        for servo_id in servo_ids:
            self._validate_servo_id(servo_id)
            positions[servo_id] = self._controller.getPosition(servo_id)

        return positions

    def get_battery_voltage(self):
        """Return the controller voltage in volts."""

        self._ensure_open()
        return self._controller.getBatteryVoltage()

    def unload_servos(self, servo_ids):
        """Release the torque of selected servos."""

        self._ensure_open()

        for servo_id in servo_ids:
            self._validate_servo_id(servo_id)

        self._controller.servoOff(list(servo_ids))

    def _calculate_angles(self, x, y):
        """Map screen coordinates to initial pan and tilt positions."""

        # Screen centre is (400, 300).
        normalised_x = (x - 400) / 400
        normalised_y = (300 - y) / 300

        # Initial mapping assumes positive x = increasing pan,
        # and positive y-up = increasing tilt.
        pan = self.CENTRE_POSITION + (
            normalised_x * self.POSITION_RANGE
        )

        tilt = self.CENTRE_POSITION + (
            normalised_y * self.POSITION_RANGE
        )

        return round(pan), round(tilt)

    def point_at(self, x, y, duration_ms=500):
        """Move the pan and tilt servos towards a screen target."""

        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise ValueError("Target coordinates must be numeric.")

        if not 0 <= x <= 800 or not 0 <= y <= 600:
            raise ValueError("Target must be inside the 800x600 space.")

        pan, tilt = self._calculate_angles(x, y)

        self.move_servos(
            [(1, pan), (2, tilt)],
            duration_ms
        )

    def close(self):
        """Release the controller connection."""

        if not self._closed:
            self._closed = True

            close_method = getattr(self._controller, "close", None)

            if callable(close_method):
                close_method()

    def __enter__(self):
        self._ensure_open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

