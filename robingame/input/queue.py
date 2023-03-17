from collections import deque

from robingame.utils import count_edges


class Empty(tuple):
    """Mock tuple of 0/1s that always returns a 0 no matter the index. This is used to
    spoof an empty pygame.key.get_pressed() tuple."""

    def __getitem__(self, *args, **kwargs) -> int:
        return 0


class InputQueue(deque):
    """
    Provides additional functionality beyond pygame.key.get_pressed().
    - Maintains a buffer of the last few inputs
    - Calculates which keys have been pressed and released this tick
               Buttons:
    Index  |   A   B    |   Notes
    -------|----------- |------------------
    0      |   0   0    |
    1      |   1   0    |   A key is pressed
    2      |   1   1    |   B key is pressed
    3      |   1   0    |   B key is released
    4      |   0   0    |   A key is released
    """

    def __init__(self, maxlen=5):
        super().__init__(maxlen=maxlen)

    def get_new_values(self) -> tuple[int]:
        """Subclasses should implement this. It should be something like pygame.key.get_pressed()"""
        raise NotImplementedError

    def update(self):
        self.append(self.get_new_values())

    def _get_values_for_iteration(self, iteration: int) -> tuple[int]:
        """This prevents IndexErrors on the first few iterations of the game when there's nothing
        in the queue yet."""
        try:
            return self[iteration]
        except IndexError:
            return Empty()

    @property
    def current(self) -> tuple[int]:
        """Get the state of all the buttons in the current iteration"""
        return self._get_values_for_iteration(-1)

    @property
    def previous(self) -> tuple[int]:
        """Get the state of all the buttons one iteration ago"""
        return self._get_values_for_iteration(-2)

    def is_down(self, key: int) -> int:
        """Return 1 if a key is currently held down; 0 if not"""
        return self.current[key]

    def is_pressed(self, key: int) -> int:
        """Return 1 if a key has been pressed this tick; 0 if not"""
        return int(self.current[key] and not self.previous[key])

    def is_released(self, key: int) -> int:
        """Return 1 if a key has been released this tick; 0 if not"""
        return int(self.previous[key] and not self.current[key])

    def buffered_inputs(self, key: int, buffer_length: int) -> tuple[int, int]:
        """Count the rising and falling edges. Can be used to detect past inputs."""
        buffer = list(self)[-buffer_length:]
        values = [layer[key] for layer in buffer]
        return count_edges(values)

    def buffered_presses(self, key: int, buffer_length: int) -> int:
        """Return the number of times the key has been pressed in the last few iterations"""
        rising, falling = self.buffered_inputs(key, buffer_length)
        return rising

    def buffered_releases(self, key: int, buffer_length: int) -> int:
        """Return the number of times the key has been released in the last few iterations"""
        rising, falling = self.buffered_inputs(key, buffer_length)
        return falling
