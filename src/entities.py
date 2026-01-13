import pygame
import random
from src.settings import TILE_SIZE, RED, TILE_FLOOR, TILE_WALL, TILE_STAIRS, PLAYER_HP, ENEMY_HP, PLAYER_ATTACK_POWER, ENEMY_ATTACK_POWER
from src.pathfinding import get_next_step

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image # プレイヤーの画像
        self.rect = self.image.get_rect() # プレイヤーの位置とサイズを管理する矩形
        self.rect.x = x * TILE_SIZE # 初期位置をタイルサイズに基づいて設定
        self.rect.y = y * TILE_SIZE 
        self.max_hp = PLAYER_HP
        self.hp = self.max_hp
        self.attack_power = PLAYER_ATTACK_POWER
        self.is_alive = True

    def move(self, dx, dy, map_data):
        """プレイヤーを移動させる。移動先が壁でなければ移動可能。"""
        new_x = self.rect.x + dx * TILE_SIZE # 新しい座標
        new_y = self.rect.y + dy * TILE_SIZE
        tile_x = new_x // TILE_SIZE # 座標に対応するタイル配列のインデックス
        tile_y = new_y // TILE_SIZE
        if 0 <= tile_y < len(map_data) and 0 <= tile_x < len(map_data[0]) and map_data[tile_y][tile_x] != TILE_WALL: # タイルがマップ内かつ壁でないか確認
            self.rect.x = new_x
            self.rect.y = new_y


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image # 敵の画像
        self.rect = self.image.get_rect() # 敵の位置とサイズを管理する矩形
        self.rect.x = x * TILE_SIZE # 初期位置をタイルサイズに基づいて設定
        self.rect.y = y * TILE_SIZE
        self.max_hp = ENEMY_HP
        self.hp = self.max_hp
        self.attack_power = ENEMY_ATTACK_POWER
        self.is_alive = True
    
    def update(self, map_data, player_x, player_y):
        """A*パスファインディングを使用してプレイヤーに向かって移動する。"""
        current_x = self.rect.x // TILE_SIZE
        current_y = self.rect.y // TILE_SIZE

        # プレイヤーまでの経路を取得し、次の1歩目を取得
        next_pos = get_next_step((current_x, current_y), (player_x, player_y), map_data)
        
        if next_pos is None:
            return  # 経路が見つからない場合は動かない
        
        new_x, new_y = next_pos
        
        # 移動先にプレイヤーがいる場合は移動しない（重ならないようにする）
        if new_x == player_x and new_y == player_y:
            return
        
        # 移動
        self.rect.x = new_x * TILE_SIZE
        self.rect.y = new_y * TILE_SIZE