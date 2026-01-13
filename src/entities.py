import pygame
import random
from src.settings import TILE_SIZE, RED, TILE_FLOOR, TILE_WALL, TILE_STAIRS, PLAYER_HP, ENEMY_HP, PLAYER_ATTACK_POWER, ENEMY_ATTACK_POWER, ENEMY_SIGHT_RANGE, ENEMY_ACT_CHANCE
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
        self.sight_range = ENEMY_SIGHT_RANGE
        self.act_chance = ENEMY_ACT_CHANCE
        self.is_alive = True
    
    def update(self, map_data, player_x, player_y):
        """索敵範囲内ならA*で追跡、範囲外ならランダム移動。一定確率で行動する。"""
        # 行動確率チェック
        if random.random() > self.act_chance:
            return  # 行動しない
        
        current_x = self.rect.x // TILE_SIZE
        current_y = self.rect.y // TILE_SIZE

        # プレイヤーとの距離を計算（マンハッタン距離）
        distance = abs(current_x - player_x) + abs(current_y - player_y)
        
        if distance > self.sight_range:
            # 索敵範囲外：ランダム移動
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                new_x = current_x + dx
                new_y = current_y + dy
                
                # マップ範囲内かつ壁でないかチェック
                if 0 <= new_y < len(map_data) and 0 <= new_x < len(map_data[0]):
                    if map_data[new_y][new_x] != TILE_WALL:
                        self.rect.x = new_x * TILE_SIZE
                        self.rect.y = new_y * TILE_SIZE
                        break  # 移動成功したらループを抜ける
        else:
            # 索敵範囲内：A*パスファインディングで追跡
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