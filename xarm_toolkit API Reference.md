xarm_toolkit API Reference 

1. Overview 

The xarm_toolkit package provides a Python interface for controlling a Hiwonder xArm robotic arm and obtaining target coordinates from interchangeable input sources. 

The package separates arm control from target selection through the ArmController class and the abstract TargetSource interface. 

This document describes the public classes and methods available in the toolkit. 

 

2. ArmController 

Module: xarm_toolkit.arm_controller 

The ArmController class provides a simplified interface for communicating with the Hiwonder xArm controller. 

It handles controller connection, servo movement, position reading, battery voltage checks and connection cleanup. 

Constants 

Constant 

Value 

Description 

MIN_POSITION 

0 

Minimum servo position 

MAX_POSITION 

1000 

Maximum servo position 

MIN_SERVO_ID 

1 

First valid servo ID 

MAX_SERVO_ID 

6 

Last valid servo ID 

CENTRE_POSITION 

500 

Initial centre position for coordinate mapping 

POSITION_RANGE 

250 

Maximum offset from the centre position 

Constructor 

ArmController(controller=None) 

Initialises the arm controller. 

Parameters: 

controller (optional): An existing controller object. If omitted, the class attempts to establish a USB connection using xarm.Controller("USB"). 

Raises: 

RuntimeError: If the USB connection fails or no controller is provided. 

Example: 

from xarm_toolkit import ArmController 
 
arm = ArmController() 

An existing controller can also be injected: 

arm = ArmController(controller=my_controller) 

move_servo() 

move_servo(servo_id, position, duration_ms) 

Moves one servo to the requested position. 

Parameters: 

servo_id (int): Servo identifier, between 1 and 6. 

position (int): Target position, between 0 and 1000. 

duration_ms (int): Movement duration in milliseconds. 

Raises: 

ValueError: If the servo ID, position or duration is invalid. 

RuntimeError: If the controller has been closed. 

Example: 

arm.move_servo(1, 500, 500) 

move_servos() 

move_servos(moves, duration_ms) 

Moves multiple servos in the same movement command. 

Parameters: 

moves (iterable): Collection of (servo_id, position) pairs. 

duration_ms (int): Movement duration in milliseconds. 

Raises: 

ValueError: If a servo ID or position is invalid, the duration is not a positive integer, or no movements are supplied. 

RuntimeError: If the controller has been closed. 

Example: 

arm.move_servos( 
    [(1, 500), (2, 650)], 
    duration_ms=500 
) 

read_servo_positions() 

read_servo_positions(servo_ids) 

Reads the current positions of the requested servos. 

Parameters: 

servo_ids (iterable): Collection of servo IDs to read. 

Returns: 

A dictionary containing servo IDs as keys and their reported positions as values. 

Raises: 

ValueError: If a servo ID is invalid. 

RuntimeError: If the controller has been closed. 

Example: 

positions = arm.read_servo_positions([1, 2]) 
 
print(positions) 

get_battery_voltage() 

get_battery_voltage() 

Retrieves the controller's reported battery voltage. 

Returns: 

The voltage value returned by the underlying xArm controller library. 

Raises: 

RuntimeError: If the controller has been closed. 

Example: 

voltage = arm.get_battery_voltage() 
 
print(f"Battery voltage: {voltage} V") 

unload_servos() 

unload_servos(servo_ids) 

Releases the torque of the specified servos. 

Parameters: 

servo_ids (iterable): Collection of servo IDs to release. 

Raises: 

ValueError: If a servo ID is invalid. 

RuntimeError: If the controller has been closed. 

Example: 

arm.unload_servos([1, 2]) 

point_at() 

point_at(x, y, duration_ms=500) 

Converts a target coordinate into pan and tilt servo positions and commands the arm to move. 

Coordinates use an 800 × 600 pixel space, with the origin at the top-left corner. 

Parameters: 

x (int or float): Horizontal target coordinate, between 0 and 800. 

y (int or float): Vertical target coordinate, between 0 and 600. 

duration_ms (int): Movement duration in milliseconds. Defaults to 500. 

The method maps the coordinates to servo IDs 1 and 2 using the initial coordinate mapping. 

Raises: 

ValueError: If the coordinates are not numeric or fall outside the permitted coordinate space. 

ValueError: If the movement duration is invalid. 

RuntimeError: If the controller has been closed. 

Example: 

arm.point_at(400, 300) 

close() 

close() 

Closes the controller connection if it has not already been closed. 

Subsequent movement and controller operations are prevented. 

Example: 

arm.close() 

Context Manager Support 

ArmController supports Python's context manager protocol. This allows the connection to be closed automatically when the with block finishes. 

Example: 

with ArmController() as arm: 
    arm.point_at(400, 300) 

 

3. TargetSource 

Module: xarm_toolkit.targets.target_source 

TargetSource is an abstract base class that defines the common interface for target-selection implementations. 

It allows different input methods to provide coordinates using the same method. 

Coordinate Convention 

Target coordinates use the following convention: 

Coordinate space: 800 × 600 pixels. 

Origin: Top-left corner. 

X-axis: Increases towards the right. 

Y-axis: Increases downwards. 

get_target() 

get_target() -> tuple[float, float] 

An abstract method that must be implemented by subclasses. 

It waits for a target selection and returns its coordinates. 

Returns: 

A tuple containing the X and Y coordinates as floating-point values. 

Example implementation: 

class CustomTargetSource(TargetSource): 
 
    def get_target(self): 
        return 400.0, 300.0 

 

4. TargetSelectionCancelled 

Module: xarm_toolkit.targets.target_source 

TargetSelectionCancelled is a custom exception raised when target selection is cancelled. 

It inherits from Python's RuntimeError. 

It allows applications to distinguish a cancelled target-selection operation from ordinary application errors. 

Example: 

from xarm_toolkit import TargetSelectionCancelled 
 
try: 
    x, y = targets.get_target() 
 
except TargetSelectionCancelled: 
    print("Target selection was cancelled.") 

 

5. MockClickTarget 

Module: xarm_toolkit.targets.mock_click 

MockClickTarget implements the TargetSource interface using Pygame. 

It creates a graphical window where the user can select a target using the mouse. 

Constructor 

MockClickTarget(title="xArm Target Selector", window_size=(800, 600)) 

Initialises the Pygame target-selection window. 

Parameters: 

title (str): Window title. Defaults to "xArm Target Selector". 

window_size (tuple): Window dimensions. Defaults to (800, 600). 

If a different window size is supplied, a warning is issued because the standard target coordinate convention uses an 800 × 600 space. 

Example: 

from xarm_toolkit import MockClickTarget 
 
targets = MockClickTarget() 

get_target() 

get_target() -> tuple[float, float] 

Waits for the user to click inside the Pygame window. 

Returns: 

A tuple containing the selected X and Y coordinates as floating-point values. 

Behaviour: 

A mouse click returns the selected coordinates. 

Pressing Escape cancels target selection. 

Closing the window cancels target selection. 

Raises: 

TargetSelectionCancelled: If the window is closed or the user presses Escape. 

Example: 

x, y = targets.get_target() 
 
print(f"Selected target: ({x}, {y})") 

close() 

close() 

Closes the Pygame window and shuts down Pygame. 

Example: 

targets.close() 

 

6. Complete Usage Example 

The following example demonstrates how MockClickTarget and ArmController can be used together. 

from xarm_toolkit import ( 
    ArmController, 
    MockClickTarget, 
    TargetSelectionCancelled, 
) 
 
 
def main(): 
 
    targets = MockClickTarget() 
 
    try: 
        with ArmController() as arm: 
 
            while True: 
                x, y = targets.get_target() 
 
                print(f"Target selected: ({x}, {y})") 
 
                arm.point_at(x, y) 
 
    except TargetSelectionCancelled: 
        print("Target selection ended.") 
 
    finally: 
        targets.close() 
 
 
if __name__ == "__main__": 
    main() 

This example creates a mouse-based target selector, waits for the user to select coordinates, and passes those coordinates to the arm controller. The arm connection is automatically closed when the context manager exits. 

 

7. Dependencies 

The toolkit relies on the following Python packages: 

Dependency 

Purpose 

xarm 

Communication with the Hiwonder xArm controller 

hidapi 

USB/HID communication support 

pygame 

Graphical mouse-based target selection 

The project also uses Python's built-in abc module to define the abstract target-source interface. 

 