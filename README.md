# xarm_toolkit

A Python toolkit for controlling a Hiwonder xArm robotic arm using interchangeable target sources.

The project separates arm control from target selection. This allows the arm controller to work independently of the method used to provide target coordinates.

## Features

- **ArmController:** Provides an interface for connecting to and controlling the Hiwonder xArm.
- **Servo control:** Supports individual and multiple-servo movement.
- **Position feedback:** Reads servo positions.
- **Battery monitoring:** Retrieves the arm's battery voltage.
- **Servo release:** Supports releasing servo torque.
- **Context management:** Supports automatic controller cleanup using Python's `with` statement.
- **TargetSource:** Defines an abstract interface for interchangeable target-selection methods.
- **MockClickTarget:** Provides mouse-based target selection using Pygame.
- **ARIPersonTracker:** Included as a package component.

## Project structure

```text
xarm_capstone/
│
|
├── pyproject.toml
├── README.md
│
├── src/
│   └── xarm_toolkit/
│       ├── __init__.py
│       ├── arm_controller.py
│       └── targets/
│           ├── __init__.py
│           ├── target_source.py
│           ├── mock_click.py
│           └── ari_tracker.py
│
├── tests/
│   ├── test_arm_controller.py
│   ├── test_target_source.py
│   ├── test_mock_click.py
│   └── test_ari_tracker.py
│
|
├── demos/
|   ├── demo.py
|   ├── mock_selector_demo.py
|   ├── swap_demo.py
|
|
└── ros2/
    └── xarm_ros2_node/
        ├── package.xml
        ├── setup.py
        ├── setup.cfg
        ├── resource/
        |   ├── xarm_ros2_node
        ├── test/
        |   ├── test_copyright.py
        |   ├── test_flake8
        |   ├── test_pep257
        |   
        └── xarm_ros2_node/
            ├── __init__.py
            ├── click_publisher.py
            ├── simulator_node.py
            └── xarm_node.py
```

## Requirements

### Python

The project requires Python 3.10 or later.

The dependencies are defined in `pyproject.toml`:

| Dependency | Purpose |
|---|---|
| `xarm` | Hiwonder xArm control library |
| `hidapi` | Hardware communication dependency |
| `pygame` | Mouse-based target selection |
| `pytest` | Automated testing |

Pygame and pytest are optional dependency groups, allowing them to be installed when needed.

### ROS 2 simulation

The ROS 2 demonstration was developed and tested using:

- Ubuntu 24.04 LTS
- ROS 2 Jazzy
- ROS 2 Desktop installation
- RViz2
- Python 3.12
- Colcon build tools
- The Hiwonder xArm 1S ROS 2 simulation repository

**Recommended environment:** Ubuntu 24.04 with ROS 2 Jazzy Desktop.

Useful installation resources:

- [Ubuntu Desktop](https://ubuntu.com/download/desktop)
- [ROS 2 Jazzy installation guide](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html)
- [ROS 2 Jazzy documentation](https://docs.ros.org/en/jazzy/index.html)
- [Colcon documentation](https://colcon.readthedocs.io/en/released/)

The ROS 2 Desktop installation includes RViz2 and the graphical tools required for the simulation demonstration.

## Installation

### 1. Obtain the project

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd xarm_capstone
```

Replace the placeholder with the actual GitHub repository URL.

### 2. Install the Python package

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows, activate it with:

```powershell
.venv\Scripts\activate
```

Install the package in editable mode, including the optional Pygame and development dependencies:

```bash
pip install -e ".[mock,dev]"
```

Editable installation allows changes made to the source files to be used without reinstalling the package.

### 3. Install ROS 2

For the ROS 2 demonstration, install ROS 2 Jazzy on Ubuntu 24.04 by following the official installation instructions:

[ROS 2 Jazzy - Ubuntu installation](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html)

Choose the Desktop installation so that RViz2 and the graphical ROS tools are available.

After installation, source the ROS 2 environment:

```bash
source /opt/ros/jazzy/setup.bash
```

It is recommended to add this command to the user's `~/.bashrc` file if ROS 2 will be used regularly.

Install the additional development tools:

```bash
sudo apt update
sudo apt install python3-colcon-common-extensions python3-rosdep
```

For additional guidance, refer to the [official ROS 2 colcon tutorial](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html).

### 4. Install the external Hiwonder xArm simulation

The RViz demonstration uses an external ROS 2 simulation repository:

**[Hiwonder xArm 1S ROS 2 - KaburaJ](https://github.com/KaburaJ/hiwonder_xArm_1s)**

This repository provides the robot description, URDF model, RViz configuration and ROS 2 launch files.

The two packages required for the basic demonstration are:

- `learm_ros2_description`
- `learm_ros2`

The `learm_ros2_moveit_config` package is not required for the click-to-RViz demonstration.

Clone the upstream repository into a separate ROS 2 workspace:

```bash
mkdir -p ~/xarm_sim_ws/src
cd ~/xarm_sim_ws/src

git clone https://github.com/KaburaJ/hiwonder_xArm_1s.git
```

Install the ROS dependencies using the instructions provided by the upstream repository. ROS dependencies can also be managed using the official [rosdep documentation](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Rosdep.html).

Build the required simulator packages:

```bash
source /opt/ros/jazzy/setup.bash

cd ~/xarm_sim_ws

colcon build --symlink-install \
  --packages-select learm_ros2_description learm_ros2
```

Source the resulting workspace:

```bash
source ~/xarm_sim_ws/install/setup.bash
```

The upstream repository contains its own launch files and RViz configurations. Refer to its documentation for the simulator setup and launch procedure.

**Note:** The external simulator is a separate third-party project. Its source code is not included in this repository and should be obtained from the original GitHub repository.

### 5. Prepare the ROS 2 demonstration package

The project's ROS 2 integration is located in:

```text
ros2_demo/src/xarm_ros2_node/
```

The package contains three ROS 2 executables:

| Executable | Purpose |
|---|---|
| `click_publisher` | Receives mouse selections and publishes target coordinates. |
| `simulator_node` | Converts target coordinates into simulated joint positions. |
| `xarm_node` | Receives target coordinates and passes them to the arm controller when hardware mode is enabled. |

The ROS 2 package requires the ROS 2 Python libraries and message packages declared in its `package.xml`.

**Python environment compatibility:** ROS 2 Jazzy uses Python 3.12 on Ubuntu 24.04. When using a virtual environment for the ROS 2 demonstration, it must be able to access the installed ROS 2 Python packages. A virtual environment created with `--system-site-packages` is one way to achieve this.

For example:

```bash
python3 -m venv --system-site-packages ~/ros2_venv
source ~/ros2_venv/bin/activate

source /opt/ros/jazzy/setup.bash
```

Install the project package and its Pygame dependency into the environment:

```bash
cd ~/xarm_capstone
pip install -e ".[mock]"
```

Build the ROS 2 package:

```bash
cd ~/xarm_capstone/ros2_demo

colcon build --symlink-install
```

Source the built package:

```bash
source install/setup.bash
```

Check the available executables:

```bash
ros2 pkg executables xarm_ros2_node
```

The expected executables are:

```text
xarm_ros2_node click_publisher
xarm_ros2_node simulator_node
xarm_ros2_node xarm_node
```

## Package architecture

The toolkit is organised around two main responsibilities.

### 1. ArmController

`ArmController` handles communication with the physical xArm and provides a higher-level interface for controlling its servos.

The controller uses the xArm Python library and connects through USB.

Its implemented responsibilities include:

- Establishing the controller connection.
- Validating servo IDs, positions and movement durations.
- Moving individual servos.
- Moving multiple servos.
- Reading servo positions.
- Retrieving battery voltage.
- Releasing servo torque.
- Closing the connection when finished.

The controller also provides a `point_at()` method, which accepts target coordinates in an 800 × 600 coordinate space and converts them into arm movement commands.

### 2. TargetSource

`TargetSource` is an abstract base class that establishes a common interface for target-selection implementations.

The intention is to separate the source of target coordinates from the hardware-control logic.

A target source can therefore provide coordinates without needing to manage the arm's servo communication directly.

### 3. MockClickTarget

`MockClickTarget` implements mouse-based target selection using Pygame.

It opens a selection window and waits for the user to click a position. The selected coordinates are returned to the calling program.

The selection process can also be cancelled by pressing Escape or closing the window.

## Usage examples

### Connecting to the arm

The `ArmController` supports Python context-manager usage:

```python
from xarm_toolkit import ArmController

with ArmController() as arm:
    arm.point_at(400, 300)
```

The context manager handles controller cleanup when execution leaves the `with` block.

This example requires a connected and compatible physical xArm.

### Selecting a target using the mouse

The mouse-based target source can be used independently of the arm controller:

```python
from xarm_toolkit import MockClickTarget

targets = MockClickTarget()

try:
    x, y = targets.get_target()
    print(f"Selected target: ({x}, {y})")

finally:
    targets.close()
```

This returns the selected coordinates for use by another part of the application.

### Combining target selection and arm control

The two components can be combined so that the selected coordinates are passed to the arm controller:

```python
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
        print("Target selection cancelled.")

    finally:
        targets.close()


if __name__ == "__main__":
    main()
```

This demonstrates the separation between target selection and arm control: the target source supplies coordinates, while the controller handles the arm movement.

## ROS 2 simulation demonstration

A separate ROS 2 demonstration was developed to show the target-selection workflow interacting with an xArm model in RViz.

The demonstration uses the following sequence:

1. `MockClickTarget` opens a Pygame window and waits for a mouse click.
2. The ROS 2 click publisher receives the selected coordinates.
3. The publisher sends the coordinates through the `/target_xy` topic using `geometry_msgs/msg/Point`.
4. A separate simulator node converts the coordinates into simulated joint positions.
5. The simulator publishes the joint positions through `/joint_states` using `sensor_msgs/msg/JointState`.
6. `robot_state_publisher` updates the robot transforms.
7. RViz displays the resulting movement of the simulated xArm.

The simulator maps the 800 × 600 target coordinate space to the simulated shoulder pan and shoulder lift joints. The other joints are held at zero in this demonstration.

### Running the demonstration

After completing the installation steps:

1. Source the ROS 2 Jazzy environment.
2. Source the external simulator workspace.
3. Start the xArm robot model in RViz using the upstream simulator's launch instructions.
4. Source the project's ROS 2 workspace.
5. Start the `simulator_node` executable.
6. Start the `click_publisher` executable.
7. Select positions in the Pygame window and observe the simulated arm respond in RViz.

The nodes communicate through ROS 2 topics, so they must be running in environments that can discover one another.

**Important distinction:** This ROS 2 demonstration is a visual simulation. It does not send physical servo commands to the arm, and its coordinate-to-joint mapping is separate from the physical `ArmController.point_at()` implementation.

The upstream simulator is maintained separately from this project. Its installation and launch files are provided by the original repository:

[https://github.com/KaburaJ/hiwonder_xArm_1s](https://github.com/KaburaJ/hiwonder_xArm_1s)

## Physical hardware integration

The project also includes the `xarm_node` ROS 2 executable, which provides a ROS 2 interface to `ArmController`.

It subscribes to the `/target_xy` topic and can pass received coordinates to the physical arm controller.

The node has a `dry_run` parameter, which defaults to `true`.

In dry-run mode, the node logs received target coordinates without moving the physical arm.

To enable physical movement, the node must be deliberately configured with `dry_run:=false`. This requires a compatible Hiwonder xArm connected through USB and the necessary hardware dependencies and permissions.

**Hardware safety:** Ensure the arm is securely positioned and its movement area is clear before enabling physical movement. The RViz simulation should not be mistaken for a physical hardware test.

## Testing

The project uses pytest for automated testing.

Run the test suite from the project root:

```bash
pytest -v
```

The tests are organised by component:

| Test file | Component |
|---|---|
| `test_arm_controller.py` | Arm controller behaviour |
| `test_target_source.py` | Abstract target-source interface |
| `test_mock_click.py` | Mouse-based target selection |
| `test_ari_tracker.py` | Included component's tests |

The arm-controller tests use test doubles to check controller behaviour without requiring a physical arm for every test.

The ROS 2 package can also be built independently:

```bash
source /opt/ros/jazzy/setup.bash

cd ros2_demo
colcon build --symlink-install
```

## Development

To install the package with its development dependencies:

```bash
pip install -e ".[mock,dev]"
```

To check Python files for syntax errors:

```bash
python -m compileall -q demo.py mock_selector_demo.py swap_demo.py src tests
```

To run the automated tests:

```bash
pytest -v
```

To build the ROS 2 integration package:

```bash
source /opt/ros/jazzy/setup.bash

cd ros2_demo
colcon build --symlink-install
```

## Project limitations

- Physical arm operation requires a compatible Hiwonder xArm connected through USB.
- Mouse-based target selection requires a graphical environment capable of running Pygame.
- The RViz demonstration is a simulation and should not be treated as evidence of physical servo movement.
- The ROS 2 simulator integration is included in this repository, but the third-party Hiwonder simulation model must be obtained separately.
- The simulated coordinate mapping controls the shoulder pan and shoulder lift joints only; it is not a full inverse-kinematics implementation.
- The physical hardware integration and RViz simulation use separate movement implementations.

## License and dependencies

The project uses third-party Python libraries declared in `pyproject.toml`. Their respective licences and distribution terms should be observed when installing or redistributing the project.

The ROS 2 integration package declares its own package metadata and dependencies. The external Hiwonder simulator is distributed separately under the terms of its original repository.

