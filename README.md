# オセロAI 自作関数集

このリポジトリは、プログラミング入門用のオセロAI開発において、自作のAI関数を管理するためのものである。

## 概要

[倉光君郎氏のnote記事](https://note.com/kkuramitsu/n/n15682979bfaa)「プログラミング入門は、オセロAIで仕上げ！」に基づいて作成された、複数種類のオセロAI実装を含んでいる。

## 実装されているAI

### 基本AI群

#### 1. `myai_greedy_simple()` - 基本AI
最も多くの石を取れる位置を選ぶシンプルなAIである。
- **戦略**: 手を打った後の自分の石の総数が最大になる位置を選択
- **特徴**: 理解しやすく、実装が簡単

#### 2. `myai_greedy_flip()` - 貪欲AI
最も多くの石をひっくり返せる手を選ぶAIである。
- **戦略**: その手でひっくり返せる石数が最大の位置を選択
- **特徴**: 即座の利益を最大化する短期思考

#### 3. `myai_positional()` - 位置評価AI
角や辺などの重要な位置を考慮した戦略的AIである。
- **戦略**: 位置の価値とひっくり返る石数の両方を評価
- **特徴**:
  - 6x6・8x8両対応の評価表を使用
  - 角（120点）、辺（20点）、危険地帯（-20〜-40点）などの定石を反映
  - 総合スコア = 位置価値 + ひっくり返る石数 × 10

### 高度AI群（ミニマックス法）

#### 4. `myai_minimax_shallow()` - 浅い探索AI
深さ3のミニマックス法を使用した探索型AIである。
- **戦略**: 3手先まで読んで最適手を選択
- **特徴**: 計算が軽く、実用的な強さ
- **技術**: アルファベータ剪定で高速化

#### 5. `myai_minimax_deep()` - 深い探索AI
深さ5のミニマックス法を使用した強力なAIである。
- **戦略**: 5手先まで読んで最適手を選択
- **特徴**: より強いが計算時間がかかる
- **技術**: アルファベータ剪定で高速化

#### 6. `myai_adaptive_depth()` - 適応的探索AI
ゲームの進行状況に応じて探索深度を調整するAIである。
- **戦略**:
  - 序盤（〜30%）: 深さ3（選択肢が多いため浅く）
  - 中盤（30-70%）: 深さ4（バランス重視）
  - 終盤（70%〜）: 深さ5-6（重要な局面を深く読む）
- **特徴**: 計算効率と強さのバランスが最適

#### 7. `myai_strategic()` - 戦略的AI（最強）
ゲーム局面に応じて異なる戦略を使い分ける最高水準のAIである。
- **戦略**:
  - 序盤（〜20%）: 位置評価重視（`myai_positional`）
  - 中盤（20-80%）: 適応的探索（`myai_adaptive_depth`）
  - 終盤（80%〜）: 深い探索（`myai_minimax_deep`）
- **特徴**: 各局面で最適な戦略を自動選択

### エイリアス・デフォルト関数

- `myai`: `myai_positional`のエイリアス（サイト互換性用）
- `myai_default`: `myai_positional`のエイリアス
- `myai_best`: `myai_strategic`のエイリアス（最強AI）

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
from othello_ai import *  # すべてのAI関数をインポート
```

### 基本的な使い方
```python
# デフォルトAI（位置評価AI）を使用
othello.play(myai)

# 最強AI（戦略的AI）を使用
othello.play(myai_best)
```

### 特定のAIを指定
```python
# 基本AI群
othello.play(myai_greedy_simple)   # 基本AI
othello.play(myai_greedy_flip)     # 貪欲AI
othello.play(myai_positional)      # 位置評価AI

# 高度AI群（ミニマックス法）
othello.play(myai_minimax_shallow)  # 浅い探索（深さ3）
othello.play(myai_minimax_deep)     # 深い探索（深さ5）
othello.play(myai_adaptive_depth)   # 適応的探索
othello.play(myai_strategic)        # 戦略的AI（最強）
```

### AIの強さ比較
```python
# 弱いAI vs 強いAI
othello.run(myai_greedy_simple, myai_strategic)

# 中級AI vs 上級AI
othello.run(myai_positional, myai_minimax_deep)

# 異なる探索深度の比較
othello.run(myai_minimax_shallow, myai_minimax_deep)
```

**注意事項:**
- このプログラムはGoogle Colab上でのみ動作する
- 人間は先手（黒）、AIは後手（白）として対戦する
- 黒を置きたい場所をクリックして操作する

## 実装技術の解説

### ミニマックス法とは
**ミニマックス法**は、2人ゲームにおいて最適な手を見つけるための探索アルゴリズムである。

**基本原理:**
- 自分のターン: 評価値を**最大化**する手を選ぶ
- 相手のターン: 評価値を**最小化**する手を選ぶ（相手は自分にとって最悪の手を打つと仮定）
- 指定した深さまで再帰的に探索し、最終的な評価値を逆算

### アルファベータ剪定
**アルファベータ剪定**は、ミニマックス法の計算量を大幅に削減する最適化技術である。

**効果:**
- 探索する必要のない枝を早期に切り捨て
- 同じ結果を得ながら計算時間を大幅短縮
- 深い探索が実用的な時間で可能

### 適応的戦略
**ゲーム局面に応じた戦略切り替え**により、各段階で最適なアプローチを採用している。

**局面別戦略:**
- **序盤**: 位置価値重視（角や辺の確保）
- **中盤**: バランス型探索（位置と読みの両立）
- **終盤**: 深い探索（正確な読み切り）

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

- `myai.py`: 各種AI実装（メインファイル）
- `othello_utils.py`: オセロゲームの基本関数群（依存関数の実装）
- `__init__.py`: パッケージ初期化ファイル（AI関数のエクスポートと依存関係処理）
- `test_demo.py`: ローカル環境でのテスト・デモ用スクリプト
- `README.md`: このファイル

## 依存関係とアーキテクチャ

### 保守性重視の設計方針

このリポジトリは以下の方針で設計されている：

1. **依存関係の明確化**: sakura.othelloへの依存を明示
2. **フォールバック機能**: sakuraが利用できない場合の代替実装を提供
3. **独立性の確保**: 単体でも動作可能
4. **モジュール分離**: AI実装と基本関数を分離

### 動作モード

#### モード1: Google Colab（推奨）
```python
# sakura.othelloが利用できる場合
from sakura.othello import can_place_x_y, move_stone, copy
```

#### モード2: スタンドアロン
```python
# othello_utils.pyを使用する場合
from othello_utils import can_place_x_y, move_stone, copy
```

### インポート処理の仕組み

`myai.py`と`__init__.py`では以下の順序で依存関数を探す：

1. `sakura.othello`モジュール（Google Colab環境）
2. ローカルの`othello_utils.py`（スタンドアロン環境）
3. エラー処理とフォールバック

## ローカル環境でのテスト

Google Colab以外の環境でも動作確認できるように、テスト用スクリプトを提供している：

```python
# ローカル環境でのテスト実行
python test_demo.py
```

**テスト内容:**
- 各AI関数の動作確認
- AI同士の対戦デモ
- 盤面表示とゲーム進行の可視化

**利点:**
- デバッグが容易
- 開発環境での動作確認
- CI/CDパイプラインでの自動テスト

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
