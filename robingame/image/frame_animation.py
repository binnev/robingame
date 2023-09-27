from pathlib import Path

from pygame import Surface, Color
from typing import Sequence
from robingame.image import manipulation, loading


class FrameAnimation(list):
    """
    Manages a sequence of images.
    Handles loading from various formats (spritesheet, multiple image files, single image file).
    Adds basic frame-by-frame animation functions to play the image sequence once, or loop it.
    Can scale, flip, and recolor itself.
    """

    # =================== instantiation ===================

    def __init__(
        self,
        images: Sequence[Surface] = None,
        scale: float = None,
        flip_x: bool = False,
        flip_y: bool = False,
        colormap: dict[Color:Color] = None,
    ):
        """
        Args:
            images: a list of Surfaces to use as frames
            scale: factor by which to scale images
            flip_x: flip all images horizontally if True
            flip_y: flip all images vertically if True
            colormap: used to recolor images. It is a mapping of old colours to new colours
        """
        super().__init__(images)
        if scale:
            self.scale_in_place(scale)
        if flip_x or flip_y:
            self.flip_in_place(flip_x, flip_y)
        if colormap:
            self.recolor_in_place(colormap)

    @classmethod
    def from_spritesheet(
        cls,
        filename: Path | str,
        image_size: (int, int),
        colorkey=None,
        num_images: int = 0,
        scale: float = None,
        flip_x: bool = False,
        flip_y: bool = False,
        colormap: dict = None,
    ) -> "FrameAnimation":
        """
        Load from a spritesheet.

        Args:
            filename: name of the spritesheet file
            image_size: size (in pixels) of the frames in the spritesheet
            colorkey: used by pygame.Surface.set_colorkey
            num_images: can be used to limit the number of images loaded
            scale: see __init__
            flip_x: see __init__
            flip_y: see __init__
            colormap: see __init__

        Returns:
            a new instance
        """
        images = loading.load_spritesheet(
            filename=filename, image_size=image_size, colorkey=colorkey, num_images=num_images
        )
        return cls(images=images, scale=scale, flip_x=flip_x, flip_y=flip_y, colormap=colormap)

    @classmethod
    def from_images(
        cls,
        pattern: Path | str,
        colorkey=None,
        num_images: int = 0,
        scale: float = None,
        flip_x: bool = False,
        flip_y: bool = False,
        colormap: dict = None,
    ) -> "FrameAnimation":
        """
        Load from a sequence of images in a folder.

        Args:
            pattern: glob pattern used by `load_image_sequence`
            colorkey: used by pygame.Surface.set_colorkey
            num_images: can be used to limit the number of images loaded
            scale: see __init__
            flip_x: see __init__
            flip_y: see __init__
            colormap: see __init__

        Returns:
            a new instance
        """
        images = loading.load_image_sequence(
            pattern=pattern, colorkey=colorkey, num_images=num_images
        )
        return cls(images=images, scale=scale, flip_x=flip_x, flip_y=flip_y, colormap=colormap)

    # =================== playback ===================

    def play(self, n: int, repeat_frame: int = -1) -> Surface:
        """
        Play the animation once and then continue returning the specified frame
        (default=last frame).

        Args:
            n: the current frame (use game tick or some other timer variable)
            repeat_frame: the frame to repeat after the animation has finished (default = last
                frame)

        Returns:
            the image to display
        """
        try:
            return self[n]
        except IndexError:
            return self[repeat_frame]

    def loop(self, n: int) -> Surface:
        """
        Like `play()` but if `n` is greater than the number of frames, start again at the beginning.

        Args:
            n: the current frame (use game tick or some other timer variable)

        Returns:
            the image to display
        """
        return self.play(n % len(self))

    # =================== image manipulation ===================

    def flip(self, x=False, y=False) -> "FrameAnimation":
        """
        Flip images and return a new instance.

        Args:
            x: flip horizontally
            y: flip vertically

        Returns:
            a new instance
        """
        return self.__class__(images=self, flip_x=x, flip_y=y)

    def flip_in_place(self, x: bool, y: bool):
        """
        Flip images in place.

        Args:
            x: flip horizontally
            y: flip vertically
        """
        for index, image in enumerate(self):
            self[index] = manipulation.flip_image(image, flip_x=x, flip_y=y)

    def recolor(self, colormap: dict) -> "FrameAnimation":
        """
        Like `recolor()` but returns a new instance.

        Args:
            colormap: mapping of old colours to new colours

        Returns:
            a new instance
        """
        return self.__class__(images=self, colormap=colormap)

    def recolor_in_place(self, colormap: dict):
        """
        Recolor in place.

        Args:
            colormap: mapping of old colours to new colours
        """
        for index, image in enumerate(self):
            self[index] = manipulation.recolor_image(image, colormap)

    def scale(self, scale: float) -> "FrameAnimation":
        """
        Scale images and return a new instance.

        Args:
            scale: factor by which to scale images

        Returns:
            a new instance
        """
        return self.__class__(images=self, scale=scale)

    def scale_in_place(self, scale: float):
        """
        Scale in place.

        Args:
            scale: factor by which to scale images
        """
        for index, image in enumerate(self):
            self[index] = manipulation.scale_image(image, scale)
