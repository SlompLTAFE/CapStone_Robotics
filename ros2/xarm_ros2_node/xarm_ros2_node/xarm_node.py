import rclpy

from rclpy.node import Node
from geometry_msgs.msg import Point


class XArmNode(Node):

    def __init__(self):
        super().__init__("xarm_node")

        self.declare_parameter("topic", "target_xy")
        self.declare_parameter("duration_ms", 500)
        self.declare_parameter("dry_run", True)

        topic = self.get_parameter("topic").value
        self.duration_ms = (
            self.get_parameter("duration_ms").value
        )
        self.dry_run = (
            self.get_parameter("dry_run").value
        )

        self.arm = None

        if not self.dry_run:
            from xarm_toolkit import ArmController
            self.arm = ArmController()

        self.subscription = self.create_subscription(
            Point,
            topic,
            self.target_callback,
            10
        )

        self.get_logger().info(
            f"Listening for targets on {topic}"
        )

        if self.dry_run:
            self.get_logger().warning(
                "DRY RUN enabled: no physical arm will move."
            )

    def target_callback(self, msg):
        x = msg.x
        y = msg.y

        if self.dry_run:
            self.get_logger().info(
                f"Received target: x={x}, y={y}"
            )
        else:
            self.arm.point_at(
                x,
                y,
                duration_ms=self.duration_ms
            )

    def destroy_node(self):
        if self.arm is not None:
            self.arm.close()

        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)

    node = XArmNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()

