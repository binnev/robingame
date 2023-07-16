# Game

Example usage:

```
# your_game.py

from levels import Level1  # Level1 is an entity

class MyGame(Game):
    def __init__(self):
        super().__init__()
        self.children = Group()
        self.child_groups = [self.children]
        self.children.add(Level1(...))  

if __name__ == "__main__":
    MyGame().main()
```

::: robingame.objects.game.Game