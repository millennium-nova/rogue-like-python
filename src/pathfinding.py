import heapq
from src.settings import TILE_WALL

def find_path(start, goal, map_data):
    """
    A*アルゴリズムを使用してスタートからゴールまでの最短経路を計算する。
    
    Args:
        start (tuple): スタート地点のタイル座標 (x, y)
        goal (tuple): ゴール地点のタイル座標 (x, y)
        map_data (list[list[int]]): マップデータ (0: 床, 1: 壁)
        
    Returns:
        list[tuple] or None: 経路の座標リスト [(x1, y1), (x2, y2), ...]、
                            経路が見つからない場合は None
    """
    if start == goal:
        return []
    
    # マップのサイズ
    height = len(map_data)
    width = len(map_data[0]) if height > 0 else 0
    
    # スタートまたはゴールが壁の場合は経路なし
    if (map_data[start[1]][start[0]] == TILE_WALL or 
        map_data[goal[1]][goal[0]] == TILE_WALL):
        return None
    
    # ヒューリスティック関数（マンハッタン距離）
    def heuristic(pos):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
    
    # 優先度付きキュー: (f値, カウンター, 座標)
    open_set = []
    counter = 0
    heapq.heappush(open_set, (heuristic(start), counter, start))
    
    # 各ノードへの最小コスト
    g_score = {start: 0}
    
    # 各ノードの親（経路再構築用）
    came_from = {}
    
    # 訪問済みセット
    closed_set = set()
    
    # 移動方向（上下左右）
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while open_set:
        _, _, current = heapq.heappop(open_set)
        
        # ゴールに到達
        if current == goal:
            # 経路を再構築
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path
        
        if current in closed_set:
            continue
        
        closed_set.add(current)
        
        # 隣接ノードを探索
        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            nx, ny = neighbor
            
            # マップ範囲外チェック
            if not (0 <= nx < width and 0 <= ny < height):
                continue
            
            # 壁チェック
            if map_data[ny][nx] == TILE_WALL:
                continue
            
            # 訪問済みチェック
            if neighbor in closed_set:
                continue
            
            # 新しいg値
            tentative_g = g_score[current] + 1
            
            # より良い経路が見つかった場合
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor)
                counter += 1
                heapq.heappush(open_set, (f_score, counter, neighbor))
    
    # 経路が見つからない
    return None


def get_next_step(start, goal, map_data):
    """
    find_path を使用して、次の1歩だけを返す便利関数。
    
    Args:
        start (tuple): スタート地点のタイル座標 (x, y)
        goal (tuple): ゴール地点のタイル座標 (x, y)
        map_data (list[list[int]]): マップデータ
        
    Returns:
        tuple or None: 次に移動すべき座標 (x, y)、経路がない場合は None
    """
    path = find_path(start, goal, map_data)
    if path and len(path) > 0:
        return path[0]
    return None
