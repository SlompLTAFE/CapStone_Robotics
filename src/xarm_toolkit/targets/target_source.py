
"""Defines the target source interface."""

from abc import ABC, abstractmethod


class TargetSelectionCancelled(RuntimeError):
    """Raised when a target source is cancelled."""


class TargetSource(ABC):
    """Abstract interface for interchangeable target sources.

    Coordinates use an 800x600 pixel space.
    Origin is top-left.
    X increases right.
    Y increases down.

    get_target() returns a tuple of floats.
    """

    @abstractmethod
    def get_target(self) -> tuple[float, float]:
        """Wait for and return the next target."""
        pass

