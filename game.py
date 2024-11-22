import pygame
from settings import WIDTH, HEIGHT

pygame.font.init()

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('impact', 70)
        self.message_color = pygame.Color('darkorange')
        self.pointColor = pygame.Color('darkgoldenrod1')
        self.pointFont = pygame.font.SysFont('impact', 60)
        self.points = 0

    def _show_points(self, player, points):
        coin_size = 30
        img_path = 'assets/coin/0.png'
        coin_image = pygame.image.load(img_path)
        coin_image = pygame.transform.scale(coin_image, (3 * coin_size, 3 * coin_size))

        indent = 0
        message = self.font.render(f"{points}", True, self.pointColor)

        self.screen.blit(message, (100, 30))
        self.screen.blit(coin_image, (indent, coin_size))

    def _game_lose(self, player):
        player.game_over = True
        message = self.font.render("You Lose...", True, self.message_color)
        self.screen.blit(message, (WIDTH // 3 + 70, 70))

    def _game_win(self, player):
        player.game_over = True
        player.win = True
        message = self.font.render('You Win!!', True, self.message_color)
        self.screen.blit(message,(WIDTH // 3, 70))

    def _tally_points(self):
        self.points += 1
        message = self.font.render(f"{self.points}", True, self.pointColor)

        self.screen.blit(message, (100, 30))
        print(self.points)

    def game_state(self, player, goal):
        if player.life <= 0 or player.rect.y >= HEIGHT:
            self._game_lose(player)
        elif player.rect.colliderect(goal.rect):
            self._game_win(player)