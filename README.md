# Fractal Dimension Analyzer for Calligraphy 🖋️📐

[![Language](https://img.shields.io/badge/Language-Python-blue.svg)](https://www.python.org/)

（[English follows Japanese](#english)）

このリポジトリは、ボックスカウント法（Box-counting method）を用いて、画像から**フラクタル次元（Fractal Dimension）**を自動で算出し、比較・解析するためのPythonプログラムです。
現在は主に**「書（カリグラフィー）やフォント」**の解析を目的として構成されていますが、非常に拡張性の高いディレクトリ構造を持っているため、**フォルダを追加するだけで、絵画、自然風景、テクスチャなど、あらゆる画像の解析にそのまま応用することが可能**です。

## 🌟 特徴
- **自動正規化**: アスペクト比を維持した1024pxへの自動リサイズとキャンバス配置。
- **自動2値化**: Otsuメソッド（大津の2値化）による主観を排除したしきい値設定。
- **学術的指標の同時算出**: フラクタル次元 (D) に加え、近似直線の決定係数 (R^2) と、黒ピクセル率 (Density) を算出。
- **高い汎用性と拡張性**: 独立したデータフォルダ構造により、コードを書き換えることなく別ジャンル（例：絵画）のデータセット解析へ容易に拡張可能。
- **重複・エラー回避**: 処理済みフォルダのログ記録によるスキップ機能と、破損ファイルの自動回避。

## 📂 ディレクトリ構成と応用
入力・出力は完全にジャンルごとに独立して管理されます。現在は `calligraphy` と `fonts` が用意されていますが、例えば `data/paintings/` というフォルダを新設すれば、そのまま絵画のフラクタル次元解析を行うことができます。

    📦 fractal-dimension-calligraphy
     ┣ 📜 fractal_analyzer.py      # 実行プログラム本体
     ┣ 📜 closed_folder.log        # 処理済みフォルダの記録用ログ
     ┣ 📂 data/                    # 入力ディレクトリ
     │  ┣ 📂 calligraphy/          # [メイン] カリグラフィー画像
     │  ┣ 📂 fonts/                # [メイン] フォント画像
     │  ┗ 📂 paintings/            # (応用例) 絵画など、フォルダ追加で拡張可能！
     ┗ 📂 results/                 # 出力ディレクトリ (自動生成)
        ┣ 📂 calligraphy/          
        ┣ 📂 fonts/                
        ┗ 📂 paintings/            

## 🚀 使い方
1. 必要なライブラリをインストールします。
   `pip install opencv-python numpy matplotlib scipy pandas`

2. `data/` 以下の任意のジャンルフォルダ（例: `data/calligraphy/Japan/`）に解析したい画像を配置します。

3. プログラムを実行し、ターミナルの指示に従って対象フォルダを選択します。
   `python fractal_analyzer.py`

4. `results/` ディレクトリ内に、解析済みのグラフ画像と、構造化されたCSVデータが自動生成されます。

---

<a id="english"></a>
# English

This repository provides a Python program to automatically calculate, compare, and analyze the **Fractal Dimension** of images using the box-counting method. 
While the current primary focus is on **analyzing calligraphy and fonts**, the tool is designed with a highly modular and scalable directory structure. **By simply adding new folders, it can be easily applied to analyze any other types of images**, such as paintings, natural landscapes, or textures, without changing the core code.

## 🌟 Features
- **Auto Resizing**: Reproduces the exact process of resizing to 1024px while maintaining aspect ratio, and centering on a canvas.
- **Auto-Binarization**: Objective thresholding using the Otsu method.
- **Academic Metrics**: Calculates the Fractal Dimension (D), the coefficient of determination (R^2) of the fitted line, and the pixel density.
- **High Extensibility**: The independent folder structure allows seamless application to new datasets (e.g., paintings) just by creating a new directory.
- **Robust Processing**: Includes a skipping mechanism for already processed folders (via log files) and automatic error handling for corrupted files.

## 📂 Directory Structure & Extensibility
Inputs and outputs are managed completely independently by category. Currently, `calligraphy` and `fonts` are set up. If you want to analyze paintings, simply create a `data/paintings/` folder, and the program will handle it automatically.

    📦 fractal-dimension-calligraphy
     ┣ 📜 fractal_analyzer.py      # Main program
     ┣ 📜 closed_folder.log        # Log file to track processed folders
     ┣ 📂 data/                    # Input directory
     │  ┣ 📂 calligraphy/          # [Main Focus] Calligraphy images
     │  ┣ 📂 fonts/                # [Main Focus] Font images
     │  ┗ 📂 paintings/            # (Example) Easily extendable to other domains!
     ┗ 📂 results/                 # Output directory (Auto-generated)
        ┣ 📂 calligraphy/          
        ┣ 📂 fonts/                
        ┗ 📂 paintings/            

## 🚀 Usage
1. Install the required libraries:
   `pip install opencv-python numpy matplotlib scipy pandas`

2. Place the images you want to analyze in a category folder under `data/` (e.g., `data/calligraphy/Japan/`).

3. Run the program and follow the terminal prompts to select the target folder:
   `python fractal_analyzer.py`

4. The analyzed plot images and structured CSV data will be automatically generated in the `results/` directory.
