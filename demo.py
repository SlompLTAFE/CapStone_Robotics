"""Demonstrates click-to-arm integration."""

from xarm_toolkit import (
    ArmController,
    MockClickTarget,
    TargetSelectionCancelled
)


def main():
    """Run the mouse-controlled arm demonstration."""

    try:
        with ArmController() as arm:
            targets = MockClickTarget()

            try:
                while True:
                    x, y = targets.get_target()

                    print(f"Target selected: ({x}, {y})")

                    arm.point_at(x, y)
            finally:
                    targets.close()

            except TargetSelectionCancelled:
                print("Target selection ended.")

    except RuntimeError as error:
        print(f"Arm connection failed: {error}")


if __name__ == "__main__":
    main()

