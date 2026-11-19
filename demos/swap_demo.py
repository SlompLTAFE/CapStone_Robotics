
import argparse
from xarm_toolkit import ArmController
from xarm_toolkit import TargetSelectionCancelled
from xarm_toolkit import MockClickTarget
from xarm_toolkit import ARIPersonTracker



def run(source):
    """Run the arm using any object that implements TargetSource."""
    arm = None

    try:
        while True:
            x, y = source.get_target()

            # Connect only after receiving a valid target.
            if arm is None:
                arm = ArmController()

            arm.point_at(x, y)

    except TargetSelectionCancelled:
        print("Target selection ended.")

    finally:
        if arm is not None:
            arm.close()



def main():
    parser = argparse.ArgumentParser(
        description="Run the xArm with a selectable target source."
    )

    parser.add_argument(
        "source",
        choices=["mock", "ari"],
        help="Select the target source."
    )

    args = parser.parse_args()

    if args.source == "mock":
        source = MockClickTarget()
    else:
        source = ARIPersonTracker(
            topic="/UNRESOLVED_ari_person_topic"
        )

    try:
        run(source)
    finally:
        close_source = getattr(source, "close", None)
        if callable(close_source):
            close_source()


if __name__ == "__main__":
    main()
