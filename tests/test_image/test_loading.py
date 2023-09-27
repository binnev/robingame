from pathlib import Path
from unittest.mock import patch

import pygame
import pytest
from pygame import Surface

from robingame.image import loading

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
    images = loading.load_spritesheet(filename=filename, image_size=(64, 64), num_images=num_images)
    assert len(images) == expected_len
    assert isinstance(images[0], Surface)


def test_load_spritesheet_no_image_size_should_load_whole_sheet_as_one_image():
    filename = mocks_folder / "123_spritesheet.png"
    images = loading.load_spritesheet(filename=filename)
    assert len(images) == 1
    assert isinstance(images[0], Surface)


def test_load_spritesheet_not_found():
    with pytest.raises(FileNotFoundError) as e:
        loading.load_spritesheet(filename="foo/bar.png", image_size=(1, 1))
    assert str(e.value) == "Couldn't find foo/bar.png"


def test_load_image_sequence_not_found():
    with pytest.raises(FileNotFoundError) as e:
        loading.load_image_sequence(pattern="foo/bar*.png")
    assert str(e.value) == "Couldn't find any images matching pattern 'foo/bar*.png'"


@pytest.mark.parametrize(
    "num_images, expected_len",
    [
        (None, 3),
        (2, 2),
    ],
)
def test_load_image_sequence(num_images, expected_len):
    images = loading.load_image_sequence(
        pattern=mocks_folder / "123_series*.png", num_images=num_images
    )
    assert len(images) == expected_len
    assert isinstance(images[0], Surface)


@patch("pygame.image.load")
def test_load_image_error(mock):
    mock.side_effect = pygame.error("Argh!")
    filename = mocks_folder / "123_spritesheet.png"
    with pytest.raises(pygame.error) as e:
        loading.load_image(filename.as_posix())

    assert str(e.value) == "Argh!"


def test_load_image_with_per_pixel_transparency():
    filename = mocks_folder / "per_pixel_alpha.png"
    image = loading.load_image(filename.as_posix())

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
    image = loading.load_image(filename.as_posix())

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
