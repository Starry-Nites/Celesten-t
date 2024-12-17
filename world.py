#import all dependencies
import pygame as pg
from settings import tile_size, WIDTH, HEIGHT, world_map
from tile import Tile
from trap import Trap
from player import Player
from game import Game
from procgen import randomizeBlocks
from coin import Coin
from mobileobstacle import Mobob
import math

#establish the world class
class World:
    def __init__(self, world_data, screen): #World receives the worldmap and screen to start with

        self.screen = screen #attach screen to World

        self.world_data = world_data # attach world map (henceforth known as world_data) to World

        self._setup_world(world_data) #send the world map to the setup world method

        self.game = Game(self.screen)

        #--initialize variables--#
        self.world_shift_y = 0 
        self.world_shift_x = 0
        self.current_y = 0
        self.current_x = 0
        self.gravity = 0.9
        self.points = 0
        self.bottomBlockY = 0
        self.bottomBlockX = 0
        self.generateNew = False
        self.timer = 0
        self.ticks = 0
        self.seconds = 10
        self.seconds1 = 0
        

    def _setup_world(self, layout):
        self.y_list = []
        self.x_list = []
        #--Make all of the sprite groups--#
        self.tiles = pg.sprite.Group()
        self.traps = pg.sprite.Group()
        self.player = pg.sprite.GroupSingle()

        self.coins = pg.sprite.Group()
        self.mobobs = pg.sprite.Group()

        #--Procedural Generation--# 
        for i in range(60): # Run the procgen 'n' times
            world_map.insert(0, "X             X")# | Insert three rows of walls so it doesn't look like digdug
            world_map.insert(0, "X             X")# | Use insert() because append() adds whatever
            world_map.insert(0, "X             X")# V to the bottom of the list, but with insert, you can
                                                  # specify where exactly you want the addition.
                                                  # In this case, add it to the top of the list :3

            world_map.insert(0, randomizeBlocks()) # add one row of randomized blocks so that the generation is actually... y'know... random...
            #print(randomizeBlocks())

        #---Make the World---#                                         
        for row_index, row in enumerate(layout): # layout = world_map
            for col_index, cell in enumerate(row):
                x, y = (col_index * tile_size), (row_index * tile_size)# sets variables x and y equal to the corresponding place they are in the list, then scales it to the tile size

                # Make a block everywhere the layout has an 'X'
                if cell == 'X':
                    tile = Tile((x, y), tile_size) # actually make the tiles
                    self.y_list.append(y)
                    self.x_list.append(x)
                    self.tiles.add(tile) # add it to the tile group

                # Make a trap everywhere the layout has a 't'
                elif cell == 't':
                    trap = Trap((x + (tile_size // 4), y + (tile_size // 4)), tile_size // 2) # make the trap with x's and y's

                    self.traps.add(trap) # add it to the trap group
                
                elif cell == 'C':
                    self.coin_sprite = Coin((x + (tile_size // 4), y + (tile_size // 4)), tile_size // 2)
                    self.coins.add(self.coin_sprite)
                elif cell == 'M':
                    mobob_sprite = Mobob((x, y), tile_size)
                    self.mobobs.add(mobob_sprite)
                
        # Make the player and add it to the group
        player_x
        player_sprite = Player((600, min(self.y_list)+ 800 ))
        self.player.add(player_sprite)

        initial_shift_x = 500
        initial_shift_y = (min(self.y_list) - max(self.y_list)) + 800
                
        # Shift everything to correct the shift caused by the procedural generation
        self.tiles.update(initial_shift_x, initial_shift_y)
        self.traps.update(initial_shift_x, initial_shift_y)
        self.coins.update(initial_shift_x, initial_shift_y)
        self.mobobs.update(initial_shift_x, initial_shift_y)

    #--World shift (left and right)--#
    def _scroll_x(self):
        player = self.player.sprite # Rename the player so that I dont have to type that every time!

        player_x = player.rect.centerx # Rename the player's X value so I dont have to type it every time!

        direction_x = player.direction.x # Rename the player's direction in the X direction so that it is easier to type.

        if player_x < WIDTH // 3 and direction_x < 0: # if the player is going right and the player is within one third of the screen size:
            self.world_shift_x = 8 # set the world shift
            player.speed_x = 0
            player.speed_y = 0 # Make sure the movement doesn't look wonky when we are shifting
        elif player_x > WIDTH - (WIDTH // 3) and direction_x > 0:
            self.world_shift_x = -8
            player.speed_x = 0
            player.speed_y = 0
        else:
            self.world_shift_x = 0
            player.speed_x = 3
            player.speed_y = 3

    def _scroll_y(self): # Literally the exact same thing as _scroll_x, but for Y
        player = self.player.sprite
        player_y = player.rect.centery
        direction_y = player.direction.y
        if player_y < HEIGHT // 2 and direction_y < 0:
            self.world_shift_y = 12
            player.speed_x = 0
            player.speed_y = 0
        elif player_y > HEIGHT - (HEIGHT // 4) and direction_y > 0:
            self.world_shift_y = -12
            player.speed_x = 0
            player.speed_y = 0
        else:
            self.world_shift_y = 0
            player.speed_x = 3
            player.speed_y = 3


    def _apply_gravity(self, player):
        if not player.climbing:
            player.direction.y += self.gravity
            player.rect.y += player.direction.y

    def _horizontal_movement_collision(self):
        player = self.player.sprite # rename self.player.sprite for ease of use
        player.rect.x += (player.direction.x * player.speed_x) # Multiply the direction (usually either 1 or -1) by the speed (usually 3). Then move the player by that many pixels.
                                                           # If the player is supposed to be going right,  multiply speed by 1. If player is going left, multiply it by -1.
        for sprite in self.tiles.sprites(): # check all tile sprites
            if sprite.rect.colliderect(player.rect): #if the player collides with a tile, don't let the player move past the tile.
                
                # Check if moving towards left
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right + 1
                    player.on_left = True
                    
                    self.current_x = player.rect.left
                # Check for moving right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left - 1
                    player.on_right = True
                    
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False 

    def _vertical_movement_collision(self): #pretty much the exact same thing as _horizontal_movement_collision
        player = self.player.sprite
        if player.climbing:
            player.rect.y += (player.direction.y * player.speed_y)
            player = self.player.sprite
        self._apply_gravity(player)
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                    self.current_y = player.rect.top + 100
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0 
                    player.on_ceiling = True
                    self.current_y = player.rect.top - 100
        if player.on_ground and (player.direction.y < 0 or player.direction.y > 1):
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def _handle_traps(self):
        player = self.player.sprite
        for sprite in self.traps.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0 or player.direction.y > 0:
                    player.rect.x += tile_size
                elif player.direction.x > 0 or player.direction.y > 0:
                    player.rect.x -= tile_size
                player.life -= 4

    def _handle_coins(self):
        player = self.player.sprite
        for sprite in self.coins.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0 or player.direction.y > 0:
                    self.points += 1
                    sprite.kill()
                elif player.direction.x > 0 or player.direction.y > 0:
                    self.points += 1
                    sprite.kill()
    def _timer(self):
        if self.seconds > 0:
            self.seconds = 90 - self.ticks // 60
            self.ticks += 1

    def update(self, keys):
        

        # for tiles
        self.traps.update(self.world_shift_x, self.world_shift_y)
        self.traps.draw(self.screen)

        # for traps
        self.tiles.update(self.world_shift_x, self.world_shift_y)
        self.tiles.draw(self.screen)

        # for coins
        self.coins.update(self.world_shift_x, self.world_shift_y)
        self.coins.draw(self.screen)

        # for mobobs
        self.mobobs.update(self.world_shift_x, self.world_shift_y)
        self.mobobs.draw(self.screen)

        #self._correct_shift()

        self._scroll_x()
        self._scroll_y()

        # for player
        self._horizontal_movement_collision()
        self._vertical_movement_collision()
        self._handle_traps()
        self._handle_coins()

        self._timer()
        #self.player.speed = 0
        self.player.update(keys)
        self.game._show_points(self.points)
        self.game._show_timer(self.seconds)
        self.player.draw(self.screen)
        game_state = self.game.game_state(self.player.sprite, self.seconds, self.x_list, self.y_list)
       
        self.tiles.update(0 ,game_state)
        self.traps.update(0 ,game_state)
        self.coins.update(0 ,game_state)
        self.mobobs.update(0 ,game_state)
        return False
                        