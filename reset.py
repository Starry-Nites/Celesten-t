import pygame

def reset(player, x_list, y_list):
    player.rect.x = min(x_list) + 40
    player.rect.y = max(y_list) - 40
