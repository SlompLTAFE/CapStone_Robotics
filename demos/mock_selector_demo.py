
from xarm_toolkit import MockClickTarget, TargetSelectionCancelled


def main():
    selector = MockClickTarget()

    try:
        print("Click anywhere in the Pygame window to select a target.")
        print("Press ESC or close the window to exit.")

        while True:
            x, y = selector.get_target()
            print(f"Selected target: x={x}, y={y}")

    except TargetSelectionCancelled:
        print("Target selection cancelled.")

    finally:
        selector.close()


if __name__ == "__main__":
    main()

