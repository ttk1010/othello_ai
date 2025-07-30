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
    "6x6": {
        "beginning": [
            # 序盤：隅を最重要視、隅隣接を強く避ける、石を多く取らない戦略
            [-1, -45, -11, -11, -45, -1],
            [-45, -25, -15, -15, -25, -45],
            [-11, -15, -3, -3, -15, -11],
            [-11, -15, -3, -3, -15, -11],
            [-45, -25, -15, -15, -25, -45],
            [-1, -45, -11, -11, -45, -1]
        ],
        "midgame": [
            # 中盤：隅の重要性を保ちつつ、辺の価値を上げる
            [-1, -30, -8, -8, -30, -1],
            [-30, -20, -10, -10, -20, -30],
            [-8, -10, -5, -5, -10, -8],
            [-8, -10, -5, -5, -10, -8],
            [-30, -20, -10, -10, -20, -30],
            [-1, -30, -8, -8, -30, -1]
        ],
        "endgame": [
            # 終盤：石数重視、隅の重要性は相対的に下がる
            [-1, -15, -5, -5, -15, -1],
            [-15, -10, -7, -7, -10, -15],
            [-5, -7, -8, -8, -7, -5],
            [-5, -7, -8, -8, -7, -5],
            [-15, -10, -7, -7, -10, -15],
            [-1, -15, -5, -5, -15, -1]
        ],
    },
    "8x8": {
        "beginning": [
            # 序盤：隅の価値を最大化、隅隣接を避ける
            [-1, -50, -15, -8, -8, -15, -50, -1],
            [-50, -35, -20, -12, -12, -20, -35, -50],
            [-15, -20, -5, -3, -3, -5, -20, -15],
            [-8, -12, -3, -2, -2, -3, -12, -8],
            [-8, -12, -3, -2, -2, -3, -12, -8],
            [-15, -20, -5, -3, -3, -5, -20, -15],
            [-50, -35, -20, -12, -12, -20, -35, -50],
            [-1, -50, -15, -8, -8, -15, -50, -1]
        ],
        "midgame": [
            # 中盤：バランス調整、辺の価値向上
            [-1, -35, -10, -6, -6, -10, -35, -1],
            [-35, -25, -15, -8, -8, -15, -25, -35],
            [-10, -15, -4, -2, -2, -4, -15, -10],
            [-6, -8, -2, -1, -1, -2, -8, -6],
            [-6, -8, -2, -1, -1, -2, -8, -6],
            [-10, -15, -4, -2, -2, -4, -15, -10],
            [-35, -25, -15, -8, -8, -15, -25, -35],
            [-1, -35, -10, -6, -6, -10, -35, -1]
        ],
        "endgame": [
            # 終盤：石数重視、位置による差を小さく
            [-1, -20, -7, -4, -4, -7, -20, -1],
            [-20, -15, -10, -6, -6, -10, -15, -20],
            [-7, -10, -6, -4, -4, -6, -10, -7],
            [-4, -6, -4, -3, -3, -4, -6, -4],
            [-4, -6, -4, -3, -3, -4, -6, -4],
            [-7, -10, -6, -4, -4, -6, -10, -7],
            [-20, -15, -10, -6, -6, -10, -15, -20],
            [-1, -20, -7, -4, -4, -7, -20, -1]
        ],
    }
}


def get_eval_table(board, game_phase="beginning"):
    """
    ボードサイズと局面に応じた評価表を取得

    Args:
        board: 2次元配列のオセロボード
        game_phase: 'beginning', 'midgame', 'endgame'

    Returns:
        評価表（2次元配列）
    """
    size = f"{len(board)}x{len(board[0])}"

    if size in EVAL_TABLES and game_phase in EVAL_TABLES[size]:
        return EVAL_TABLES[size][game_phase]
    else:
        # デフォルト値
        return EVAL_TABLES["6x6"]["beginning"]


def count_stable_stones(board, color):
    """
    確定石（二度とひっくり返されない石）の数を数える

    Args:
        board: 2次元配列のオセロボード
        color: 石の色

    Returns:
        確定石の数
    """
    stable_count = 0
    rows, cols = len(board), len(board[0])

    # 隅から始まる確定石をチェック
    corners = [(0, 0), (0, cols-1), (rows-1, 0), (rows-1, cols-1)]

    for corner_y, corner_x in corners:
        if board[corner_y][corner_x] == color:
            stable_count += 1

            # 隅から連続する同色の石を確定石として扱う（簡易版）
            # 実際の確定石判定はより複雑だが、ここでは簡略化

            # 縦方向の確定石
            for y in range(1, rows):
                if corner_y == 0:  # 上の隅から下へ
                    if board[y][corner_x] == color:
                        stable_count += 1
                    else:
                        break
                else:  # 下の隅から上へ
                    if board[rows-1-y][corner_x] == color:
                        stable_count += 1
                    else:
                        break

            # 横方向の確定石
            for x in range(1, cols):
                if corner_x == 0:  # 左の隅から右へ
                    if board[corner_y][x] == color:
                        stable_count += 1
                    else:
                        break
                else:  # 右の隅から左へ
                    if board[corner_y][cols-1-x] == color:
                        stable_count += 1
                    else:
                        break

    return stable_count


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
    eval_table = get_eval_table(board)

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


def myai_positional_improved(board, color):
    """
    改良版位置評価AI：段階別評価表 + 確定石考慮
    サイトの知見を基に実装：
    - 負の評価値で「石を多く取らない」戦略
    - 序盤・中盤・終盤で評価表を切り替え
    - 確定石の数も考慮

    Args:
        board: 2次元配列のオセロボード
        color: 自分の色 (BLACK=1, WHITE=2)

    Returns:
        (column, row): 評価値が最も高い位置
    """
    # ゲーム進行度を判定
    total_stones = sum(row.count(1) + row.count(2) for row in board)
    total_cells = len(board) * len(board[0])
    progress = total_stones / total_cells

    # 局面に応じた評価表を取得
    if progress < 0.25:
        eval_table = get_eval_table(board, "beginning")
        flip_weight = 5   # 序盤：石を取りすぎない
    elif progress < 0.75:
        eval_table = get_eval_table(board, "midgame")
        flip_weight = 8   # 中盤：バランス
    else:
        eval_table = get_eval_table(board, "endgame")
        flip_weight = 15  # 終盤：石数重視

    best_score = float('-inf')
    best_move = None

    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, color, x, y):
                # 手を試してみる
                test_board = copy(board)
                original_count = sum(row.count(color) for row in test_board)
                move_stone(test_board, color, x, y)
                new_count = sum(row.count(color) for row in test_board)
                flip_count = new_count - original_count - 1

                # 位置評価（負の値なので、石が少ないほど良い）
                position_value = eval_table[y][x]

                # 確定石の評価
                my_stable = count_stable_stones(test_board, color)
                opponent_stable = count_stable_stones(test_board, 3 - color)
                stable_diff = my_stable - opponent_stable

                # 総合評価（サイトの考え方に基づく）
                # 1. 位置評価（負の値）
                # 2. ひっくり返る石数（序盤は少ない方が良い）
                # 3. 確定石の差（多い方が良い）
                if progress < 0.5:
                    # 序盤～中盤：石を取りすぎない戦略
                    total_score = position_value - flip_count * flip_weight + stable_diff * 50
                else:
                    # 終盤：石数も重要
                    stone_diff = sum(row.count(color) for row in test_board) - sum(row.count(3-color) for row in test_board)
                    total_score = position_value + flip_count * flip_weight + stable_diff * 30 + stone_diff * 10

                if total_score > best_score:
                    best_score = total_score
                    best_move = (x, y)

    return best_move if best_move else (0, 0)


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
