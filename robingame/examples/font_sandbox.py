import pygame.draw
from pygame.color import Color
from pygame.surface import Surface

from robingame.objects import Game
from robingame.text import fonts

snippet = r"""THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG 
the quick brown fox jumps over the lazy dog 
Numbers 1234567890
Punctuation `~!@#$%^&*()-=_+[]\{}|;':",./<>?
Accents ÀÈÌÒÙ àèìòù ÁÉÍÓÚÝ áéíóúý ÂÊÎÔÛ âêîôû ÃÑÕ ãñõ ÄËÏÖÜŸ äëïöüÿ

Mötörhêàd

code snippet with indentation
for ii in range(3): 
    for jj in range(9): 
        print(math.sqrt(ii**2 + jj**2))
"""


class FontTest(Game):
    font = fonts.cellphone_white  # the font to test
    window_width = 1500
    window_height = 1000
    screen_color = (150, 150, 150)

    def draw(self, surface: Surface, debug: bool = False):
        super().draw(surface, debug)
        X = 50
        Y = 30
        WRAP = 1400
        self.font.render(
            surface,
            snippet,
            scale=2,
            wrap=WRAP,
            x=X,
            y=Y,
            align=-1,
        )
        pygame.draw.rect(surface, color=Color("red"), rect=(X, Y, WRAP, WRAP), width=1)


if __name__ == "__main__":
    FontTest().main()
