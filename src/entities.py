import pygame
from src.settings import TILE_SIZE, RED

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE)) # プレイヤーの見た目を定義
        self.image.fill(RED) # 赤色で塗りつぶし
        self.rect = self.image.get_rect() # プレイヤーの位置とサイズを管理する矩形
        self.rect.x = x * TILE_SIZE # 初期位置をタイルサイズに基づいて設定
        self.rect.y = y * TILE_SIZE 

    def move(self, dx, dy):
        self.rect.x += dx * TILE_SIZE # 移動量をタイルサイズに基づいて計算
        self.rect.y += dy * TILE_SIZE
