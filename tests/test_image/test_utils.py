import pygame
from pathlib import Path
from unittest.mock import patch

import pytest
from pygame import Surface, Color

from robingame.image import utils

mocks_folder = Path(__file__).parent.parent.absolute() / "mocks"


@pytest.mark.parametrize(
    "num_images, expected_len",
    [
        (None, 3),
        (2, 2),
    ],
)
def test_load_spritesheet(num_images, expected_len):
    filename = mocks_folder / "123_spritesheet.png"
    images = utils.load_spritesheet(filename=filename, image_size=(64, 64), num_images=num_images)
    assert len(images) == expected_len
    assert isinstance(images[0], Surface)


def test_load_spritesheet_no_image_size_should_load_whole_sheet_as_one_image():
    filename = mocks_folder / "123_spritesheet.png"
    images = utils.load_spritesheet(filename=filename)
    assert len(images) == 1
    assert isinstance(images[0], Surface)


def test_load_spritesheet_not_found():
    with pytest.raises(FileNotFoundError) as e:
        utils.load_spritesheet(filename="foo/bar.png", image_size=(1, 1))
    assert str(e.value) == "Couldn't find foo/bar.png"


def test_load_image_sequence_not_found():
    with pytest.raises(FileNotFoundError) as e:
        utils.load_image_sequence(pattern="foo/bar*.png")
    assert str(e.value) == "Couldn't find any images matching pattern 'foo/bar*.png'"


@pytest.mark.parametrize(
    "num_images, expected_len",
    [
        (None, 3),
        (2, 2),
    ],
)
def test_load_image_sequence(num_images, expected_len):
    images = utils.load_image_sequence(
        pattern=mocks_folder / "123_series*.png", num_images=num_images
    )
    assert len(images) == expected_len
    assert isinstance(images[0], Surface)


@patch("pygame.image.load")
def test_load_image_error(mock):
    mock.side_effect = pygame.error("Argh!")
    filename = mocks_folder / "123_spritesheet.png"
    with pytest.raises(pygame.error) as e:
        utils.load_image(filename.as_posix())

    assert str(e.value) == "Argh!"


def test_load_image_with_per_pixel_transparency():
    filename = mocks_folder / "per_pixel_alpha.png"
    image = utils.load_image(filename.as_posix())

    # white and red pixels should have full alpha
    for red_pixel in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        assert image.get_at(red_pixel) == (255, 0, 0, 255)
    for white_pixel in [(2, 2), (2, 3), (3, 2), (3, 3)]:
        assert image.get_at(white_pixel) == (255, 255, 255, 255)

    # green pixels should have alpha = 100
    for green_pixel in [(2, 0), (2, 1), (3, 1), (1, 3), (1, 2), (0, 2)]:
        assert image.get_at(green_pixel) == (0, 255, 0, 100)

    # corner pixels should be fully transparent
    for corner_pixel in [(3, 0), (0, 3)]:
        assert image.get_at(corner_pixel) == (0, 0, 0, 0)


def test_load_image_with_global_transparency():
    filename = mocks_folder / "global_alpha.png"
    image = utils.load_image(filename.as_posix())

    # white and red and green pixels should have full alpha
    for red_pixel in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        assert image.get_at(red_pixel) == (255, 0, 0, 255)
    for white_pixel in [(2, 2), (2, 3), (3, 2), (3, 3)]:
        assert image.get_at(white_pixel) == (255, 255, 255, 255)
    for green_pixel in [(2, 0), (2, 1), (3, 1), (1, 3), (1, 2), (0, 2)]:
        assert image.get_at(green_pixel) == (0, 255, 0, 255)

    # corner pixels should be fully transparent
    for corner_pixel in [(3, 0), (0, 3)]:
        assert image.get_at(corner_pixel) == (0, 0, 0, 0)


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
    assert utils.brighten_color(old_color, amount=amount) == new_color


def test_brighten_image():
    filename = mocks_folder / "global_alpha.png"
    image = utils.load_image(filename.as_posix())
    new_image = utils.brighten_image(image, 300)
    for x in range(new_image.get_width() - 1):
        for y in range(new_image.get_height() - 1):
            assert new_image.get_at((x, y)) == (255, 255, 255, 255)


def test_subsurface():
    filename = mocks_folder / "padded.png"
    image = utils.load_image(filename.as_posix())
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
    new_image = utils.scale_image(image, 2)
    assert new_image.get_size() == (4, 4)
    assert new_image is not image  # should be a copy


def test_flip_image():
    image = Surface((2, 2))
    image.fill(Color("white"))
    image.set_at((0, 0), Color("red"))
    new_image = utils.flip_image(image, flip_x=True, flip_y=True)
    assert new_image.get_at((1, 1)) == Color("red")
    assert new_image is not image  # should be a copy


def test_recolor_image():
    image = Surface((2, 2))
    image.fill(Color("white"))
    image.set_at((0, 0), Color("red"))
    new_image = utils.recolor_image(image, color_mapping={(255, 0, 0): (0, 255, 0)})
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
    assert utils.pad_alpha(input) == expected_output


def test_pad_alpha_error():
    with pytest.raises(Exception) as e:
        utils.pad_alpha((0,))
    assert str(e.value) == "bogus colour, man"
