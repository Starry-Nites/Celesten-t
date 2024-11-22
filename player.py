import pygame
from support import importSprite

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self._import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations["idle"][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 3
        self.jump_move = -10
        # player stats
        self.life = 5
        self.game_over = False
        self.win = False 
        self.status = 'idle'
        self.facing_right = True
        self.facing_left = False
        self.facing_up = False
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.climbing = False
        self.dashing = False
        self.isHittingWall = False
        self.clock = pygame.time.Clock()
        self.current_time = 0
        self.last_dash_time = 0

    def _import_character_assets(self):
        character_path = 'assets/player/'
        self.animations = {
            'idle': [], 
            'walk': [],
            'jump': [],
            'fall': [],
            'lose': [],
            'win': []
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = importSprite(full_path)

    def _animate(self):
        animation = self.animations[self.status]
        # loop over frame index
        if not (self.status == 'lose' and int(self.frame_index) == len(self.animations['lose']) - 1):
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation):
                self.frame_index = 0
        image = animation[int(self.frame_index)]
        image = pygame.transform.scale(image, (35, 50))
        if self.facing_right:
            self.image = image
        elif self.facing_left:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        elif self.facing_up:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
        
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
            self.isHittingWall = True
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
            self.isHittingWall = True
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)

        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)

        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def _get_input(self, player_event):
        
        if player_event[pygame.K_e] and self.isHittingWall:
            self.climbing = True

        elif player_event[pygame.K_d]:
            
            self.direction.x = 1
            self.facing_left = False
            self.facing_right = True
            self.facing_up = False
        elif player_event[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
            self.facing_left = True
            self.facing_up = False
        elif player_event[pygame.K_w]:
            self.facing_up = True
            self.facing_left = False
            self.facing_right = False
        else:
            self.direction.x = 0

        
    def _jump(self):
        self.direction.y = self.jump_move

    def _climb(self, player_event):
        if player_event[pygame.K_w] and self.climbing:
            self.direction.y = -1
        if player_event[pygame.K_s] and self.climbing:
            self.direction.y = 1

    def _dash(self):
        DASH_COOLDOWN = 500
        if self.current_time - self.last_dash_time > DASH_COOLDOWN:
            if self.facing_up:
                self.direction.y = -20
                
            if self.facing_right:
                self.direction.x = 7

            if self.facing_left:
                self.direction.x = -7

            self.last_dash_time = self.current_time
        
    def _get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        elif self.direction.x != 0:
            self.status = 'walk'
        else:
            self.status = 'idle'

    
    def updatey(self, world_shift_y):
        self.rect.y += world_shift_y
        
    def update(self, keys):
        
        self._get_status()
        self.current_time = pygame.time.get_ticks()
        if self.life > 0 and not self.game_over:
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                self._dash()
            if keys[pygame.K_e]:
                self._climb(keys)
            if keys[pygame.K_SPACE] and self.on_ground:
                self._jump()
            else:
                self._get_input(keys)
        elif self.game_over and self.win:
            self.direction.x = 0
            self.status = 'win'
        else:
            self.direction.x = 0
            self.status = 'lose'
        self.clock.tick(60)
        self._animate()

    