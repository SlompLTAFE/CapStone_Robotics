
import logging
import threading
from .target_source import TargetSource, TargetSelectionCancelled
logger = logging.getLogger(__name__)

class ARIPersonTracker(TargetSource):
    """
    Week 15 stub for an ARI-backed TargetSource.

    The tracker will eventually translate ARI's tracking message
    into the shared 800x600 screen coordinate system.

    Mesage fields, coordinate axes, origin and scaling must be
    confirmed during the live ARI investigation before implementing
    _to_target().
    """

    def __init__(
        self,
        topic: str = "/UNRESOLVED_ari_person_topic"
    ):
        self._topic = topic
        self._latest = None
        self._lock = threading.Lock()

        logger.warning(
            "ARIPersonTracker is currently a stub. "
            "No live ARI subscription has been configured."
        )

    def _to_target(self, msg) -> tuple[float, float]:
        """
        Convert an ARI tracking message into canonical 800x600
        coordinates.

        TODO: Complete after investigating the actual ARI message because I don't have the details yet.

        Record here:
        - Message type and position fields
        - Which field maps to screen x and screen y
        - Coordinate origin and axis directions
        - Required scaling and axis inversion
        """
        raise NotImplementedError(
            "ARI message conversion requires live investigation."
        )

    def _on_msg(self, msg) -> None:
        """Store the latest converted target safely."""
        target = self._to_target(msg)

        with self._lock:
            self._latest = target

    def get_target(self) -> tuple[float, float]:
        """Return the latest target or signal that none exists."""
        with self._lock:
            target = self._latest

        if target is None:
            raise TargetSelectionCancelled(
                "No ARI tracking target is currently available."
            )

        return target
