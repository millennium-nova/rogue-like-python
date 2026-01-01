import pygame
import random
from src.settings import TILE_SIZE, RED, TILE_FLOOR, TILE_WALL, PLAYER_HP, ENEMY_HP, PLAYER_ATTACK_POWER, ENEMY_ATTACK_POWER

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE)) # プレイヤーの見た目を定義
        self.image.fill(RED) # 赤色で塗りつぶし
        self.rect = self.image.get_rect() # プレイヤーの位置とサイズを管理する矩形
        self.rect.x = x * TILE_SIZE # 初期位置をタイルサイズに基づいて設定
        self.rect.y = y * TILE_SIZE 
        self.max_hp = PLAYER_HP
        self.hp = self.max_hp
        self.attack_power = PLAYER_ATTACK_POWER
        self.is_alive = True
        

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
        self.max_hp = ENEMY_HP
        self.hp = self.max_hp
        self.attack_power = ENEMY_ATTACK_POWER
        self.is_alive = True
    
    def update(self, map_data):
        # 上下左右のいずれかにランダムに移動
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