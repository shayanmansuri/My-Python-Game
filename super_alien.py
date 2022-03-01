import pygame
from pygame.sprite import Sprite
from alien import Alien
import random

class SuperAliens(Alien):
    """A class to represent a single super alien in the fleet."""

    def __init__(self, ai_game):
        super().__init__(ai_game)
        self.health = 2 
      
        self.image = pygame.image.load('images/alien2.bmp')
   
        self.rect.x = self.screen_rect.right
    
        self.rect.y = self.rect.height * 6
        

        

