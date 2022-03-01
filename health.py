import pygame
from pygame.sprite import Sprite


class Health(Sprite) :
     def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen


        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship_health.bmp')
        self.rect = self.image.get_rect()

        