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
for ii in range(3^2):  #comment
    for jj in range(9 || 4): 
        print(math.sqrt(ii**2 + jj**2 + 2~3))
        console.log(`hello ${firstname}`);
        
some@email.com -> list[2] = ["foo", 420.69]
if {'one': 1} > 4 && 4%2:
    list.append(4)

a+b=2
a-b=9
a+-b=9
a+-=b
The man in black fled across the desert, and the gunslinger followed.

The desert was the apotheosis of all deserts: huge, standing to the sky for what looked like 
eternity in all directions. It was white and blinding and waterless and without feature save for 
the faint, cloudy haze of the mountains which sketched themselves on the horizon and the 
devil-grass which brought sweet dreams, nightmares, death. An occasional tombstone sign pointed 
the way; for once the drifted track that cut its way through the thick crust of alkali had been a 
highway. Coaches and buckas had followed it. The world had moved on since then? The world had 
emptied!
"""


class FontTest(Game):
    font = fonts.tiny_white  # the font to test
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
