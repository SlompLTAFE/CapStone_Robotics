
"""
ARI person-tracking integration for xarm_toolkit.

The ROS 2 message type and coordinate conversion must be configured depending on topic and message types.
Canonical target coordinates:
    - 800 x 600
    - Origin at top-left
    - X increases towards the right
    - Y increases downwards
"""

import logging
import math
import threading
from typing import Optional, Type

from .target_source import TargetSource, TargetSelectionCancelled

logger = logging.getLogger(__name__)


class ARIPersonTracker(TargetSource):
    """
    ROS 2 subscriber that converts ARI tracking messages into
    canonical 800x600 screen coordinates.
    """

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    def __init__(
        self,
        topic: str = "/UNRESOLVED_ari_person_topic",
        message_type: Optional[Type] = None,
    ):
        self._topic = topic
        self._message_type = message_type

        self._latest: Optional[tuple[float, float]] = None
        self._lock = threading.Lock()

        self._node = None
        self._executor = None
        self._subscription = None
        self._spin_thread = None
        self._owns_ros_context = False
        self._closed = False

        if message_type is None:
            logger.warning(
                "ARI tracker is not connected. "
                "The actual message type has not been configured."
            )
            return

        self._start_subscription()

    def _start_subscription(self) -> None:
        """
        Initialise ROS 2 and subscribe to the configured ARI topic.

        ROS imports are kept inside this method so that the main
        toolkit can still be imported without ROS 2 installed.
        """
        try:
            import rclpy
            from rclpy.executors import SingleThreadedExecutor

            if not rclpy.ok():
                rclpy.init()
                self._owns_ros_context = True

            self._node = rclpy.create_node("ari_person_tracker")

            self._subscription = self._node.create_subscription(
                self._message_type,
                self._topic,
                self._on_msg,
                10,
            )

            self._executor = SingleThreadedExecutor()
            self._executor.add_node(self._node)

            self._spin_thread = threading.Thread(
                target=self._executor.spin,
                name="ari-tracker-executor",
                daemon=True,
            )
            self._spin_thread.start()

            logger.info(
                "ARI tracker subscribed to topic: %s",
                self._topic,
            )

        except Exception as error:
            self.close()
            raise RuntimeError(
                f"Unable to initialise ARI subscription on {self._topic}"
            ) from error

    def _to_target(self, msg) -> tuple[float, float]:
        """
        Convert an ARI tracking message into canonical 800x600
        screen coordinates.

        Change this method when ARI message type and published fields are confirmed.
        
        PLEASE NOTE: Topics and message types change, both physical and simulated versions will have different message types and fields. The following must be confirmed before implementing this method,
        Due to this, i have constructed a function that fails gracefully and can be configured once the ARI message type and fields are known. My apolagies for the github activity here, had the template
        on the clip board and ended up making a few mistakes on upload. 

        1. Actual ROS message type.
        2. Position field names and nesting.
        3. Coordinate origin and axis directions.
        4. Coordinate units and valid ranges.
        5. Required scaling and axis inversion.

        
        """
        raise NotImplementedError(
            "ARI coordinate conversion has not been configured."
        )

        # ---------------------------------------------------------
        # COORDINATE CONVERSION
        # Convert source_x and source_y into:
        # x: 0 to SCREEN_WIDTH
        # y: 0 to SCREEN_HEIGHT
        #
        # Account for coordinate origin, axis direction and scaling.
        # ---------------------------------------------------------

        # x = ...
        # y = ...

        # ---------------------------------------------------------
        # VALIDATE FINAL COORDINATES
        # ---------------------------------------------------------

        # if not math.isfinite(x) or not math.isfinite(y):
        #     raise ValueError("ARI returned non-finite coordinates.")
        #
        # if not (0 <= x <= self.SCREEN_WIDTH):
        #     raise ValueError("ARI x coordinate is outside the screen.")
        #
        # if not (0 <= y <= self.SCREEN_HEIGHT):
        #     raise ValueError("ARI y coordinate is outside the screen.")
        #
        # return float(x), float(y)

    def _on_msg(self, msg) -> None:
        """
        Handle incoming ARI messages.

        Convert the message and safely store the latest target.
        """
        if self._closed:
            return

        try:
            target = self._to_target(msg)

            with self._lock:
                self._latest = target

        except NotImplementedError:
            logger.error(
                "ARI message received, but coordinate conversion "
                "has not been implemented."
            )

            with self._lock:
                self._latest = None

        except (AttributeError, TypeError, ValueError) as error:
            logger.warning(
                "Unable to convert ARI tracking message: %s",
                error,
            )

            with self._lock:
                self._latest = None

    def get_target(self) -> tuple[float, float]:
        """
        Return the latest converted ARI target.

        Raises:
            TargetSelectionCancelled: If no valid target is available.
        """
        if self._closed:
            raise TargetSelectionCancelled(
                "ARI tracker has been closed."
            )

        with self._lock:
            target = self._latest

        if target is None:
            raise TargetSelectionCancelled(
                "No valid ARI tracking target is currently available."
            )

        return target

    def close(self) -> None:
        """Stop the ROS 2 subscriber and release owned resources."""
        if self._closed:
            return

        self._closed = True

        if self._executor is not None:
            self._executor.shutdown()

        if self._node is not None:
            self._node.destroy_node()

        if self._owns_ros_context:
            import rclpy

            if rclpy.ok():
                rclpy.shutdown()

        if (
            self._spin_thread is not None
            and self._spin_thread.is_alive()
        ):
            self._spin_thread.join(timeout=2.0)

        self._subscription = None
        self._executor = None
        self._node = None
        self._spin_thread = None

        logger.info("ARI tracker closed.")
