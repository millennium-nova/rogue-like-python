# Rogue-like Python

PythonとPygameを使用し、GitHub CopilotおよびGeminiを活用して制作したゲームです。
年末年始休暇の空き時間を利用して、「LLMを活用した短期間でのプロトタイピング」をテーマに制作しました。

![Demo](https://via.placeholder.com/800x450?text=Game+Screenshot)

## 開発の目的と背景
* **目的:** 生成AIを開発プロセスに組み込み、未知のアルゴリズム（BSP、A*）を含むゲームを短期間で形にすること。
* **開発期間:** 1週間
* **技術スタック:** Python 3.x, Pygame
* **開発ツール:** GitHub Copilot, Gemini, VS Code

## AI活用のプロセスと役割分担
本プロジェクトは、AIツールによるコード生成を主体として開発を行いました。

* **自身の役割 (Human):**
    * ゲームの仕様策定と要件定義
    * AIへのプロンプトエンジニアリング（詳細な指示出し）
    * 生成されたコードの動作確認、デバッグ、結合
    * ファイル構成やクラス設計の方針決定

* **AIの役割 (Copilot / Gemini):**
    * ダンジョン生成ロジック（BSP法）のコーディング
    * 経路探索アルゴリズム（A*法）の実装
    * Pygameを用いた描画処理のボイラープレート記述

## 実装機能と技術的アプローチ

### 1. 手続き型ダンジョン生成
マップ生成には、BSP (二分空間分割法) を採用しました。
Geminiに対して「部屋が重ならないように分割し、それらを通路で繋ぐ」という支持を与えました。

### 2. 敵キャラクターの追跡AI
敵が壁を避けてプレイヤーを追尾する機能には、A*アルゴリズムを使用しました。
複雑な経路探索ロジックはCopilotに記述してもらいました。

### 3. オブジェクト指向設計
AIが生成しやすいよう、機能ごとにファイルを分割して管理しました。
* `dungeon.py`: マップ生成ロジック
* `entities.py`: キャラクターのステータス管理
* `game.py`: ゲームループとイベント処理

## インストールと実行方法

```bash
git clone [https://github.com/あなたのID/rogue-like-python.git](https://github.com/あなたのID/rogue-like-python.git)
cd rogue-like-python
pip install -r requirements.txt
python main.py