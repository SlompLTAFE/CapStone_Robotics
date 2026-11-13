"""Pygame mouse-click target source."""

import warnings
import pygame

from .target_source import TargetSource
from .target_source import TargetSelectionCancelled

class MockClickTarget(TargetSource):
    """Provides target coordinates using mouse clicks."""

    def __init__(self, title="xArm Target Selector",
                 window_size=(800, 600)):

        if window_size != (800, 600):
            warnings.warn(
                "Target window should be 800x600 to match "
                "the TargetSource coordinate contract.",
                UserWarning
            )

        self._title = title
        self._size = window_size

        pygame.init()
        self._screen = None
        self._screen = pygame.display.set_mode(self._size)
        pygame.display.set_caption(self._title)

        self._font = None

        try:
            self._font = pygame.font.Font(None, 28)
        except pygame.error:
            pass

    
    def get_target(self) -> tuple[float, float]:
        """Wait for a mouse click and return its coordinates."""

        if self._screen is None:
            raise TargetSelectionCancelled("Window is closed.")

        self._screen.fill((30, 30, 30))

        if self._font:
            hint = self._font.render(
                "Click to select a target. ESC to exit.",
                True,
                (255, 255, 255)
            )
            self._screen.blit(hint, (20, 20))

        pygame.display.flip()

        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.close()
                    raise TargetSelectionCancelled("Window closed.")

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.close()
                        raise TargetSelectionCancelled(
                            "Selection cancelled."
                        )

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    return float(x), float(y)

    def close(self):
        """Close the Pygame window safely."""

        if self._screen is not None:
            pygame.quit()
            self._screen = None


