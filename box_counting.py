import os
import re
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from datetime import datetime
import pandas as pd
import csv

# --- 設定 ---
DATA_DIR = "./data"
RESULTS_DIR = "./results"
LOG_FILE = "closed_folder.log"

# 🌟【画像サイズ定数】ここを変更すれば全体に反映されます (例: 1024, 512, 256)
IMG_SIZE = 256

# 分析用ファイルの名前（すべて results フォルダ直下に配置）
MASTER_CSV = os.path.join(RESULTS_DIR, "master_analysis.csv")
FONTS_RAW_CSV = os.path.join(RESULTS_DIR, "fonts_results_raw.csv")
CALLIGRAPHY_RAW_CSV = os.path.join(RESULTS_DIR, "calligraphy_results_raw.csv")

def init_directories():
    """ディレクトリとログファイルの初期化"""
    os.makedirs(os.path.join(DATA_DIR, "calligraphy"), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "fonts"), exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(os.path.join(RESULTS_DIR, "calligraphy"), exist_ok=True)
    os.makedirs(os.path.join(RESULTS_DIR, "fonts"), exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            pass

def get_base_name(folder_name):
    """フォルダ名の末尾にある数字を削除 (例: Japan2 -> Japan)"""
    return re.sub(r'\d+$', '', folder_name)

def read_closed_folders():
    """ログから処理済みフォルダ一覧を取得"""
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def append_to_log(folder_name):
    """完了したフォルダをログに追記"""
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{folder_name}\n")

def process_image(img_path, output_path):
    """画像の解析、グラフ描画、D値の算出"""
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError("画像の読み込みに失敗しました。")
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 指定のIMG_SIZEへのリサイズ（アスペクト比維持）
    h, w = gray.shape
    scale = IMG_SIZE / max(h, w)
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(gray, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    # 指定サイズのキャンバス配置
    canvas = np.full((IMG_SIZE, IMG_SIZE), 255, dtype=np.uint8)
    y_off = (IMG_SIZE - new_h) // 2
    x_off = (IMG_SIZE - new_w) // 2
    canvas[y_off:y_off+new_h, x_off:x_off+new_w] = resized
    
    # 大津の2値化 (文字部分を255に反転)
    _, binary = cv2.threshold(canvas, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Density (黒ピクセル率) の計算と除外判定
    density = np.count_nonzero(binary) / binary.size
    if density > 0.50:
        raise ValueError(f"Density異常({density:.4f})。背景誤認識のため除外。")

    # ボックスカウント実行
    # IMG_SIZEに応じた2の累乗リストを自動生成 (例: 1024なら 2, 4, ... 512)
    max_pow = int(np.log2(IMG_SIZE))
    box_sizes = [2**i for i in range(1, max_pow)]
    
    counts = []
    for L in box_sizes:
        count = 0
        for i in range(0, IMG_SIZE, L):
            for j in range(0, IMG_SIZE, L):
                if np.any(binary[i:i+L, j:j+L]):
                    count += 1
        counts.append(count)
    
    # 回帰分析
    x = np.log(1.0 / np.array(box_sizes))
    y = np.log(counts)
    slope, intercept, r_value, _, _ = linregress(x, y)
    r_squared = r_value ** 2
    
    # 結果画像の保存
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.bitwise_not(binary), cmap='gray')
    plt.title(f"Density: {density:.4f} (Size: {IMG_SIZE})")
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.plot(x, y, 'o')
    plt.plot(x, intercept + slope * x, 'r', label=f'D={slope:.4f}, R²={r_squared:.4f}')
    plt.xlabel('log(1/L)')
    plt.ylabel('log(N(L))')
    plt.legend(); plt.grid(True); plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    
    return slope, r_squared, density

def update_master_analysis():
    """フォントとカリグラフィーの生データを統合して横並び表を生成"""
    all_dfs = []
    for p in [FONTS_RAW_CSV, CALLIGRAPHY_RAW_CSV]:
        if os.path.exists(p):
            try:
                all_dfs.append(pd.read_csv(p))
            except Exception:
                pass
    
    if not all_dfs:
        return

    combined = pd.concat(all_dfs, ignore_index=True)
    pivot_df = combined.pivot_table(index='文字', columns='カテゴリ', values='フラクタル次元', aggfunc='last')
    pivot_df.to_csv(MASTER_CSV, encoding='utf-8-sig')
    print(f"\n[Master Updated] {MASTER_CSV}")

def main():
    init_directories()
    
    print(f"=== フラクタル次元 解析ツール（サイズ設定: {IMG_SIZE}px） ===")
    print("1: Calligraphy | 2: Fonts")
    choice = input("モードを選択してください: ").strip()
    
    if choice == '1':
        mode, raw_csv = "calligraphy", CALLIGRAPHY_RAW_CSV
    elif choice == '2':
        mode, raw_csv = "fonts", FONTS_RAW_CSV
    else:
        return

    target_data_dir = os.path.join(DATA_DIR, mode)
    all_folders = [f for f in os.listdir(target_data_dir) if os.path.isdir(os.path.join(target_data_dir, f))]
    closed = read_closed_folders()
    available = [f for f in all_folders if f not in closed]

    if not available:
        print("未処理のフォルダがありません。")
        return

    print("\n【未処理フォルダ一覧】")
    for i, f in enumerate(available, 1):
        print(f"{i}: {f}")
    
    try:
        idx = int(input("\n処理する番号を入力: ")) - 1
        selected_folder = available[idx]
    except:
        return

    category_name = get_base_name(selected_folder)
    output_dir = os.path.join(RESULTS_DIR, mode, category_name)
    os.makedirs(output_dir, exist_ok=True)

    headers = ['文字', 'カテゴリ', 'フラクタル次元', 'R^2', 'Density', '入力パス', '出力パス', 'タイムスタンプ']
    if not os.path.exists(raw_csv):
        with open(raw_csv, 'w', encoding='utf-8-sig', newline='') as f:
            csv.writer(f).writerow(headers)

    input_dir = os.path.join(target_data_dir, selected_folder)
    images = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    with open(raw_csv, 'a', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        for img_name in images:
            char_name = os.path.splitext(img_name)[0]
            out_path = os.path.join(output_dir, f"{char_name}_output.png")
            
            if os.path.exists(out_path):
                continue
            
            print(f"処理中: {char_name}...", end=" ", flush=True)
            try:
                d, r2, dens = process_image(os.path.join(input_dir, img_name), out_path)
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([char_name, category_name, d, r2, dens, os.path.join(input_dir, img_name), out_path, ts])
                print(f"D={d:.4f}")
            except Exception as e:
                print(f"スキップ: {e}")

    update_master_analysis()
    append_to_log(selected_folder)
    print("\nすべての工程が完了しました。")

if __name__ == "__main__":
    main()