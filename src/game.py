import pygame
import sys
import random
import os
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, YELLOW, MOVE_DELAY, COLS, ROWS, TILE_SIZE, TILE_FLOOR, TILE_WALL, TILE_STAIRS, UI_HEIGHT
from src.entities import Player, Enemy
from src.dungeon import DungeonGenerator

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # スクリーン作成
        pygame.display.set_caption("Rogue-like Python")
        self.clock = pygame.time.Clock() # フレームレートを保つための時計
        self.running = True # 動作フラグ
        self.floor = 1 # 現在の階層

        # 画像の読み込みとリサイズ
        self.images = {}
        asset_path = os.path.join(os.path.dirname(__file__), "..", "assets")
        image_files = {
            "floor": "floor.png",
            "wall": "wall.png",
            "downstairs": "downstairs.png",
            "player": "player.png",
            "enemy": "enemy.png"
        }
        for key, filename in image_files.items():
            img = pygame.image.load(os.path.join(asset_path, filename))
            self.images[key] = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

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
            self.player = Player(start_pos[0], start_pos[1], self.images["player"])
        else:
            self.player = Player(1, 1, self.images["player"]) # フォールバック

        self.all_sprites.add(self.player) # プレイヤーをスプライトグループに追加
        
        # 階段の配置
        self._place_stairs()
        
        # 敵の生成
        self._spawn_enemies()

        # 「プレイヤーが動いたら敵も動く」ためのフラグ
        self.enemy_turn_pending = False
        self.game_over = False

    def _spawn_enemies(self):
        """各部屋に敵を配置する（プレイヤーのいる部屋を除く）"""
        player_room_index = -1
        
        # プレイヤーがどの部屋にいるか特定
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
                
                enemy = Enemy(ex, ey, self.images["enemy"])
                self.all_sprites.add(enemy)
                self.enemies.add(enemy)

    def _place_stairs(self):
        """階段をランダムな床タイルに配置する"""
        valid_positions = []
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                if tile == TILE_FLOOR:
                    valid_positions.append((x, y))
        
        if valid_positions:
            stairs_pos = random.choice(valid_positions)
            self.map_data[stairs_pos[1]][stairs_pos[0]] = TILE_STAIRS

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
                # ゲームオーバー時はRキーでリセットのみ受け付ける
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.__init__()  # ゲームをリセット
                    continue
                
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
                    # まず「移動予定の座標（タイル座標）」を計算
                    player_tile_x = self.player.rect.x // TILE_SIZE
                    player_tile_y = self.player.rect.y // TILE_SIZE
                    target_x = player_tile_x + dx
                    target_y = player_tile_y + dy

                    # 移動先に敵がいるか確認
                    target_enemy = None
                    for enemy in self.enemies:
                        enemy_tile_x = enemy.rect.x // TILE_SIZE
                        enemy_tile_y = enemy.rect.y // TILE_SIZE
                        if enemy_tile_x == target_x and enemy_tile_y == target_y:
                            target_enemy = enemy
                            break

                    # 敵がいる場合: 攻撃 / いない場合: 移動
                    if target_enemy is not None:
                        print("Player attacks Enemy!")
                        target_enemy.hp -= self.player.attack_power
                        print(f"Enemy HP: {target_enemy.hp}")
                        if target_enemy.hp <= 0:
                            # kill() で所属している全てのGroupから削除される
                            target_enemy.kill()
                            print("Enemy defeated!")
                        self.enemy_turn_pending = True
                    else:
                        # 通常移動（移動できたかどうかでターン消費を決める）
                        before_x, before_y = self.player.rect.x, self.player.rect.y
                        self.player.move(dx, dy, self.map_data)
                        moved = (self.player.rect.x != before_x) or (self.player.rect.y != before_y)
                        if moved:
                            # 移動先が階段かチェック
                            player_tile_x = self.player.rect.x // TILE_SIZE
                            player_tile_y = self.player.rect.y // TILE_SIZE
                            if self.map_data[player_tile_y][player_tile_x] == TILE_STAIRS:
                                self.next_level()
                            else:
                                self.enemy_turn_pending = True

    def update(self):
        # NOTE: Enemy.update(map_data) は引数が必要なので、all_sprites.update() は呼ばない
        # 「キー入力があったときだけ敵も動く」ターン制にしたいので、フラグを使って制御する
        if self.enemy_turn_pending:
            player_tile_x = self.player.rect.x // TILE_SIZE
            player_tile_y = self.player.rect.y // TILE_SIZE
            self.enemies.update(self.map_data, player_tile_x, player_tile_y)
            
            # 敵の移動後、プレイヤーに隣接している敵がいれば攻撃
            for enemy in self.enemies:
                enemy_tile_x = enemy.rect.x // TILE_SIZE
                enemy_tile_y = enemy.rect.y // TILE_SIZE
                # プレイヤーと隣接しているか判定（上下左右）
                if abs(enemy_tile_x - player_tile_x) + abs(enemy_tile_y - player_tile_y) == 1:
                    print("Enemy attacks Player!")
                    self.player.hp -= enemy.attack_power
                    print(f"Player HP: {self.player.hp}")
                    if self.player.hp <= 0:
                        self.game_over = True
                        print("Game Over!")
            
            self.enemy_turn_pending = False

    def draw(self):
        self.screen.fill(BLACK) # 画面を黒でクリア (これがないと前のフレームの残像が出る)

        # マップ描画 (UI領域の下にオフセット)
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                pos = (x * TILE_SIZE, y * TILE_SIZE + UI_HEIGHT)
                if tile == TILE_FLOOR:
                    self.screen.blit(self.images["floor"], pos)
                elif tile == TILE_WALL:
                    self.screen.blit(self.images["wall"], pos)
                elif tile == TILE_STAIRS:
                    self.screen.blit(self.images["downstairs"], pos)

        # スプライト描画 (オフセット適用)
        for sprite in self.all_sprites:
            offset_rect = sprite.rect.copy()
            offset_rect.y += UI_HEIGHT
            self.screen.blit(sprite.image, offset_rect)
        
        # UI描画
        font = pygame.font.SysFont(None, 36)
        floor_text = font.render(f"Floor: {self.floor}", True, WHITE)
        hp_text = font.render(f"HP: {self.player.hp}/{self.player.max_hp}", True, WHITE)
        self.screen.blit(floor_text, (10, 10))
        self.screen.blit(hp_text, (10, 50))
        
        # ゲームオーバー時の表示
        if self.game_over:
            game_over_font = pygame.font.SysFont(None, 72)
            game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)
            
            reset_font = pygame.font.SysFont(None, 36)
            reset_text = reset_font.render("Press R to Restart", True, WHITE)
            reset_rect = reset_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            self.screen.blit(reset_text, reset_rect)
        
        pygame.display.flip() # 画面更新

    def next_level(self):
        """次の階層へ進む。ダンジョンを再生成し、プレイヤーと敵を再配置する。"""
        self.floor += 1
        print(f"Advance to level {self.floor}")
        
        # ダンジョンを再生成
        self.map_data = self.dungeon_generator.generate_map(COLS, ROWS)
        
        # 既存の敵を全て削除
        for enemy in self.enemies:
            enemy.kill()
        
        # プレイヤーを再配置
        valid_positions = []
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                if tile == TILE_FLOOR:
                    valid_positions.append((x, y))
        
        if valid_positions:
            start_pos = random.choice(valid_positions)
            self.player.rect.x = start_pos[0] * TILE_SIZE
            self.player.rect.y = start_pos[1] * TILE_SIZE
        
        # 階段を再配置
        self._place_stairs()
        
        # 敵を再生成
        self._spawn_enemies()