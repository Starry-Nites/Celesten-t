#-Import dependencies-#
import pygame, sys
from settings import *
from world import World

pygame.init() #initialize pygame

screen = pygame.display.set_mode((WIDTH, HEIGHT)) #width and height are from the settings file.
pygame.display.set_caption("Celesten't")

class Platformer:
    # initialize the whole shebang
    def __init__(self, screen, width, height):
        self.screen = screen
        self.clock = pygame.time.Clock() # make the frame counter

        self.player_event = False #make the player_event false by default upon running to program.

        self.bg_img = pygame.image.load('assets/terrain/background1.png') #load the background
        self.bg_img = pygame.transform.scale(self.bg_img, (width, height))

        pygame.mouse.set_visible(False) # make the mouse invisible just for funsies

        self.keys = pygame.key.get_pressed() # set a variable equal to the dictionary built into pygame that contains every key on the keyboard and has a True/False value tied to it.
        self.reset = False

    def main(self):
        world = World(world_map, self.screen) # send the World class the worldmap and the screen (see World for more info)

        while True: # pretty much until the entire system closes or crashes, run this.

            self.screen.blit(self.bg_img, (0, 0)) # put that background image on the screen

            for event in pygame.event.get(): # if the user hits the 'X,' close the window and stop the program.
                if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()
            self.keys = pygame.key.get_pressed()
                
            
            self.reset = world.update(self.keys)# send the dictionary of keys down to world's update method
            if self.reset:
                world = World(world_map, self.screen)
            pygame.display.update()
            self.clock.tick(60) #set fps to 60

if __name__ == "__main__":
    play = Platformer(screen, WIDTH, HEIGHT)
    play.main()
    