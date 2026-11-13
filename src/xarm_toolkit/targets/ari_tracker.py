
"""Placeholder for the future ARI person tracker."""

from .target_source import TargetSource


class ARIPersonTracker(TargetSource):
    """Future target source for ARI tracking data."""

    def __init__(self, topic="/ari/tracking"):
        self._topic = topic

    def get_target(self) -> tuple[float, float]:
        """Receive and return a tracked person's coordinates."""

        raise NotImplementedError(
            "ARI tracking will be implemented in Session 15."
        )

