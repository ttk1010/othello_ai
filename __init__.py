"""
オセロAI 自作関数集

このパッケージには複数種類のオセロAI実装が含まれています。
- myai: 基本AI（石数最大化）
- myai_greedy: 貪欲AI（ひっくり返し数最大化）
- myai_positional: 位置評価AI（推奨）
"""

from .myai import (
    myai,
    myai_greedy, 
    myai_positional,
    myai_default
)

__version__ = "1.0.0"
__author__ = "ttk1010"

# デフォルトのAI関数をパッケージレベルで公開
__all__ = [
    'myai',
    'myai_greedy',
    'myai_positional', 
    'myai_default'
]
