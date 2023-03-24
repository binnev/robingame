from robingame.input.device import NormalisedValue
from robingame.input.queue import InputQueue


class InputChannel:
    """
    Represents a single input channel on a device -- e.g. a button or analog input.
    Can be used standalone to provide shortcuts for a particular input:
        ```
        input_queue = InputQueue(...)
        a_button = InputChannel(channel_id=A_BUTTON_ID, input_queue=input_queue)
        ...
        if a_button.is_pressed:
            ...  # do stuff
        ```

    Can also be declared on an InputGroup subclass to map inputs:
        ```
        class KeyboardWASD(InputGroup):
            UP = InputChannel(pygame.K_w)
            LEFT = InputChannel(pygame.K_a)
            DOWN = InputChannel(pygame.K_s)
            RIGHT = InputChannel(pygame.K_d)

        player1 = KeybboardWASD()
        if player1.RIGHT.is_pressed:
            ...  # move right
        ```
    """

    def __init__(self, channel_id: int, input_queue: InputQueue = None):
        """
        Class to describe a single input channel on a joystick/controller -- e.g. the "A" button
        on a gamecube controller. Implements methods which check with the parent input device
        whether this button is pressed, released, etc. This allows for the more pleasant shorthand:
        `controller.a_button.is_pressed` instead of `controller.is_pressed(controller.a_button)`

        :param int channel_id: index of this input channel in the input_queue.get_new_values() tuple
        :param InputQueue input_queue: The input queue to which this instance listens
        """
        self.channel_id = channel_id
        self.input_queue = input_queue

    @property
    def is_down(self):
        return self.input_queue.is_down(self.channel_id)

    @property
    def is_pressed(self):
        return self.input_queue.is_pressed(self.channel_id)

    @property
    def is_released(self):
        return self.input_queue.is_released(self.channel_id)

    @property
    def value(self):
        """Does the same thing as is_down but makes some parts of the code more readable,
        especially for analog inputs that can be between 0-1."""
        return self.is_down

    def buffered_presses(self, buffer_length: int):
        return self.input_queue.buffered_presses(self.channel_id, buffer_length)

    def buffered_releases(self, buffer_length: int):
        return self.input_queue.buffered_releases(self.channel_id, buffer_length)

    def __sub__(self, other: "InputChannel|NormalisedValue"):
        return self.value - (other.value if isinstance(other, InputChannel) else other)

    def __add__(self, other: "InputChannel|NormalisedValue"):
        return self.value + (other.value if isinstance(other, InputChannel) else other)

    def __bool__(self):
        """This allows us to do `if input.UP` instead of `if input.UP.is_down`"""
        return bool(self.value)


class AxisInput(InputChannel):
    smash_threshold = 0.9
    smash_window = 3  # frames in which to reach smash_threshold

    @property
    def is_smashed(self) -> bool:
        history = list(self.parent)[-1 - self.smash_window :]
        history = [inputs[self.id] for inputs in history]
        if history:
            return history[-1] >= self.smash_threshold and history[0] <= 0.1
        else:
            return False


class InputGroup:
    """
    Maps controller-specific channels (e.g. the "A" button on a gamecube controller or the "B"
    key on the keyboard) to game-specific channels (e.g. "left" or "jump")

    Provides syntactic sugar to easily access the state of each input channel, e.g:
        input_group.A_BUTTON.is_released()
    """

    def __init__(self, input_queue: InputQueue):
        self.input_queue = input_queue

        # for each InputChannel declared on this class, create a new InputChannel
        # instance with access to self.input_queue
        input_channels = {
            name: attr
            for _class in self.__class__.__mro__
            for name, attr in _class.__dict__.items()
            if issubclass(_class, InputGroup) and isinstance(attr, InputChannel)
        }
        for name, attr in input_channels.items():
            attr.input_queue = self.input_queue

    def update(self):
        self.input_queue.update()
