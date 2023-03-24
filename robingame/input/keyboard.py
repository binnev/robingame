import pygame

from robingame.input.base import InputGroup, InputChannel
from robingame.input.queue import InputQueue


class KeyboardInputQueue(InputQueue):
    def get_new_values(self) -> tuple[int]:
        scancode_wrapper = pygame.key.get_pressed()
        return tuple(scancode_wrapper[ii] for ii in range(len(scancode_wrapper)))


class KeyboardInputGroup(InputGroup):
    ESCAPE = InputChannel(channel_id=pygame.K_ESCAPE)
    SPACE = InputChannel(channel_id=pygame.K_SPACE)
    RETURN = InputChannel(channel_id=pygame.K_RETURN)

    def __init__(self):
        super().__init__(input_queue=KeyboardInputQueue())


if __name__ == "__main__":
    from robingame.objects import Game

    class KeyboardInputGroupTest(Game):
        fps = 60
        window_caption = "KeyboardInputGroup test"

        def __init__(self):
            super().__init__()
            self.keyboard_input = KeyboardInputGroup()

        def read_inputs(self):
            super().read_inputs()
            self.keyboard_input.update()

        def update(self):
            super().update()
            for key_name in "SPACE", "ESCAPE", "RETURN":
                channel = getattr(self.keyboard_input, key_name)
                if channel.is_pressed:
                    print(f"{key_name} pressed")
                if channel.is_released:
                    print(f"{key_name} released")

    KeyboardInputGroupTest().main()
