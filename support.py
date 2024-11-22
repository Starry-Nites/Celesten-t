from os import walk
import pygame as pg

def importSprite(path):
    surface_list = []
    for _, __, img_file in walk(path):
        for image in img_file:
            full_path = f"{path}/{image}"
            img_surface = pg.image.load(full_path).convert_alpha()
            surface_list.append(img_surface)
    return surface_list