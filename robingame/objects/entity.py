from typing import Callable, Iterable

import pygame
from pygame import Surface

from robingame.objects.group import Group


class Entity(pygame.sprite.Sprite):
    """
    Finite State Machine:
    - self.state is executed every tick
    - self.tick is incremented every time the main game loop executes
    - when self.state changes, self.tick is set to 0, so you can track how long the entity has
      been in its current state

    Hierarchical structure:
    - Entities can be added to Groups to create a hierarchical structure
    - The order of groups in the .child_groups attribute determines the draw order; it's basically
      the layers

    Example game structure:
    Game: Entity
    └── scenes: Group
        └── MainMenu: Entity
            ├── buttons: Group
            │   ├── Button: Entity
            │   ├── Button: Entity
            │   └── Button: Entity
            └── sliders: Group
                ├── Slider: Entity
                └── Slider: Entity

    """

    _state: Callable = lambda *args, **kwargs: None  # default state: do nothing
    child_groups: list[Group]  # groups of child Entities belonging to this entity
    tick: int = 0  # number of game loop iterations elapsed in the current state

    def __init__(self, groups: Iterable[Group] = ()):
        super().__init__(*groups)
        self.child_groups = []

    def update(self):
        self.state()  # execute current state function
        # update all child groups. This allows the entire tree of objects to update by only
        # calling the .update() method of the root object
        for group in self.child_groups:
            group.update()
        self.tick += 1  # increment tick to keep track of how long we've been in the current state

    def draw(self, surface: Surface, debug: bool = False):
        # draw all child groups. This allows the entire tree of objects to draw by only calling
        # the .draw() method of the root object.
        for group in self.child_groups:
            group.draw(surface, debug)

    def kill(self):
        """Removes self from all groups it is a member of."""
        for group in self.child_groups:
            group.kill()
        super().kill()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        """
        Reset self.tick when state changes so we know how long we've been in the current state.
        """
        self._state = new_state
        self.tick = 0

    def __repr__(self):
        # The `_Sprite__g` is necessary because of name mangling in subclasses I think
        return f"<{self.__class__.__name__} Entity(in {len(self._Sprite__g)} groups)>"
