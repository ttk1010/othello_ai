"""
オセロAI 自作関数集

このパッケージには複数種類のオセロAI実装が含まれています。

基本AI群:
- myai_greedy_simple: 基本AI（石数最大化）
- myai_greedy_flip: 貪欲AI（ひっくり返し数最大化）
- myai_positional: 位置評価AI

高度AI群（ミニマックス法）:
- myai_minimax_shallow: 浅い探索AI（深さ3）
- myai_minimax_deep: 深い探索AI（深さ5）
- myai_adaptive_depth: 適応的探索AI
- myai_strategic: 戦略的AI（最強）

エイリアス:
- myai: myai_positional（サイト互換性用）
- myai_default: myai_positional
ユーティリティ:
- othello_utils: オセロゲームの基本関数群
"""

# 依存関数の処理
try:
    # sakura.othelloがある場合は何もしない
    from sakura.othello import can_place_x_y, move_stone, copy
    _SAKURA_AVAILABLE = True
except ImportError:
    # othello_utilsを使用
    from . import othello_utils
    _SAKURA_AVAILABLE = False

from .myai import (
    # 基本AI群
    myai_greedy_simple,
    myai_greedy_flip,
    myai_positional,
    myai_default,

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
    minimax
)

__version__ = "2.1.0"
__author__ = "ttk1010"

# デフォルトのAI関数をパッケージレベルで公開
__all__ = [
    # 基本AI群
    'myai_greedy_simple',
    'myai_greedy_flip',
    'myai_positional',
    'myai_default',

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
    'minimax'
]

# sakuraが利用できない場合はothello_utilsも公開
if not _SAKURA_AVAILABLE:
    __all__.append('othello_utils')
