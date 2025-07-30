"""
オセロAI関数集

このモジュールには複数種類のオセロAI実装が含まれています。
依存関係: othello_utils.py または sakura.othello モジュール
"""

# 依存関数のインポート
try:
    # sakura.othelloがある場合（Google Colab環境）
    from sakura.othello import can_place_x_y, move_stone, copy
except ImportError:
    try:
        # ローカルのothello_utilsがある場合
        from .othello_utils import can_place_x_y, move_stone, copy
    except ImportError:
        # 同じディレクトリのothello_utilsがある場合
        from othello_utils import can_place_x_y, move_stone, copy


# 評価表
EVAL_TABLES = {
    "6x6": [
            [100, -20,  10,  10, -20, 100],
            [-20, -30,   2,   2, -30, -20],
            [ 10,   2,   5,   5,   2,  10],
            [ 10,   2,   5,   5,   2,  10],
            [-20, -30,   2,   2, -30, -20],
            [100, -20,  10,  10, -20, 100]
        ],
    "8x8": [
            [120, -20,  20,   5,   5,  20, -20, 120],
            [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
            [ 20,  -5,  15,   3,   3,  15,  -5,  20],
            [  5,  -5,   3,   3,   3,   3,  -5,   5],
            [  5,  -5,   3,   3,   3,   3,  -5,   5],
            [ 20,  -5,  15,   3,   3,  15,  -5,  20],
            [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
            [120, -20,  20,   5,   5,  20, -20, 120]
        ]
    }


def get_eval_table(board):
    """ボードサイズに応じた評価表を取得"""
    size = f"{len(board)}x{len(board[0])}"
    return EVAL_TABLES.get(size, EVAL_TABLES["6x6"])  # デフォルトは6x6


def myai_greedy_simple(board, color):
    """
    最も多くの石を取れる位置を選ぶオセロAI

    Args:
        board: 2次元配列のオセロボード
        color: 自分の色 (BLACK=1, WHITE=2)

    Returns:
        (column, row): 最も多くの石が取れる位置
    """
    best_score = -1
    best_move = None

    # すべての可能な位置をチェック
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, color, x, y):
                # この位置に置いた場合の石数を計算
                test_board = copy(board)
                move_stone(test_board, color, x, y)

                # 自分の石の数を数える
                my_stones = sum(row.count(color) for row in test_board)

                # より多くの石を取れる手があれば更新
                if my_stones > best_score:
                    best_score = my_stones
                    best_move = (x, y)

    return best_move if best_move else (0, 0)


def myai_greedy_flip(board, color):
    """
    貪欲AI: 最も多くの石をひっくり返せる手を選ぶ

    Args:
        board: 2次元配列のオセロボード
        color: 自分の色 (BLACK=1, WHITE=2)

    Returns:
        (column, row): 最も多くの石をひっくり返せる位置
    """
    best_flip_count = -1
    best_move = None

    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, color, x, y):
                # この位置に置いた場合にひっくり返る石数を計算
                test_board = copy(board)
                original_count = sum(row.count(color) for row in test_board)
                move_stone(test_board, color, x, y)
                new_count = sum(row.count(color) for row in test_board)
                flip_count = new_count - original_count - 1  # 置いた石を除く

                if flip_count > best_flip_count:
                    best_flip_count = flip_count
                    best_move = (x, y)

    return best_move if best_move else (0, 0)


def myai_positional(board, color):
    """
    位置評価AI: 角や辺などの価値の高い位置を優先する

    Args:
        board: 2次元配列のオセロボード
        color: 自分の色 (BLACK=1, WHITE=2)

    Returns:
        (column, row): 評価値が最も高い位置
    """
    eval_table = EVAL_TABLES["6x6"] if len(board) == 6 else EVAL_TABLES["8x8"]

    best_score = float('-inf')
    best_move = None

    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, color, x, y):
                # 位置の評価値を取得
                position_value = eval_table[y][x]

                # ひっくり返る石数も考慮
                test_board = copy(board)
                original_count = sum(row.count(color) for row in test_board)
                move_stone(test_board, color, x, y)
                new_count = sum(row.count(color) for row in test_board)
                flip_count = new_count - original_count - 1

                # 総合スコア = 位置価値 + ひっくり返る石数
                total_score = position_value + flip_count * 10

                if total_score > best_score:
                    best_score = total_score
                    best_move = (x, y)

    return best_move if best_move else (0, 0)


myai = myai_positional


def evaluate_board(board, color):
    """
    盤面を評価する関数

    Args:
        board: 2次元配列のオセロボード
        color: 評価する色 (BLACK=1, WHITE=2)

    Returns:
        評価値（数値が大きいほど有利）
    """
    weights = get_eval_table(board)

    opponent = 3 - color
    score = 0

    # 位置評価
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == color:
                score += weights[y][x]
            elif board[y][x] == opponent:
                score -= weights[y][x]

    # 石数の差（終盤重視）
    my_stones = sum(row.count(color) for row in board)
    opponent_stones = sum(row.count(opponent) for row in board)
    stone_diff = my_stones - opponent_stones

    # 盤面の埋まり具合で重みを調整
    total_stones = my_stones + opponent_stones
    total_cells = len(board) * len(board[0])
    game_progress = total_stones / total_cells

    # 序盤は位置重視、終盤は石数重視
    if game_progress < 0.7:
        return score + stone_diff * 5  # 序盤：位置重視
    else:
        return score + stone_diff * 20  # 終盤：石数重視


def get_valid_moves(board, color):
    """
    有効な手の一覧を取得

    Args:
        board: 2次元配列のオセロボード
        color: プレイヤーの色

    Returns:
        有効な手のリスト [(x, y), ...]
    """
    moves = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, color, x, y):
                moves.append((x, y))
    return moves


def minimax(board, depth, maximizing_player, color, alpha=float('-inf'), beta=float('inf')):
    """
    アルファベータ剪定付きミニマックス法

    Args:
        board: 現在の盤面
        depth: 探索の深さ
        maximizing_player: 最大化プレイヤーかどうか
        color: 現在のプレイヤーの色
        alpha: アルファ値（アルファベータ剪定用）
        beta: ベータ値（アルファベータ剪定用）

    Returns:
        (評価値, 最適手)
    """
    # 終了条件：深さ0または有効手なし
    if depth == 0:
        return evaluate_board(board, color if maximizing_player else 3 - color), None

    current_color = color if maximizing_player else 3 - color
    valid_moves = get_valid_moves(board, current_color)

    if not valid_moves:
        # パスする場合
        opponent_moves = get_valid_moves(board, 3 - current_color)
        if not opponent_moves:
            # ゲーム終了
            return evaluate_board(board, color if maximizing_player else 3 - color), None
        else:
            # 相手のターン
            eval_score, _ = minimax(board, depth - 1, not maximizing_player, color, alpha, beta)
            return eval_score, None

    best_move = None

    if maximizing_player:
        max_eval = float('-inf')
        for move in valid_moves:
            x, y = move
            # 手を試す
            test_board = copy(board)
            move_stone(test_board, current_color, x, y)

            eval_score, _ = minimax(test_board, depth - 1, False, color, alpha, beta)

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

            # アルファベータ剪定
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break

        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in valid_moves:
            x, y = move
            # 手を試す
            test_board = copy(board)
            move_stone(test_board, current_color, x, y)

            eval_score, _ = minimax(test_board, depth - 1, True, color, alpha, beta)

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

            # アルファベータ剪定
            beta = min(beta, eval_score)
            if beta <= alpha:
                break

        return min_eval, best_move


def myai_minimax_shallow(board, color):
    """
    浅い探索（深さ3）のミニマックスAI
    計算が軽く、実用的な強さ

    Args:
        board: 2次元配列のオセロボード
        color: 自分の色 (BLACK=1, WHITE=2)

    Returns:
        (column, row): 最適手
    """
    _, best_move = minimax(board, 3, True, color)
    return best_move if best_move else (0, 0)


def myai_minimax_deep(board, color):
    """
    深い探索（深さ5）のミニマックスAI
    より強いが計算時間がかかる

    Args:
        board: 2次元配列のオセロボード
        color: 自分の色 (BLACK=1, WHITE=2)

    Returns:
        (column, row): 最適手
    """
    _, best_move = minimax(board, 5, True, color)
    return best_move if best_move else (0, 0)


def myai_adaptive_depth(board, color):
    """
    適応的深さのミニマックスAI
    ゲームの進行状況に応じて探索深度を調整

    Args:
        board: 2次元配列のオセロボード
        color: 自分の色 (BLACK=1, WHITE=2)

    Returns:
        (column, row): 最適手
    """
    # 盤面の埋まり具合を計算
    total_stones = sum(row.count(1) + row.count(2) for row in board)
    total_cells = len(board) * len(board[0])
    game_progress = total_stones / total_cells

    # 有効手の数を計算
    valid_moves = get_valid_moves(board, color)
    move_count = len(valid_moves)

    # 探索深度を動的に決定
    if game_progress < 0.3:
        # 序盤：浅く探索（選択肢が多いため）
        depth = 3
    elif game_progress < 0.7:
        # 中盤：中程度の探索
        depth = 4
    else:
        # 終盤：深く探索（重要な局面）
        if move_count <= 5:
            depth = 6  # 選択肢が少ない場合は深く
        else:
            depth = 5

    _, best_move = minimax(board, depth, True, color)
    return best_move if best_move else (0, 0)


def myai_strategic(board, color):
    """
    戦略的AI：序盤は位置重視、中盤は探索、終盤は深い探索

    Args:
        board: 2次元配列のオセロボード
        color: 自分の色 (BLACK=1, WHITE=2)

    Returns:
        (column, row): 最適手
    """
    total_stones = sum(row.count(1) + row.count(2) for row in board)
    total_cells = len(board) * len(board[0])
    game_progress = total_stones / total_cells

    if game_progress < 0.2:
        # 序盤：位置評価重視
        return myai_positional(board, color)
    elif game_progress < 0.8:
        # 中盤：適応的探索
        return myai_adaptive_depth(board, color)
    else:
        # 終盤：深い探索で正確に読み切る
        return myai_minimax_deep(board, color)


myai_best = myai_strategic
