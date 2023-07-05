import pygame


class Group(pygame.sprite.Group):
    """Container for multiple Entity objects."""

    def update(self, *args):
        super().update(*args)

    def draw(self, surface: pygame.Surface, debug: bool = False):
        """
        Draws all of the member sprites onto the given surface.
        Different from pygame's Group.draw in that it calls the Entity.draw() method instead of
        just blitting the Entity.image to the screen.
        """
        entities = self.sprites()
        for entity in entities:
            entity.draw(surface, debug)
        self.lostsprites = []

    def kill(self):
        """
        Kill all the sprites in this group. This is different from .empty().
        Does not kill the sprites in other groups.
        """
        for sprite in self:
            sprite.kill()
