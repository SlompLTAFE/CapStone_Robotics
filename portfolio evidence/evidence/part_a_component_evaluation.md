# Part A – Component Evaluation
**Project:** xarm_toolkit – xArm Integration Capstone  
**By:** Lucas Slomp : 20069199 
**Date:** 12 November 2026
**PLEASE NOTE**: AI assistance was used during the preparation of this component evaluation to help organise information, improve document structure, and refine presentation. The content was developed from my own research, draft writing, project work and observations, with AI used as a supporting tool rather than a replacement for my own work.
I have personally reviewed the final document, checked its technical content, and made changes to ensure it accurately represents my understanding and the work completed. Responsibility for the submitted content and its accuracy remains my own.

## 1. Project Overview

The purpose of this project is to develop a Python package called `xarm_toolkit` that provides an interface between the Hiwonder xArm robotic arm and interchangeable target sources.
The system is designed around two primary components: an `ArmController`, which manages communication with the xArm, and a `TargetSource` interface, which provides coordinates for the arm to follow.
The project uses a Pygame-based mouse input as a development mock and an ARI person-tracking source as the intended real-world input. ROS 2 provides an integration layer for communication between the target publisher and arm controller.
The selected components were evaluated based on their suitability, maintainability, licensing, complexity and ability to integrate into the proposed system.

## 2. Hardware Component Evaluation

### 2.1 Hiwonder xArm 2.0

The Hiwonder xArm 2.0 was selected as the project's physical robotic platform. It provides multiple servo-controlled joints, allowing the arm to move in response to coordinate-based targeting.

The arm is suitable for this project because it provides a relatively accessible robotic platform with an existing controller interface and documented communication protocol. Its movement capabilities are sufficient for demonstrating our ability to write code and develop packages for aphysical platform.

The arm's multiple joints allow the system to perform basic pan and tilt movements, which are the primary requirements of the pointing demonstration.

**Advantages:**
- Provides a physical platform for demonstrating robotic movement.
- Uses servo-controlled joints that can be addressed individually.
- Has an existing Python control library available.
- Supports HID-based communication through its controller board.

**Limitations:**
- Movement accuracy depends on servo calibration and the coordinate-to-position mapping.
- The arm has physical movement limits that must be respected.
- Communication failures can prevent commands from reaching the hardware.
- The current implementation does not use closed-loop feedback to continuously correct movement.

**Evaluation:**

The xarm is an appropriate choice for this project because it provides sufficient functionality without requiring the development of a complete robotic platform. Its existing controller interface allows development to focus on software integration rather than hardware communication from the beginning.

### 2.2 HID Controller Board

The xArm controller board provides the communication interface between the computer and the arm's servo hardware.
The controller receives commands from the computer through a USB HID connection and translates them into the appropriate instructions for the robotic arm.
HID communication was selected because it provides a direct way to communicate with the controller without requiring a separate network connection or custom hardware interface.
The project uses the existing `xarm` Python package to communicate with this board.

**Advantages:**
- Provides a direct USB communication pathway.
- Allows software to issue movement commands to individual servos.
- Avoids the need to develop a complete USB communication driver.
- Can be accessed through existing Python libraries.

**Limitations:**
- Requires the correct USB device and permissions to be available.
- Communication depends on the controller being connected and recognised.
- Hardware-specific behaviour can complicate testing in virtualised environments.
- Communication failures must be handled appropriately by the application.

**Evaluation:**

The HID controller board is appropriate for the project because it provides a straightforward communication boundary between the Python application and the robotic hardware.
Using an existing library reduces the amount of low-level communication code required and allows the project to concentrate on actual implementation.

### 2.3 LSC Communication Protocol

The xArm uses the LSC protocol to communicate movement instructions to its servo controller.
The protocol investigation established the following structure from the available reference material:

| Protocol element | Description |
|---|---|
| Baud rate | 9600 |
| Header | `55 55` |
| Length | N + 2 |
| Command | `CMD_SERVO_MOVE (0x03)` |
| Checksum | No checksum |
| Servo identifiers | 1–6 |
| Communication | Serial-style command framing |

The protocol allows the controller to receive instructions containing servo identifiers, target positions and movement durations.
Understanding the protocol was important because it established how higher-level movement requests are eventually translated into commands that the controller can understand.
The project separates this responsibility from the rest of the application. The `ArmController` provides methods such as `move_servo()`, `move_servos()` and `point_at()`, rather than requiring other components to construct communication frames themselves.

**Advantages:**
- Provides a relatively simple command structure.
- Allows individual servo movements to be controlled.
- Supports a lightweight implementation without introducing an additional protocol framework.
- Keeps hardware communication separate from target generation and ROS 2 integration.

**Limitations:**
- Commands must follow the correct frame structure.
- Incorrect servo identifiers or positions can result in unexpected behaviour.
- Movement commands do not provide the same reliability guarantees as a fully acknowledged communication protocol.
- The current implementation does not provide continuous feedback-based movement correction.

**Evaluation:**

The LSC protocol is suitable for the project because it provides the necessary functionality to control the arm without requiring a more complicated communication system.
Understanding its structure also makes it possible to investigate and troubleshoot communication problems independently of the higher-level Python application.
The protocol details above are based on the available reference material and Session 13 investigation.

## 3. Software Dependency Evaluation

The following dependencies were selected to support hardware communication, user input, automated testing and package installation.

| Dependency | Version recorded (ROS2 environment) | Licence |                                    |Purpose |
|            |                  |                                                       |
| xarm       | 0.0.4            | MIT (PyPI classifier; repository licence to confirm)  | Provides the Python interface for controlling the xArm. |
| hidapi     | 0.15.0           | Distribution-dependent; verify installed licence      | Provides USB HID communication. |
| pygame     | 2.5.2            | LGPL 2.1 with linking exception (verify distribution) | Provides the graphical mouse-click target source. |
| pytest     | 9.2.0            | MIT                                                   | Runs automated tests without requiring physical hardware. |
| setuptools | 68.1.2           | MIT                                                   | Provides the build backend for installing the Python package. |

*Versions marked with an asterisk require confirmation against the installed project environment before final submission.*

### 3.1 xarm

The `xarm` package was selected because it provides an existing interface for communicating with the Hiwonder xArm controller.
Rather than implementing the complete communication system independently, the project uses the package's `Controller` and `Servo` classes.
This reduces development complexity and allows the project to focus on providing a consistent interface through `ArmController`.
The package is declared as MIT-licensed through its PyPI classifier. However, its licence metadata should be checked against the project's actual repository licence before finalising the licensing record.

### 3.2 hidapi

The `hidapi` package provides access to USB HID devices through Python.
It is required as part of the hardware communication dependency chain and allows the application to communicate with the xArm controller board.
Its inclusion avoids the need to implement low-level USB HID communication independently.
The exact licence must be checked against the installed distribution because HIDAPI has different licensing arrangements depending on the distribution and included components.

### 3.3 pygame

Pygame was selected to provide the development mock for the ARI tracking system.
It creates an 800 × 600 graphical window in which mouse clicks produce coordinate pairs. These coordinates follow the same `TargetSource` contract expected from the future ARI integration.
Pygame is suitable because it provides straightforward mouse-event handling and a simple event loop without requiring a more complex computer vision framework.
It is an optional dependency because the arm controller does not require a graphical interface to operate.

### 3.4 pytest
Pytest was selected as the project's automated testing framework.
It allows the `ArmController`, `TargetSource` and target implementations to be tested independently of the physical xArm.
Dependency injection allows a fake controller to replace the real `xarm.Controller`, making it possible to verify method calls, position validation and controller behaviour without connecting the hardware.
Pytest also supports automated testing of Pygame events through synthetic events.

### 3.5 setuptools
Setuptools is used as the build backend for the project's `pyproject.toml` configuration.
It allows the `xarm_toolkit` package to be installed using:

`pip install -e ".[mock,dev]"`

This provides an editable installation and allows the project to separate its required hardware dependencies from optional development and testing dependencies.

## 4. Dependency Maintenance and Alternatives

The dependencies were selected because they provide established functionality and reduce the need to develop low-level functionality from scratch.

| Dependency | Maintenance consideration |                                                                                    |Alternative considered |
|            |                                                                                              |                                        |
| xarm       | Existing third-party hardware library; repository activity should be checked.                | Direct HID implementation using hidapi. |
| hidapi     | Established HID interface; installed distribution and repository activity should be checked. | Alternative `hid` Python binding or pyusb. |
| pygame     | Established graphical library with mouse and event handling.                                 | tkinter or OpenCV GUI. |
| pytest     | Established Python testing framework.                                                        | Built-in unittest. |
| setuptools | Established Python packaging tool.                                                           | Hatchling or Flit. |

The alternatives were considered based on implementation complexity, compatibility and suitability for the project's requirements.
For example, implementing HID communication directly would provide greater control but would introduce unnecessary development work. Similarly, using OpenCV for the mouse-click mock would introduce functionality that the project does not require.
The selected dependencies provide the necessary functionality while keeping the package relatively small and modular.

## 5. SDK Versus Raw Protocol Decision

An important design decision was whether to use the existing `xarm` Python package or implement communication directly through the HID interface and LSC protocol.
The raw-protocol approach would involve manually constructing communication frames, managing USB HID reports and handling the low-level details of communicating with the controller.
Although this would provide greater control over communication, it would also introduce additional complexity and increase the amount of code requiring testing and maintenance.
The existing `xarm` package provides an abstraction over these lower-level operations. It allows the project to issue movement commands through existing classes and methods.
For this reason, the SDK/library approach was selected.
The project still investigates the underlying protocol because understanding the communication structure is important for troubleshooting and explaining how the system operates.
The chosen approach also supports the project's software architecture. The `ArmController` wraps the third-party controller and exposes a smaller, consistent interface to the rest of the application.
This means that other components do not need to know how HID communication or LSC frame construction works.
If the third-party package becomes unsupported or incompatible with future hardware, the implementation could be replaced with a direct protocol driver while keeping the public `ArmController` interface largely unchanged.

## 6. Design Decision: Coordinate Mapping
The project uses a direct coordinate-to-servo mapping rather than an inverse-kinematics library.
The target source produces coordinates within an 800 × 600 pixel space. These coordinates are normalised around the centre of the window and converted into suitable servo positions.
This approach was chosen because the current project only requires approximate pointing movement rather than precise robotic positioning or complex trajectory planning.
The mapping is isolated inside the private `_calculate_angles()` method within `ArmController`.
This design makes future changes easier because the coordinate conversion can be replaced with a more advanced inverse-kinematics implementation without changing the target-source interface or the rest of the application.
An additional inverse-kinematics dependency would introduce unnecessary complexity for the current requirements.

## 7. Overall Component Evaluation
The selected hardware and software components provide a suitable foundation for the xArm integration project.
The Hiwonder xArm provides the physical movement platform, while its HID controller board provides the communication interface. The LSC protocol defines the underlying command structure, and the existing `xarm` package provides a higher-level interface for controlling the hardware.
The supporting Python dependencies provide the functionality required for target generation, testing and package installation.
The most important architectural decision was to separate hardware control from target generation through the `TargetSource` interface.
This allows the project to use a Pygame mouse-click mock during development and introduce an ARI tracking implementation without requiring changes to the arm-control logic.
Overall, the selected components are appropriate for the project's scope because they reduce unnecessary implementation complexity while maintaining clear boundaries between hardware communication, target generation and application integration.
