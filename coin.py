import pygame
from support import importSprite
from game import Game

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.coin_img = importSprite("assets/coin")
        self.frame_index = 0
        self.animation_delay = 3
        self.image = self.coin_img[self.frame_index]
        self.image = pygame.transform.scale(self.image, (size, size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)

    def _animate(self):
        sprites = self.coin_img
        sprite_index = (self.frame_index // self.animation_delay % len(sprites))
        self.image = sprites[sprite_index]
        self.frame_index += 1
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)
        if self.frame_index // self.animation_delay > len(sprites):
            self.frame_index = 0

    def update(self, x_shift, y_shift):
        self._animate()
        self.rect.x += x_shift
        self.rect.y += y_shift

