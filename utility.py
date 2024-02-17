import pygame
import os

def load_image(filename):
    image_path = os.path.join("assets", filename)
    image = pygame.image.load(image_path).convert()
    image.set_colorkey((0, 0, 0))
    return image



