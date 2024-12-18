import pygame
from support import importSprite

class Mobob(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.mobob_img = importSprite('assets/trap/MobOb')
        self.frame_index = 0
        self.animation_delay = 1

        self.image = self.mobob_img[self.frame_index]
        self.image = pygame.transform.scale(self.image, (size, size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)

    def _animate(self):
        sprites = self.mobob_img
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
