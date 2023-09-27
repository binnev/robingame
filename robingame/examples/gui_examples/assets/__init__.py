from pathlib import Path

from robingame.image import FrameAnimation

folder = Path(__file__).parent


button_flash = FrameAnimation.from_spritesheet(
    filename=folder / "flashybutton.png",
    image_size=(32, 16),
    scale=10,
)
