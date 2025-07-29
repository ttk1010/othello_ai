"""
オセロAI テスト・デモ用スクリプト
Google Colab以外の環境でAIの動作確認を行う
"""

from othello_utils import create_initial_board, print_board, can_place_x_y, move_stone, count_stones, is_game_over
from myai import myai_greedy_simple, myai_positional, myai_strategic


def demo_ai_vs_ai(ai1, ai2, ai1_name="AI1", ai2_name="AI2", board_size=6):
    """
    AI同士の対戦デモ

    Args:
        ai1: 先手AI関数（黒）
        ai2: 後手AI関数（白）
        ai1_name: 先手AIの名前
        ai2_name: 後手AIの名前
        board_size: ボードサイズ
    """
    print(f"=== {ai1_name} vs {ai2_name} ===")
    board = create_initial_board(board_size)
    current_player = 1  # 黒から開始
    move_count = 0

    print("初期盤面:")
    print_board(board)
    print()

    while not is_game_over(board) and move_count < 100:  # 無限ループ防止
        # 現在のプレイヤーが置ける場所があるかチェック
        has_moves = any(can_place_x_y(board, current_player, x, y)
                       for y in range(len(board))
                       for x in range(len(board[0])))

        if has_moves:
            # AI関数を呼び出し
            if current_player == 1:
                x, y = ai1(board, current_player)
                player_name = ai1_name
            else:
                x, y = ai2(board, current_player)
                player_name = ai2_name

            # 手を実行
            if can_place_x_y(board, current_player, x, y):
                move_stone(board, current_player, x, y)
                print(f"{player_name}（{'●' if current_player == 1 else '○'}）: ({x}, {y})")
                move_count += 1

                # 5手ごとに盤面表示
                if move_count % 5 == 0:
                    print_board(board)
                    black, white = count_stones(board)
                    print(f"石数 - 黒: {black}, 白: {white}")
                    print()
            else:
                print(f"警告: {player_name}が無効な手を選択 ({x}, {y})")
        else:
            print(f"{current_player}（{'●' if current_player == 1 else '○'}）はパス")

        # プレイヤー交代
        current_player = 3 - current_player

    # 最終結果
    print("最終盤面:")
    print_board(board)
    black, white = count_stones(board)
    print(f"最終結果 - 黒: {black}, 白: {white}")

    if black > white:
        print(f"勝者: {ai1_name}（黒）")
    elif white > black:
        print(f"勝者: {ai2_name}（白）")
    else:
        print("引き分け")
    print("=" * 40)
    print()


def test_single_ai(ai_func, ai_name="AI"):
    """
    単一AIの動作テスト

    Args:
        ai_func: テストするAI関数
        ai_name: AIの名前
    """
    print(f"=== {ai_name} 動作テスト ===")
    board = create_initial_board(6)

    print("テスト盤面:")
    print_board(board)

    # 黒番での手を取得
    x, y = ai_func(board, 1)
    print(f"{ai_name}が選択した手: ({x}, {y})")

    if can_place_x_y(board, 1, x, y):
        move_stone(board, 1, x, y)
        print("手を実行後:")
        print_board(board)
        print("✓ 有効な手でした")
    else:
        print("✗ 無効な手でした")

    print("=" * 30)
    print()


def main():
    """メイン関数"""
    print("オセロAI テスト・デモ")
    print("=" * 50)

    # 個別AIテスト
    print("1. 個別AI動作テスト")
    test_single_ai(myai_greedy_simple, "基本AI")
    test_single_ai(myai_positional, "位置評価AI")
    test_single_ai(myai_strategic, "戦略的AI")

    # AI対戦デモ
    print("2. AI対戦デモ")
    demo_ai_vs_ai(myai_greedy_simple, myai_positional, "基本AI", "位置評価AI")
    demo_ai_vs_ai(myai_positional, myai_strategic, "位置評価AI", "戦略的AI")


if __name__ == "__main__":
    main()
