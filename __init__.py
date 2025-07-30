"""
オセロAI 自作関数集

このパッケージには複数種類のオセロAI実装が含まれています。

基本AI群:
- myai_greedy_simple: 基本AI（石数最大化）
- myai_greedy_flip: 貪欲AI（ひっくり返し数最大化）
- myai_positional: 位置評価AI
- myai_positional_improved: 改良版位置評価AI（局面別評価表+確定石考慮）

高度AI群（ミニマックス法）:
- myai_minimax_shallow: 浅い探索AI（深さ3）
- myai_minimax_deep: 深い探索AI（深さ5）
- myai_adaptive_depth: 適応的探索AI
- myai_strategic: 戦略的AI（最強）

エイリアス:
- myai: myai_positional（サイト互換性用）

内部関数:
- evaluate_board: ボード評価関数
- get_valid_moves: 有効な手を取得
- minimax: ミニマックス探索関数
- count_stable_stones: 確定石カウント関数
- get_eval_table: 局面別評価表取得関数
"""

from .myai import (
    # 基本AI群
    myai_greedy_simple,
    myai_greedy_flip,
    myai_positional,
    myai_positional_improved,

    # 高度AI群
    myai_minimax_shallow,
    myai_minimax_deep,
    myai_adaptive_depth,
    myai_strategic,

    # エイリアス
    myai,
    myai_best,

    # 内部関数（上級者用）
    evaluate_board,
    get_valid_moves,
    minimax,
    count_stable_stones,
    get_eval_table,
)

__version__ = "2.3.0"
__author__ = "ttk1010"

# デフォルトのAI関数をパッケージレベルで公開
__all__ = [
    # 基本AI群
    'myai_greedy_simple',
    'myai_greedy_flip',
    'myai_positional',
    'myai_positional_improved',

    # 高度AI群
    'myai_minimax_shallow',
    'myai_minimax_deep',
    'myai_adaptive_depth',
    'myai_strategic',

    # エイリアス
    'myai',
    'myai_best',

    # 内部関数
    'evaluate_board',
    'get_valid_moves',
    'minimax',
    'count_stable_stones',
    'get_eval_table',
]
