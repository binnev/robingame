import string
from pathlib import Path

from robingame.image import init_display
from robingame.text.font import Font

window = init_display()

assets = Path(__file__).parent / "assets"

test_font = Font.from_spritesheet(
    filename=assets / "test_font.png",
    image_size=(16, 16),
    letters=(
        string.ascii_uppercase
        + string.ascii_lowercase
        + r"1234567890-=!@#$%^&*()_+[]\;',./{}|:\"<>?~`"
    ),
    trim=True,
    xpad=1,
    space_width=8,
)

cellphone_black = Font.from_spritesheet(
    filename=assets / "cellphone-black.png",
    image_size=(7, 9),
    letters=(
        """!"#$%&'()*+,-./0123456789:;<=>?@"""
        + string.ascii_uppercase
        + r"[\]^_`"
        + string.ascii_lowercase
        + r"{|}~"
    ),
    xpad=1,
    colorkey=-1,
    trim=True,
    space_width=4,
)
cellphone_white = Font.from_spritesheet(
    filename=assets / "cellphone-white.png",
    image_size=(7, 9),
    letters=(
        r"""!"#$%&'()*+,-./0123456789:;<=>?@"""
        + string.ascii_uppercase
        + r"[\]^_`"
        + string.ascii_lowercase
        + r"{|}~"
    ),
    xpad=1,
    colorkey=-1,
    trim=True,
    space_width=4,
)
cellphone_white_mono = Font.from_spritesheet(
    filename=assets / "cellphone-white.png",
    image_size=(7, 9),
    letters=(
        r"""!"#$%&'()*+,-./0123456789:;<=>?@"""
        + string.ascii_uppercase
        + r"[\]^_`"
        + string.ascii_lowercase
        + r"{|}~"
    ),
    colorkey=-1,
)
chunky_retro = Font.from_spritesheet(
    filename=assets / "chunky_retro.png",
    image_size=(20, 20),
    letters=(
        r"""!"#$%&'()*+,-."""
        r"/0123456789:;<="
        r">?@ABCDEFGHIJKL"
        r"MNOPQRSTUVWXYZ["
        r"\]^_abcdefghij"
        r"klmnopqrstuvwxy"
        r"z{|}~çÜÉÂÄÀ ÇÊ"
        r"ËÈÏÎÌÄ ÉÆæÔÖÒÛÙ"
    ),
    space_width=12,
    trim=True,
    xpad=-1,
)
sharp_retro = Font.from_spritesheet(
    filename=assets / "sharp_retro.png",
    image_size=(8, 16),
    letters=(
        r"""!"#$%'()*+,-./"""
        + "0123456789:;<=>?@"
        + string.ascii_uppercase
        + "[\\]^_`"
        + string.ascii_lowercase
        + "{|}~"
    ),
    trim=True,
    xpad=1,
    space_width=6,
)

tiny_white = Font.from_spritesheet(
    filename=assets / "tiny.png",
    image_size=(8, 12),
    letters=(
        string.ascii_uppercase
        + string.ascii_lowercase
        + "ÄËÏÖÜŸÁÉÍÓÚÝÀÈÌÒÙÂÊÎÔÛ"
        + "äëïöüÿáéíóúýàèìòùâêîôû"
        + "ÃÑÕãñõ"
        + "1234567890"
        + ".,-!?:;'"
        + '"`&+_/#%=()[]{}*<>@^|~$'
        + "\\"
    ),
    trim=True,
    xpad=1,
    space_width=4,
)
