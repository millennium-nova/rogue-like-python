import pygame
import sys
import random
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, MOVE_DELAY, COLS, ROWS, TILE_SIZE
from src.entities import Player
from src.dungeon import DungeonGenerator, TILE_FLOOR, TILE_WALL

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
        
        # 移動制御用
        self.move_delay = MOVE_DELAY  # 連続移動の間隔(ms)
        self.last_move_time = 0 # 最後に移動した時間

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
            

    def update(self):
        self.all_sprites.update()
        
        # キー入力による連続移動処理
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if current_time - self.last_move_time > self.move_delay:
            dx, dy = 0, 0
            if keys[pygame.K_LEFT]:
                dx = -1
            elif keys[pygame.K_RIGHT]:
                dx = 1
            elif keys[pygame.K_UP]:
                dy = -1
            elif keys[pygame.K_DOWN]:
                dy = 1
            
            if dx != 0 or dy != 0:
                self.player.move(dx, dy)
                self.last_move_time = current_time

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
