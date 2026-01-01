import pygame
import sys
import random
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, MOVE_DELAY, COLS, ROWS, TILE_SIZE, TILE_FLOOR, TILE_WALL
from src.entities import Player, Enemy
from src.dungeon import DungeonGenerator

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # スクリーン作成
        pygame.display.set_caption("Rogue-like Python")
        self.clock = pygame.time.Clock() # フレームレートを保つための時計
        self.running = True # 動作中かどうかを示すフラグ

        # ダンジョン生成
        self.dungeon_generator = DungeonGenerator()
        self.map_data = self.dungeon_generator.generate_map(COLS, ROWS)

        # Sprite: ゲーム内に登場するオブジェクトのベースになるクラス
        # Group: スプライトをまとめて管理するコンテナ
        self.all_sprites = pygame.sprite.Group()    
        self.enemies = pygame.sprite.Group()
        
        # プレイヤーの初期位置をランダムな床の上に設定
        valid_positions = []
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                if tile == TILE_FLOOR:
                    valid_positions.append((x, y))
        
        if valid_positions:
            start_pos = random.choice(valid_positions)
            self.player = Player(start_pos[0], start_pos[1])
        else:
            self.player = Player(1, 1) # フォールバック

        self.all_sprites.add(self.player) # プレイヤーをスプライトグループに追加
        
        # 敵の生成
        self._spawn_enemies()

        # 「プレイヤーが動いたら敵も動く」ためのフラグ
        self.enemy_turn_pending = False

    def _spawn_enemies(self):
        """各部屋に敵を配置する（プレイヤーのいる部屋を除く）"""
        player_room_index = -1
        
        # プレイヤーがどの部屋にいるか特定（簡易判定）
        px, py = self.player.rect.x // TILE_SIZE, self.player.rect.y // TILE_SIZE
        for i, room in enumerate(self.dungeon_generator.rooms):
            rx, ry, rw, rh = room
            if rx <= px < rx + rw and ry <= py < ry + rh:
                player_room_index = i
                break
        
        # 部屋ごとに敵を配置
        for i, room in enumerate(self.dungeon_generator.rooms):
            if i == player_room_index:
                continue # プレイヤーのいる部屋には敵を置かない
            
            # 一定の確率で敵を配置
            if random.random() < 0.8:
                rx, ry, rw, rh = room
                # 部屋の中のランダムな位置
                ex = rx + random.randint(0, rw - 1)
                ey = ry + random.randint(0, rh - 1)
                
                enemy = Enemy(ex, ey)
                self.all_sprites.add(enemy)
                self.enemies.add(enemy)

    def run(self): # メインループ
        while self.running:
            self.handle_events() # イベント処理
            self.update() # 状態更新
            self.draw() # 画面描画
            self.clock.tick(FPS) # フレームレートを維持
        
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                dx, dy = 0, 0
                if event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1
                elif event.key == pygame.K_UP:
                    dy = -1
                elif event.key == pygame.K_DOWN:
                    dy = 1
                
                if dx != 0 or dy != 0:
                    self.player.move(dx, dy, self.map_data)
                    self.enemy_turn_pending = True

    def update(self):
        # NOTE: Enemy.update(map_data) は引数が必要なので、all_sprites.update() は呼ばない。
        # 「キー入力があったときだけ敵も動く」ターン制にしたいので、フラグを使って制御する。
        if self.enemy_turn_pending:
            self.enemies.update(self.map_data)
            self.enemy_turn_pending = False

    def draw(self):
        self.screen.fill(BLACK) # 画面を黒でクリア (これがないと前のフレームの残像が出る)

        # マップ描画
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tile == TILE_FLOOR:
                    pygame.draw.rect(self.screen, WHITE, rect)
                elif tile == TILE_WALL:
                    pygame.draw.rect(self.screen, BLACK, rect)

        self.all_sprites.draw(self.screen) # すべてのスプライトを描画
        pygame.display.flip() # 画面更新
        
       