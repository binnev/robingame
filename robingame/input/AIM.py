"""
This is how I intend to arrange things

robingame/input
    device  # reading the state of input devices and normalising it
        base
            Channel
                Button
                Axis
                Hat
            Device (same as InputDevice)
        gamecube
            GamecubeControllerMayflashDevice
        keyboard
            KeyboardDevice (really just a pygame.key.get_pressed wrapper)
    queue  # storing state history and providing utilities
        InputQueue
    controller  # grouping device inputs and mapping them to game-specific inputs
        base
            Channel
                Button
                Axis
            Controller
        gamecube
            GamecubeMayflashController
        keyboard
            KeyboardController

    ========================================================
    USER'S CODE

    controllers.py
        class KeyboardWASD(controller.Controller):
            LEFT = controller.Button(pygame.K_a)
            RIGHT = controller.Button(pygame.K_d)

        class KeyboardIJKL(controller.Controller):
            LEFT = controller.Button(pygame.K_j)
            RIGHT = controller.Button(pygame.K_l)

        class GamecubePlayer(controller.Controller):
            LEFT = controller.Axis(gamecube.LEFT)
            RIGHT = controller.Axis(gamecube.RIGHT)

    game.py
        player1 = controllers.KeyboardWASD()
        player2 = controllers.GamecubePlayer(
            input_queue=
        )
"""


class GamecubeMayflashController(Controller):
    # buttons
    X = Button(id=0)
    A = Button(id=1)
    B = Button(id=2)

    # grey analog stick
    LEFT = Axis(id=0, zero_value=-0.1, one_value=-0.77)
    RIGHT = Axis(id=0, zero_value=0.1, one_value=0.77)
    UP = Axis(id=1, zero_value=-0.1, one_value=-0.77)
    DOWN = Axis(id=1, zero_value=0.1, one_value=0.77)

    # shoulder buttons
    L = Button(id=4)
    L_AXIS = Axis(id=3, zero_value=-0.5, one_value=1)

    # 4-way rocker
    D_LEFT = Hat(id=0, axis=0, zero_value=0, one_value=-1)
    D_RIGHT = Hat(id=0, axis=0, zero_value=0, one_value=1)
    D_UP = Hat(id=0, axis=1, zero_value=0, one_value=1)
    D_DOWN = Hat(id=0, axis=1, zero_value=0, one_value=-1)
