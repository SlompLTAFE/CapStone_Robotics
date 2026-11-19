import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from sensor_msgs.msg import JointState


class SimulatorNode(Node):
    """Convert target coordinates into joint states for the xArm RViz model."""

    def __init__(self):
        super().__init__("xarm_simulator_node")

        self.declare_parameter("target_topic", "target_xy")
        self.declare_parameter("joint_topic", "joint_states")

        target_topic = self.get_parameter("target_topic").value
        joint_topic = self.get_parameter("joint_topic").value

        self.joint_names = [
            "shoulder_pan",
            "shoulder_lift",
            "elbow",
            "wrist_flex",
            "wrist_roll",
            "grip_left",
            "grip_right",
            "tendon_left",
            "tendon_right",
            "finger_left",
            "finger_right",
        ]

        self.publisher = self.create_publisher(
            JointState, joint_topic, 10
        )

        self.subscription = self.create_subscription(
            Point,
            target_topic,
            self.target_callback,
            10,
        )

        self.get_logger().info(
            f"Simulator listening on /{target_topic}"
        )

    def target_callback(self, msg):
        """Convert an 800x600 target into shoulder joint angles."""

        x = max(0.0, min(800.0, msg.x))
        y = max(0.0, min(600.0, msg.y))

        pan = ((x - 400.0) / 400.0) * 1.57
        lift = ((300.0 - y) / 300.0) * 1.57

        joint_state = JointState()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.name = self.joint_names

        joint_state.position = [
            pan,
            lift,
            0.0,  # elbow
            0.0,  # wrist_flex
            0.0,  # wrist_roll
            0.0,  # grip_left
            0.0,  # grip_right
            0.0,  # tendon_left
            0.0,  # tendon_right
            0.0,  # finger_left
            0.0,  # finger_right
        ]

        self.publisher.publish(joint_state)

        self.get_logger().info(
            f"Target ({x:.1f}, {y:.1f}) -> "
            f"pan={pan:.2f}, lift={lift:.2f}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = SimulatorNode()

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
