
import pygame
import pytest

from xarm_toolkit import MockClickTarget
from xarm_toolkit import TargetSelectionCancelled


@pytest.fixture
def target():
    mock = MockClickTarget()

    yield mock

    mock.close()


def test_mouse_click_returns_float_coordinates(target):
    pygame.event.post(
        pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {"pos": (400, 300), "button": 1}
        )
    )

    result = target.get_target()

    assert result == (400.0, 300.0)
    assert isinstance(result[0], float)
    assert isinstance(result[1], float)


def test_quit_event_cancels_selection(target):
    pygame.event.post(
        pygame.event.Event(pygame.QUIT)
    )

    with pytest.raises(TargetSelectionCancelled):
        target.get_target()


def test_escape_cancels_selection(target):
    pygame.event.post(
        pygame.event.Event(
            pygame.KEYDOWN,
            {"key": pygame.K_ESCAPE}
        )
    )

    with pytest.raises(TargetSelectionCancelled):
        target.get_target()

