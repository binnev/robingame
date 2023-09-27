import glob
from pathlib import Path

import pygame

from robingame.image.manipulation import not_empty


def init_display() -> pygame.Surface:
    """
    Make sure the pygame display is initialised (required for loading images).
    If the display already exists, return it. If not, generate a new 1x1 pixel display.

    Returns:
        the pygame display
    """
    if not pygame.display.get_init():
        pygame.display.init()
        return pygame.display.set_mode((1, 1))
    else:
        return pygame.display.get_surface()


def load_image(filename: str | Path, colorkey: pygame.Color | int = None) -> pygame.Surface:
    """
    Load an image. Abstracts away some of the pygame pitfalls.

    Args:
        filename: path to the image file
        colorkey: sets the color to treat as transparent (like the green in greenscreen).
            if `-1` is passed, then the color of the top-left pixel will be used.

    Returns:
        the loaded image
    """
    init_display()
    try:
        image = pygame.image.load(filename)
    except pygame.error:
        print("Unable to load image:", filename)
        raise

    # colorkey needs to be set before .convert_alpha() is called, because Surfaces with a
    # per-pixel transparency (i.e. after convert_alpha) ignore colorkey.
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)

    image = image.convert_alpha()
    return image


def load_spritesheet(
    filename: Path | str,
    image_size: (int, int) = None,
    colorkey: pygame.Color = None,
    num_images: int = 0,
) -> [pygame.Surface]:
    """
    Load the image file. Don't call this until pygame.display has been initiated. Split the
    spritesheet into images and return a list of images.

    If image_size is None, load the whole spritesheet as one sprite.

    Args:
        filename: path to the spritesheet file
        image_size: size of the individual frames of the spritesheet (in pixels)
        colorkey: used to set transparency (see `load_image`)
        num_images: can be used to limit the number of frames loaded (default = load all)

    Returns:
        a list of images
    """
    filename = Path(filename)
    if not filename.exists():
        raise FileNotFoundError(f"Couldn't find {filename}")
    sheet = load_image(filename=filename.as_posix(), colorkey=colorkey)

    if image_size:
        width, height = image_size
        num_horizontal = sheet.get_rect().width // width
        num_vertical = sheet.get_rect().height // height
        rects = [
            pygame.Rect((width * i, height * j, width, height))
            for j in range(num_vertical)
            for i in range(num_horizontal)
        ]
        images = [sheet.subsurface(rect) for rect in rects]
        images = list(filter(not_empty, images))
        if num_images:
            images = images[:num_images]
    else:
        images = [sheet]
    return images


def load_image_sequence(
    pattern: Path | str,
    colorkey: pygame.Color = None,
    num_images: int = 0,
) -> [pygame.Surface]:
    """
    Load a sequence of images.

    Args:
        pattern: glob pattern for the image sequence. E.g. if your folder of image contains
            `"example1.png", "example2.png"`, etc, then your pattern should be `"example*.png"`
        colorkey: used to recolor images (see `load_image`)
        num_images: used to limit how many images are loaded (default = load all images that
            match the pattern)

    Returns:
        a list of images
    """
    pattern = Path(pattern).as_posix()
    files = glob.glob(pattern)
    if not files:
        raise FileNotFoundError(f"Couldn't find any images matching pattern '{pattern}'")
    images = [load_image(file, colorkey) for file in files]
    if num_images:
        images = images[:num_images]
    return images
