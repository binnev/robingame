from robingame.image import FrameAnimation
from pathlib import Path

import pytest
from pygame import Surface, Color
from redbreast.testing import parametrize, testparams


mocks_folder = Path(__file__).parent.parent.absolute() / "mocks"


@pytest.fixture
def original():
    image = Surface((2, 2))
    image.fill(Color("red"))
    image.set_at((0, 0), Color("black"))
    return FrameAnimation(images=[image])


def assert_original_unchanged(original: FrameAnimation):
    img = original[0]

    # check pixels (covers flip & recolor)
    assert img.get_at((0, 0)) == Color("black")
    assert img.get_at((0, 1)) == Color("red")
    assert img.get_at((1, 0)) == Color("red")
    assert img.get_at((1, 1)) == Color("red")

    # check scale
    assert img.get_width() == 2
    assert img.get_height() == 2


def test_from_spritesheet():
    filename = mocks_folder / "123_spritesheet.png"
    sequence = FrameAnimation.from_spritesheet(filename=filename, image_size=(64, 64))
    assert isinstance(sequence, FrameAnimation)
    assert len(sequence) == 3
    assert isinstance(sequence[0], Surface)


def test_from_images():
    pattern = mocks_folder / "123_series*.png"
    sequence = FrameAnimation.from_images(pattern=pattern)
    assert isinstance(sequence, FrameAnimation)
    assert len(sequence) == 3
    assert isinstance(sequence[0], Surface)


def test_flip(original):
    not_flipped = original.flip(x=False, y=False)
    assert_original_unchanged(not_flipped)

    horizontally_flipped = original.flip(x=True)
    assert horizontally_flipped[0].get_at((0, 0)) == Color("red")
    assert horizontally_flipped[0].get_at((0, 1)) == Color("red")
    assert horizontally_flipped[0].get_at((1, 0)) == Color("black")
    assert horizontally_flipped[0].get_at((1, 1)) == Color("red")

    vertically_flipped = original.flip(y=True)
    assert vertically_flipped[0].get_at((0, 0)) == Color("red")
    assert vertically_flipped[0].get_at((0, 1)) == Color("black")
    assert vertically_flipped[0].get_at((1, 0)) == Color("red")
    assert vertically_flipped[0].get_at((1, 1)) == Color("red")

    both_flipped = original.flip(x=True, y=True)
    assert both_flipped[0].get_at((0, 0)) == Color("red")
    assert both_flipped[0].get_at((0, 1)) == Color("red")
    assert both_flipped[0].get_at((1, 0)) == Color("red")
    assert both_flipped[0].get_at((1, 1)) == Color("black")

    assert_original_unchanged(original)


@parametrize(
    param := testparams("flip_x", "flip_y", "expected_pixels"),
    [
        param(
            description="Not flipped",
            flip_x=False,
            flip_y=False,
            expected_pixels={
                (0, 0): Color("black"),
                (0, 1): Color("red"),
                (1, 0): Color("red"),
                (1, 1): Color("red"),
            },
        ),
        param(
            description="X only",
            flip_x=True,
            flip_y=False,
            expected_pixels={
                (0, 0): Color("red"),
                (0, 1): Color("red"),
                (1, 0): Color("black"),
                (1, 1): Color("red"),
            },
        ),
        param(
            description="Y only",
            flip_x=False,
            flip_y=True,
            expected_pixels={
                (0, 0): Color("red"),
                (0, 1): Color("black"),
                (1, 0): Color("red"),
                (1, 1): Color("red"),
            },
        ),
        param(
            description="X and Y",
            flip_x=True,
            flip_y=True,
            expected_pixels={
                (0, 0): Color("red"),
                (0, 1): Color("red"),
                (1, 0): Color("red"),
                (1, 1): Color("black"),
            },
        ),
    ],
)
def test_flip_in_place(param, original):
    assert original.flip_in_place(x=param.flip_x, y=param.flip_y) is None
    img = original[0]
    for coord, color in param.expected_pixels.items():
        assert img.get_at(coord) == color


def test_recolor(original):
    colormap = {(0, 0, 0): Color("blue")}  # Color is unhashable
    recolored = original.recolor(colormap)
    assert recolored[0].get_at((0, 0)) == Color("blue")
    assert recolored[0].get_at((0, 1)) == Color("red")
    assert recolored[0].get_at((1, 0)) == Color("red")
    assert recolored[0].get_at((1, 1)) == Color("red")
    assert_original_unchanged(original)


def test_recolor_in_place(original):
    colormap = {(0, 0, 0): Color("blue")}  # Color is unhashable
    assert original.recolor_in_place(colormap) is None
    assert original[0].get_at((0, 0)) == Color("blue")
    assert original[0].get_at((0, 1)) == Color("red")
    assert original[0].get_at((1, 0)) == Color("red")
    assert original[0].get_at((1, 1)) == Color("red")


def test_scale(original):
    scaled = original.scale(scale=3)
    assert scaled[0].get_rect().width == 6
    assert scaled[0].get_rect().height == 6
    assert_original_unchanged(original)


def test_scale_in_place(original):
    assert original.scale_in_place(scale=3) is None
    assert original[0].get_rect().width == 6
    assert original[0].get_rect().height == 6


def test_play():
    animation = FrameAnimation(images=[0, 1, 2])
    assert animation.play(0) == 0
    assert animation.play(1) == 1
    assert animation.play(2) == 2
    assert animation.play(3) == 2  # defaults to repeating the last frame
    assert animation.play(0, repeat_frame=1) == 0
    assert animation.play(1, repeat_frame=1) == 1
    assert animation.play(2, repeat_frame=1) == 2
    assert animation.play(3, repeat_frame=1) == 1  # we told it to repeat frame 1


def test_loop():
    animation = FrameAnimation(images=[0, 1, 2])
    assert animation.loop(0) == 0
    assert animation.loop(1) == 1
    assert animation.loop(2) == 2
    assert animation.loop(3) == 0  # continues from the beginning
    assert animation.loop(4) == 1
    assert animation.loop(5) == 2
