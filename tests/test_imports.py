from robingame.gui import Button, Menu
from robingame.gui.menu import MyMenu
from robingame.image import SpriteAnimation, SpriteDict
from robingame.input import InputQueue, EventQueue, KeyboardInputQueue, GamecubeController
from robingame.objects import Game, Entity, PhysicalEntity, FpsTracker, Group, Particle
from robingame.text.font import Font, fonts


def test_imports():
    assert (
        Game,
        Entity,
        PhysicalEntity,
        Group,
        FpsTracker,
        Particle,
        Menu,
        Button,
        MyMenu,
        InputQueue,
        EventQueue,
        KeyboardInputQueue,
        GamecubeController,
        Font,
        fonts,
        SpriteAnimation,
    )
