from abc import ABC

from pygame.joystick import Joystick

from robingame.input.gamecube import linear_map

NormalisedValue = float  # between 0 (no input) and 1 (maximum input)


class Channel(ABC):
    """
    Reads the input of one button / axis / hat from a parent controller instance
    """

    device: "Device"
    zero_value: float
    one_value: float

    def __init__(self, id: int, zero_value=0.0, one_value=1.0):
        self.id = id
        self.zero_value = zero_value
        self.one_value = one_value

    def _raw_value(self) -> float:
        raise NotImplementedError

    def get_value(self) -> NormalisedValue:
        return linear_map(
            input_value=self._raw_value(),
            input_range=(self.zero_value, self.one_value),
            output_range=(0, 1),
            limit_output=True,
        )

    @property
    def joystick(self) -> Joystick:
        return self.device.joystick


class Button(Channel):
    def _raw_value(self) -> float:
        return self.joystick.get_button(self.id)


class Axis(Channel):
    def _raw_value(self) -> float:
        return self.joystick.get_axis(self.id)


class Hat(Channel):
    axis: int  # e.g. 0 for horizontal rocking, 1 for vertical rocking

    def __init__(self, id: int, axis: int, zero_value=0.0, one_value=1.0):
        super().__init__(id, zero_value, one_value)
        self.axis = axis

    def _raw_value(self) -> float:
        return self.joystick.get_hat(self.id)[self.axis]


class Device:
    """
    Driver that maps the raw inputs of the joystick to 0-1 values that we can use in games.
    Maps axes + hats to meaningful inputs like "left", "right", etc.
    """

    """
    Basically a driver for a specific input device (e.g. the keyboard, a GameCube controller,
    a Logitech joystick)

    Reads the state of each input channel (button / axis) on the device. This state is often
    represented by a float with device-specific range. To allow games to be written in a
    controller-independent way, we normalise the value of each channel be between 0 (no input) to
    1 (max input).
    """

    channels: list[Channel]
    joystick: Joystick

    def __init__(self, joystick: Joystick):
        self.joystick = joystick
        self.joystick.init()

        # bind all buttons / axes / hats to self
        channels = [chan for chan in self.__dict__.values() if isinstance(chan, Channel)]
        for channel in channels:
            channel.controller = self
        self.channels = channels

    def get_values(self) -> tuple[NormalisedValue]:
        """
        Read the state of all the device's channels and output them as a tuple of floats ranging
        from 0 to 1.
        """
        return tuple(chan.get_value() for chan in self.channels)
