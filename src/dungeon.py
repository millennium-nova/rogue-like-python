import random

# タイルID
TILE_FLOOR = 0
TILE_WALL = 1

class Node:
    """BSP木のノード。ダンジョンの区画を表す。"""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left = None
        self.right = None
        self.room = None  # (x, y, w, h)

    def center(self):
        """区画の中心座標を返す"""
        if self.room:
            return (self.room[0] + self.room[2] // 2, self.room[1] + self.room[3] // 2)
        else:
            return (self.x + self.width // 2, self.y + self.height // 2)

class DungeonGenerator:
    """
    BSP（二分空間分割）法を使用してダンジョンを生成するクラス。
    """
    def __init__(self):
        self.map_data = []
        self.min_size = 8  # 区画の最小サイズ
        self.min_room_size = 5 # 部屋の最小サイズ

    def generate_map(self, width, height):
        """
        指定された幅と高さでダンジョンマップを生成する。
        
        Args:
            width (int): マップの幅（タイル数）
            height (int): マップの高さ（タイル数）
            
        Returns:
            list[list[int]]: タイル情報の2次元配列 (0: 床, 1: 壁)
        """
        # すべてのタイルを壁に設定
        # width 個の TILE_WALL を要素に持つ配列を height 個作成
        self.map_data = [[TILE_WALL for _ in range(width)] for _ in range(height)]
        
        root = Node(0, 0, width, height)
        
        # 再帰的に分割 (4回程度分割)
        self._split_node(root, 4)
        
        # 部屋と通路の生成
        self._create_rooms_and_corridors(root)
        
        return self.map_data

    def _split_node(self, node, depth):
        """ノードを再帰的に分割する"""
        if depth <= 0:
            return

        # 分割方向を決定 (縦長なら水平分割、横長なら垂直分割しやすくする)
        split_vertically = random.choice([True, False])
        if node.width > node.height * 1.5:
            split_vertically = True
        elif node.height > node.width * 1.5:
            split_vertically = False

        if split_vertically:
            # 垂直分割 (左右に分ける)
            if node.width < self.min_size * 2:
                return # 幅が最小値x2 未満であれば分割不可
            
            # 分割幅は最小値を考慮しつつランダムに決定
            split_x = random.randint(self.min_size, node.width - self.min_size)
            # 分割後の子ノードを作成
            node.left = Node(node.x, node.y, split_x, node.height)
            node.right = Node(node.x + split_x, node.y, node.width - split_x, node.height)
        else:
            # 水平分割 (上下に分ける)
            if node.height < self.min_size * 2:
                return # 高さが最小値x2 未満であれば分割不可
            
            split_y = random.randint(self.min_size, node.height - self.min_size)
            node.left = Node(node.x, node.y, node.width, split_y)
            node.right = Node(node.x, node.y + split_y, node.width, node.height - split_y)

        # 子ノードも再帰的に分割
        self._split_node(node.left, depth - 1)
        self._split_node(node.right, depth - 1)

    def _create_rooms_and_corridors(self, node):
        """部屋と通路を作成する"""
        if node.left and node.right:
            # 子ノードがある場合、再帰的に処理
            self._create_rooms_and_corridors(node.left)
            self._create_rooms_and_corridors(node.right)
            
            # 左右のノードを繋ぐ通路を作成
            self._create_corridor(node.left, node.right)
        else:
            # リーフノードの場合、部屋を作成
            self._create_room(node)

    def _create_room(self, node):
        """区画内にランダムな部屋を作成"""
        # 区画のサイズ内でランダムな部屋のサイズと位置を決定
        # マージンを持たせて壁と隣接しすぎないようにする
        w = random.randint(self.min_room_size, max(self.min_room_size, node.width - 2))
        h = random.randint(self.min_room_size, max(self.min_room_size, node.height - 2))
        x = node.x + random.randint(1, max(1, node.width - w - 1))
        y = node.y + random.randint(1, max(1, node.height - h - 1))
        
        node.room = (x, y, w, h)
        
        # マップデータに書き込み
        for i in range(y, y + h):
            for j in range(x, x + w):
                if 0 <= i < len(self.map_data) and 0 <= j < len(self.map_data[0]):
                    self.map_data[i][j] = TILE_FLOOR

    def _create_corridor(self, node1, node2):
        """2つのノード（の中心）を繋ぐ通路を作成"""
        x1, y1 = node1.center()
        x2, y2 = node2.center()
        
        # L字型の通路を作成
        # 水平移動 -> 垂直移動
        if random.choice([True, False]):
            self._h_corridor(x1, x2, y1)
            self._v_corridor(y1, y2, x2)
        else:
            self._v_corridor(y1, y2, x1)
            self._h_corridor(x1, x2, y2)

    def _h_corridor(self, x1, x2, y):
        """水平方向の通路"""
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if 0 <= y < len(self.map_data) and 0 <= x < len(self.map_data[0]):
                self.map_data[y][x] = TILE_FLOOR

    def _v_corridor(self, y1, y2, x):
        """垂直方向の通路"""
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if 0 <= y < len(self.map_data) and 0 <= x < len(self.map_data[0]):
                self.map_data[y][x] = TILE_FLOOR
