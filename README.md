# Fractal Dimension Analyzer for Calligraphy 🖋️📐

ボックスカウント法（Box-counting method）を用いて、画像（書道やフォント）のフラクタル次元を自動算出し、比較・解析するためのツールです。

## 🌟 主な機能
- **自動正規化**: アスペクト比を維持したまま、指定サイズ（`IMG_SIZE` 定数で変更可能）のキャンバスにリサイズし、中央に配置します。
- **大津の2値化 (Otsu's Method)**: 画像の明るさを解析し、主観を排除した最適な閾値で白黒に変換します。
- **マスター分析シートの自動生成**: フォントと肉筆（国名など）のデータを統合し、同じ文字ごとに数値を横並びで比較できる `master_analysis.csv` を自動で更新します。
- **学術的指標の算出**: フラクタル次元 ($D$) だけでなく、近似直線の決定係数 ($R^2$) や、パターンの密度（Density）も同時に記録します。
- **効率的なフォルダ処理**: 処理済みフォルダを `closed_folder.log` に記録し、次回実行時に自動でスキップします。

## 📂 ディレクトリ構成
解析したい画像を `data/` 配下の各カテゴリフォルダに入れるだけで、自動的に分類して処理されます。

```text
📦 fractal-dimension
 ┣ 📜 box_counting.py         # メインプログラム
 ┣ 📜 .gitignore              # Git管理除外設定
 ┣ 📜 README.md               # このファイル
 ┣ 📜 closed_folder.log       # 処理済みフォルダの記録（自動生成）
 ┣ 📂 data/                   # 入力画像フォルダ
 ┃  ┣ 📂 calligraphy/         # 肉筆データ (例: Japan, China)
 ┃  ┗ 📂 fonts/               # フォントデータ (例: Meiryo, Yuumeicho)
 ┗ 📂 results/                # 解析結果（自動生成）
    ┣ 📜 master_analysis.csv  # 【分析用】全データの横並び比較表
    ┣ 📜 fonts_results_raw.csv
    ┗ 📜 calligraphy_results_raw.csv
```
## 🚀 使い方
1. **環境準備**:
   必要なライブラリをインストールします。
   `pip install opencv-python numpy matplotlib scipy pandas`

2. **設定の変更**:
   `box_counting.py` 冒頭の `IMG_SIZE` を書き換えることで、解析解像度（1024px, 512pxなど）を簡単に変更できます。

3. **実行**:
   ターミナルでプログラムを実行し、画面の指示に従ってモードとフォルダを選択します。
   `python box_counting.py`

4. **結果の確認**:
   `results/master_analysis.csv` を Excel 等で開くと、文字ごとのフラクタル次元が一覧で比較できます。

---


   