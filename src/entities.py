import pygame
from src.settings import TILE_SIZE, RED, TILE_FLOOR, TILE_WALL

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE)) # プレイヤーの見た目を定義
        self.image.fill(RED) # 赤色で塗りつぶし
        self.rect = self.image.get_rect() # プレイヤーの位置とサイズを管理する矩形
        self.rect.x = x * TILE_SIZE # 初期位置をタイルサイズに基づいて設定
        self.rect.y = y * TILE_SIZE 

    def move(self, dx, dy, map_data):
        """プレイヤーを移動させる。移動先が床であれば移動可能。"""
        new_x = self.rect.x + dx * TILE_SIZE # 新しい座標
        new_y = self.rect.y + dy * TILE_SIZE
        tile_x = new_x // TILE_SIZE # 座標に対応するタイル配列のインデックス
        tile_y = new_y // TILE_SIZE
        if 0 <= tile_y < len(map_data) and 0 <= tile_x < len(map_data[0]) and map_data[tile_y][tile_x] == TILE_FLOOR: # タイルがマップ内かつ床であるか確認
            self.rect.x = new_x
            self.rect.y = new_y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE)) # 敵の見た目を定義
        self.image.fill((0, 255, 0)) # 緑色で塗りつぶし
        self.rect = self.image.get_rect() # 敵の位置とサイズを管理する矩形
        self.rect.x = x * TILE_SIZE # 初期位置をタイルサイズに基づいて設定
        self.rect.y = y * TILE_SIZE
    
    def update(self, map_data):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_x = self.rect.x + dx * TILE_SIZE
            new_y = self.rect.y + dy * TILE_SIZE
            tile_x = new_x // TILE_SIZE
            tile_y = new_y // TILE_SIZE
            if 0 <= tile_y < len(map_data) and 0 <= tile_x < len(map_data[0]) and map_data[tile_y][tile_x] == TILE_FLOOR:
                self.rect.x = new_x
                self.rect.y = new_y
                break