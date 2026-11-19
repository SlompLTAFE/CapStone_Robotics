"""Demonstrates click-to-arm integration."""

from xarm_toolkit import (
    ArmController,
    MockClickTarget,
    TargetSelectionCancelled,
)


def main():
    """Run the mouse-controlled arm demonstration."""

    targets = MockClickTarget()

    try:
        with ArmController() as arm:
            while True:
                x, y = targets.get_target()

                print(f"Target selected: ({x}, {y})")

                arm.point_at(x, y)

    except TargetSelectionCancelled:
        print("Target selection ended.")

    except RuntimeError as error:
        print(f"Arm connection failed: {error}")

    finally:
        targets.close()


if __name__ == "__main__":
    main()