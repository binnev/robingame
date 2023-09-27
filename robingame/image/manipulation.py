import pygame

from robingame.utils import limit_value


def empty_image(*args, **kwargs) -> pygame.Surface:
    """
    Generate an empty Surface with `.convert_alpha()` already called.

    Returns:
        an empty Surface
    """
    img = pygame.Surface(*args, **kwargs).convert_alpha()
    img.fill((0, 0, 0, 0))
    return img


def not_empty(surface: pygame.Surface) -> bool:
    """
    Check if a surface has any non-zero pixels. `Surface.get_bounding_rect()` returns the
    smallest rectangle on the surface containing data. If the surface is empty, it will return
    Rect(0, 0, 0, 0), for which `any` returns False.
    """
    return any(surface.get_bounding_rect())


def pad_alpha(colour_tuple: pygame.Color | tuple) -> pygame.Color | tuple:
    """
    Add the 4th (alpha) channel to a length 3 color tuple.
    By default it sets the new alpha channel to full opacity (255).

    Args:
        colour_tuple:

    Returns:
        a colour
    """
    if len(colour_tuple) == 3:
        # if no alpha channel supplied, assume it's full opacity
        return (*colour_tuple, 255)
    elif len(colour_tuple) == 4:
        return colour_tuple
    else:
        raise Exception("bogus colour, man")


def brighten_color(color: pygame.Color | tuple, amount: int) -> pygame.Color:
    """
    Increase all channels to brighten a colour.
    Does not allow values greater than 255.

    Args:
        color: the input colour
        amount: how much to increase each channel

    Returns:
        the output colour
    """
    color = pygame.Color(color)
    r = limit_value(color.r + amount, between=(0, 255))
    g = limit_value(color.g + amount, between=(0, 255))
    b = limit_value(color.b + amount, between=(0, 255))
    return pygame.Color(r, g, b, color.a)


def brighten_image(image: pygame.Surface, amount: int) -> pygame.Surface:
    """
    Use `brighten_color` to brighten all pixels in an image by `amount`.

    Args:
        image: the input image
        amount: how much to increase brightness

    Returns:
        a new image
    """
    width, height = image.get_size()
    # surface.copy() inherits surface's colorkey; preserving transparency
    new_image = image.copy()

    # iterate over all the pixels in the old surface, and write a pixel to the new surface in the
    # corresponding position. If the colour of the present pixel has an entry in the
    # color_mapping dict, then write the new colour instead of the old one.
    for x in range(width):
        for y in range(height):
            color = image.get_at((x, y))[:]
            new_color = brighten_color(color, amount)
            new_image.set_at((x, y), pygame.Color(*new_color))
    return new_image


def scale_image(image: pygame.Surface, scale: float) -> pygame.Surface:
    """
    Return a scaled copy of an image.

    Args:
        image: input image
        scale: factor by which to scale image

    Returns:
        output image
    """
    width, height = image.get_rect().size
    image = pygame.transform.scale(image, (width * scale, height * scale))
    return image


def flip_image(image: pygame.Surface, flip_x: bool = False, flip_y: bool = False) -> pygame.Surface:
    """
    Return a flipped copy of an image.

    Args:
        image: input image
        flip_x: flip horizontally
        flip_y: flip vertically

    Returns:
        output image
    """
    return pygame.transform.flip(image, bool(flip_x), bool(flip_y))


def recolor_image(surface: pygame.Surface, color_mapping: dict) -> pygame.Surface:
    """
    Return a recolored copy of an image.

    Args:
        surface: input image
        color_mapping: dictionary of old colors (keys) to new colors (values).
            Unfortunately they have to be RGB tuples, not pygame Colors, because Color is an
            unhashable type...

    Returns:
        output image
    """
    # make sure the colourmap has alpha channel on all colours
    color_mapping = {pad_alpha(k): pad_alpha(v) for k, v in color_mapping.items()}
    width, height = surface.get_size()
    # surface.copy() inherits surface's colorkey; preserving transparency
    new_surface = surface.copy()

    # iterate over all the pixels in the old surface, and write a pixel to the new surface in the
    # corresponding position. If the colour of the present pixel has an entry in the
    # color_mapping dict, then write the new colour instead of the old one.
    for x in range(width):
        for y in range(height):
            color = surface.get_at((x, y))[:]
            new_color = color_mapping.get(color)
            if new_color:
                new_surface.set_at((x, y), pygame.Color(*new_color))
            else:
                new_surface.set_at((x, y), pygame.Color(*color))

    return new_surface
