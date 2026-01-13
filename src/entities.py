import pygame
import random
from src.settings import TILE_SIZE, RED, TILE_FLOOR, TILE_WALL, TILE_STAIRS, PLAYER_HP, ENEMY_HP, PLAYER_ATTACK_POWER, ENEMY_ATTACK_POWER

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
        """プレイヤーを移動させる。移動先が壁でなければ移動可能。"""
        new_x = self.rect.x + dx * TILE_SIZE # 新しい座標
        new_y = self.rect.y + dy * TILE_SIZE
        tile_x = new_x // TILE_SIZE # 座標に対応するタイル配列のインデックス
        tile_y = new_y // TILE_SIZE
        if 0 <= tile_y < len(map_data) and 0 <= tile_x < len(map_data[0]) and map_data[tile_y][tile_x] != TILE_WALL: # タイルがマップ内かつ壁でないか確認
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
    
    def update(self, map_data, player_x, player_y):
        """プレイヤーに1マス近づく単純な追跡AI。壁なら動かない。"""
        current_x = self.rect.x // TILE_SIZE
        current_y = self.rect.y // TILE_SIZE

        dx = player_x - current_x
        dy = player_y - current_y

        # 距離が大きい軸を優先
        if abs(dx) >= abs(dy):
            step_x = 1 if dx > 0 else -1 if dx < 0 else 0
            step_y = 0
        else:
            step_x = 0
            step_y = 1 if dy > 0 else -1 if dy < 0 else 0

        if step_x == 0 and step_y == 0:
            return  # すでに同じタイル

        new_x = current_x + step_x
        new_y = current_y + step_y

        # 移動先にプレイヤーがいる場合は移動しない（重ならないようにする）
        if new_x == player_x and new_y == player_y:
            return

        if 0 <= new_y < len(map_data) and 0 <= new_x < len(map_data[0]) and map_data[new_y][new_x] == TILE_FLOOR:
            self.rect.x = new_x * TILE_SIZE
            self.rect.y = new_y * TILE_SIZE