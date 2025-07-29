"""
オセロゲームの基本関数群
sakura.othelloモジュールに依存している関数をローカル実装
"""

def can_place_x_y(board, stone, x, y):
    """
    指定位置に石を置けるかチェック

    Args:
        board: 2次元配列のオセロボード
        stone: 石の色 (BLACK=1, WHITE=2)
        x: 列位置
        y: 行位置

    Returns:
        bool: 置けるならTrue
    """
    if board[y][x] != 0:
        return False  # 既に石がある場合は置けない

    opponent = 3 - stone  # 相手の石 (1なら2、2なら1)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            found_opponent = True

        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True  # 石を置ける条件を満たす

    return False


def move_stone(board, stone, x, y):
    """
    指定位置に石を置き、相手の石をひっくり返す

    Args:
        board: 2次元配列のオセロボード（破壊的変更）
        stone: 石の色 (BLACK=1, WHITE=2)
        x: 列位置
        y: 行位置
    """
    moves = [copy(board)]*3
    if not can_place_x_y(board, stone, x, y):
        return moves  # 置けない場合は何もしない

    board[y][x] = stone  # 石を置く
    moves.append(copy(board))
    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    flipped_count = 0

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        stones_to_flip = []

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            stones_to_flip.append((nx, ny))
            nx += dx
            ny += dy

        if stones_to_flip and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            for flip_x, flip_y in stones_to_flip:
                board[flip_y][flip_x] = stone
                moves.append(copy(board))
                flipped_count += 1

    return moves


def copy(board):
    """
    ボードのディープコピーを作成

    Args:
        board: 2次元配列のオセロボード

    Returns:
        コピーされたボード
    """
    return [row[:] for row in board]


def print_board(board):
    """
    ボードを見やすく表示（デバッグ用）

    Args:
        board: 2次元配列のオセロボード
    """
    symbols = {0: '.', 1: '●', 2: '○'}
    print('  ' + ' '.join(str(i) for i in range(len(board[0]))))
    for i, row in enumerate(board):
        print(f'{i} ' + ' '.join(symbols[cell] for cell in row))


def count_stones(board):
    """
    盤面の石数をカウント

    Args:
        board: 2次元配列のオセロボード

    Returns:
        tuple: (黒石数, 白石数)
    """
    black_count = sum(row.count(1) for row in board)
    white_count = sum(row.count(2) for row in board)
    return black_count, white_count


def is_game_over(board):
    """
    ゲーム終了判定

    Args:
        board: 2次元配列のオセロボード

    Returns:
        bool: ゲーム終了ならTrue
    """
    # 両プレイヤーとも置ける場所がない場合
    black_moves = any(can_place_x_y(board, 1, x, y)
                     for y in range(len(board))
                     for x in range(len(board[0])))
    white_moves = any(can_place_x_y(board, 2, x, y)
                     for y in range(len(board))
                     for x in range(len(board[0])))

    return not (black_moves or white_moves)


def create_initial_board(size=6):
    """
    初期ボードを作成

    Args:
        size: ボードサイズ（6または8）

    Returns:
        初期状態のボード
    """
    board = [[0 for _ in range(size)] for _ in range(size)]
    center = size // 2

    # 中央4マスに初期配置
    board[center-1][center-1] = 2  # 白
    board[center-1][center] = 1    # 黒
    board[center][center-1] = 1    # 黒
    board[center][center] = 2      # 白

    return board
