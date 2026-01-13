# src/settings.py
TILE_SIZE = 32
ROWS = 20
COLS = 30
UI_HEIGHT = 80  # UI表示用の高さ
SCREEN_WIDTH = TILE_SIZE * COLS
SCREEN_HEIGHT = TILE_SIZE * ROWS + UI_HEIGHT  # マップ領域 + UI領域
FPS = 60
MOVE_DELAY = 200

# Dungeon generation (BSP)
# BSP分割の深さ（大きいほど部屋・通路が増えやすい）
BSP_MAX_DEPTH = 4
# 区画（リーフ）の最小サイズ（これ未満だとそれ以上分割しない）
BSP_MIN_LEAF_SIZE = 8
# 部屋の最小サイズ
BSP_MIN_ROOM_SIZE = 5
# 部屋を区画の端から離す余白（タイル）
BSP_ROOM_MARGIN = 1
# 縦横比がこの倍率を超えたら分割方向を寄せる
BSP_ASPECT_RATIO_THRESHOLD = 1.5

# tile values
TILE_FLOOR = 0
TILE_WALL = 1
TILE_STAIRS = 2

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Player stats
PLAYER_HP = 30
PLAYER_ATTACK_POWER = 5

# Enemy stats
ENEMY_HP = 10
ENEMY_ATTACK_POWER = 2