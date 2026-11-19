import rclpy

from rclpy.node import Node
from geometry_msgs.msg import Point

from xarm_toolkit import (
    MockClickTarget,
    TargetSelectionCancelled,
)


class ClickPublisher(Node):

    def __init__(self):
        super().__init__("click_publisher")

        self.declare_parameter("topic", "target_xy")
        topic = self.get_parameter("topic").value

        self.publisher = self.create_publisher(
            Point,
            topic,
            10
        )

        # Create the click source once so its window can remain open.
        self.target_source = MockClickTarget()

        self.get_logger().info(
            f"Publishing target coordinates on {topic}"
        )

    def publish_clicks(self):
        try:
            while rclpy.ok():
                x, y = self.target_source.get_target()

                msg = Point()
                msg.x = float(x)
                msg.y = float(y)
                msg.z = 0.0

                self.publisher.publish(msg)

                self.get_logger().info(
                    f"Published target: x={x}, y={y}"
                )

        except TargetSelectionCancelled:
            self.get_logger().info(
                "Target selection ended."
            )

        finally:
            self.target_source.close()


def main(args=None):
    rclpy.init(args=args)

    node = ClickPublisher()

    try:
        node.publish_clicks()
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()

