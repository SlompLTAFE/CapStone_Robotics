
import pytest

from xarm_toolkit import ArmController


class FakeController:

    def __init__(self):
        self.commands = []
        self.closed = False

    def setPosition(self, servos, duration=1000, wait=False):
        self.commands.append((servos, duration, wait))

    def getPosition(self, servo_id):
        return 500

    def getBatteryVoltage(self):
        return 7.5

    def servoOff(self, servos):
        self.commands.append(("off", servos))

    def close(self):
        self.closed = True


def test_centre_target():
    fake = FakeController()
    arm = ArmController(controller=fake)

    assert arm._calculate_angles(400, 300) == (500, 500)


def test_out_of_range_position():
    fake = FakeController()
    arm = ArmController(controller=fake)

    with pytest.raises(ValueError):
        arm.move_servo(1, 1200, 500)


def test_invalid_servo_id():
    fake = FakeController()
    arm = ArmController(controller=fake)

    with pytest.raises(ValueError):
        arm.move_servo(7, 500, 500)


def test_multiple_servo_movement():
    fake = FakeController()
    arm = ArmController(controller=fake)

    arm.move_servos([(1, 500), (2, 600)], 1000)

    assert len(fake.commands) == 1
    assert fake.commands[0][1] == 1000


def test_battery_voltage():
    fake = FakeController()
    arm = ArmController(controller=fake)

    assert arm.get_battery_voltage() == 7.5


def test_close_twice():
    fake = FakeController()
    arm = ArmController(controller=fake)

    arm.close()
    arm.close()

    assert fake.closed is True


def test_command_after_close():
    fake = FakeController()
    arm = ArmController(controller=fake)

    arm.close()

    with pytest.raises(RuntimeError):
        arm.move_servo(1, 500, 500)


def test_context_manager():
    fake = FakeController()

    with ArmController(controller=fake) as arm:
        assert arm is not None

    assert fake.closed is True

