from pathlib import Path

import pytest
from pygame import Surface, Color

from robingame.image import manipulation, loading

mocks_folder = Path(__file__).parent.parent.absolute() / "mocks"


@pytest.mark.parametrize(
    "amount, old_color, new_color",
    [
        (
            20,
            (0, 0, 0),
            (20, 20, 20),
        ),
        (
            20,
            Color(0, 0, 0),
            (20, 20, 20),
        ),
        (
            20,
            (250, 250, 250),
            (255, 255, 255),
        ),
        (
            20,
            (255, 255, 255),
            (255, 255, 255),
        ),
        (
            20,
            (0, 250, 255),
            (20, 255, 255),
        ),
        (
            20,
            (0, 0, 0, 0),
            (20, 20, 20, 0),
        ),
        (
            20,
            Color(0, 0, 0, 0),
            (20, 20, 20, 0),
        ),
        (
            -50,
            Color(0, 0, 0, 0),
            (0, 0, 0, 0),
        ),
        (
            -50,
            Color(0, 30, 55, 0),
            (0, 0, 5, 0),
        ),
    ],
)
def test_brighten_color(amount, old_color, new_color):
    assert manipulation.brighten_color(old_color, amount=amount) == new_color


def test_brighten_image():
    filename = mocks_folder / "global_alpha.png"
    image = loading.load_image(filename.as_posix())
    new_image = manipulation.brighten_image(image, 300)
    for x in range(new_image.get_width() - 1):
        for y in range(new_image.get_height() - 1):
            assert new_image.get_at((x, y)) == (255, 255, 255, 255)


def test_subsurface():
    filename = mocks_folder / "padded.png"
    image = loading.load_image(filename.as_posix())
    assert image.get_width() == 16
    assert image.get_height() == 6

    x, y, w, h = image.get_bounding_rect()
    assert x == 7
    assert y == 2
    assert w == 2
    assert h == 2

    new = image.subsurface(image.get_bounding_rect())
    assert new.get_rect() == (0, 0, 2, 2)


def test_scale_image():
    image = Surface((2, 2))
    image.fill(Color("white"))
    image.set_at((0, 0), Color("red"))
    new_image = manipulation.scale_image(image, 2)
    assert new_image.get_size() == (4, 4)
    assert new_image is not image  # should be a copy


def test_flip_image():
    image = Surface((2, 2))
    image.fill(Color("white"))
    image.set_at((0, 0), Color("red"))
    new_image = manipulation.flip_image(image, flip_x=True, flip_y=True)
    assert new_image.get_at((1, 1)) == Color("red")
    assert new_image is not image  # should be a copy


def test_recolor_image():
    image = Surface((2, 2))
    image.fill(Color("white"))
    image.set_at((0, 0), Color("red"))
    new_image = manipulation.recolor_image(image, color_mapping={(255, 0, 0): (0, 255, 0)})
    assert new_image.get_at((0, 0)) == Color("green")
    assert new_image is not image  # should be a copy


@pytest.mark.parametrize(
    "input, expected_output",
    [
        (Color("red"), (255, 0, 0, 255)),
        ((255, 0, 0), (255, 0, 0, 255)),
    ],
)
def test_pad_alpha(input, expected_output):
    assert manipulation.pad_alpha(input) == expected_output


def test_pad_alpha_error():
    with pytest.raises(Exception) as e:
        manipulation.pad_alpha((0,))
    assert str(e.value) == "bogus colour, man"
