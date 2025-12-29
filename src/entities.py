import pygame
from src.settings import TILE_SIZE, RED

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

    def move(self, dx, dy):
        self.rect.x += dx * TILE_SIZE
        self.rect.y += dy * TILE_SIZE
