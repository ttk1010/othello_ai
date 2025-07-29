# オセロAI 自作関数集

このリポジトリは、プログラミング入門用のオセロAI開発において、自作のAI関数を管理するためのものである。

## 概要

[倉光君郎氏のnote記事](https://note.com/kkuramitsu/n/n15682979bfaa)「プログラミング入門は、オセロAIで仕上げ！」に基づいて作成された、複数種類のオセロAI実装を含んでいる。

## 実装されているAI

### 1. `myai()` - 基本AI
最も多くの石を取れる位置を選ぶシンプルなAI。
- **戦略**: 手を打った後の自分の石の総数が最大になる位置を選択
- **特徴**: 理解しやすく、実装が簡単

### 2. `myai_greedy()` - 貪欲AI
最も多くの石をひっくり返せる手を選ぶAI。
- **戦略**: その手でひっくり返せる石数が最大の位置を選択
- **特徴**: 即座の利益を最大化する短期思考

### 3. `myai_positional()` - 位置評価AI（推奨）
角や辺などの重要な位置を考慮した戦略的AI。
- **戦略**: 位置の価値とひっくり返る石数の両方を評価
- **特徴**: 
  - 6x6・8x8両対応の評価表を使用
  - 角（120点）、辺（20点）、危険地帯（-20〜-40点）などの定石を反映
  - 総合スコア = 位置価値 + ひっくり返る石数 × 10

## 使用方法

### Google Colabでの環境準備

このオセロAIは **Google Colab** 上での実行を前提としている。以下の手順で環境を準備する：

```python
# 1. 演習用コードのクローン
!git clone https://github.com/kkuramitsu/sakura.git

# 2. 自作AIパッケージをクローン
!git clone https://github.com/ttk1010/othello_ai.git

# 3. 必要なモジュールのインポート
from sakura import othello
from sakura.othello import *
from othello_ai import myai, myai_greedy, myai_positional
```

### 基本的な使い方
```python
# デフォルトAI（位置評価AI）を使用
othello.play(myai)
```

### 特定のAIを指定
```python
# 貪欲AIを使用
othello.play(myai_greedy)

# 位置評価AIを使用
othello.play(myai_positional)
```

### AIの性能テスト
```python
# AI同士を対戦させる
othello.run(myai_greedy, myai_positional)
```

**注意事項:**
- このプログラムはGoogle Colab上でのみ動作する
- 人間は先手（黒）、AIは後手（白）として対戦する
- 黒を置きたい場所をクリックして操作する

## AI関数の仕様

すべてのAI関数は以下の仕様に従っている：

**入力:**
- `board`: 2次元配列（6x6 または 8x8）
  - `0`: 空きマス
  - `1`: 黒石（BLACK）
  - `2`: 白石（WHITE）
- `color`: 自分の色（`1` = 黒、`2` = 白）

**出力:**
- `(column, row)`: 置く位置のタプル（x, y座標）

## ファイル構成

- `myai.py`: 各種AI実装
- `__init__.py`: パッケージ初期化ファイル（AI関数のエクスポート）
- `README.md`: このファイル

## 評価表について

位置評価AIで使用している評価表は以下の考え方に基づいている：

- **角（120点）**: 最も価値が高い。一度取られると取り返せない
- **辺（20点）**: 比較的安全で価値が高い
- **角の隣（-20〜-40点）**: 相手に角を取らせるリスクがあるため避けるべき
- **中央付近（3〜15点）**: 中程度の価値

## 今後の改良案

記事で紹介されている、より高度なAI開発のアプローチ：

1. **探索アルゴリズム**: ミニマックス法、アルファベータ法による先読み
2. **動的評価**: 局面（序盤・中盤・終盤）に応じた評価関数の切り替え
3. **機械学習**: 深層学習やTransformerを用いた学習型AI
4. **強化学習**: 自己対戦による学習

## 参考資料

- [プログラミング入門は、オセロAIで仕上げ！](https://note.com/kkuramitsu/n/n15682979bfaa)
- [演習用コード（GitHub）](https://github.com/kkuramitsu/sakura.git)
