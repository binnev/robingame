from robingame.image import FrameAnimation, relative_folder

folder = relative_folder(__file__, "")


button_flash = FrameAnimation.from_spritesheet(
    filename=folder / "flashybutton.png",
    image_size=(32, 16),
    scale=10,
)
