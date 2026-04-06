import sys

# 12音の定義（シャープ表記に統一）
NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# フラット表記をシャープ表記に変換するための辞書
FLAT_TO_SHARP = {
    'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#'
}

# ダイアトニックコードの構成パターン
# メジャー: I, IIm, IIIm, IV, V, VIm, VIIdim
MAJOR_PATTERN = ['', 'm', 'm', '', '', 'm', 'dim']
# マイナー: Im, IIdim, bIII, IVm, Vm, bVI, bVII
MINOR_PATTERN = ['m', 'dim', '', 'm', 'm', '', '']

def normalize_chord(chord):
    """入力されたコードを#表記に正規化する"""
    if not chord:
        return ""
    
    # 最初の2文字を確認してフラットがあれば変換
    for flat, sharp in FLAT_TO_SHARP.items():
        if chord.startswith(flat):
            chord = chord.replace(flat, sharp, 1)
            break
    
    # 小文字の 'am' を 'm' に修正するなど、簡単な表記ゆれ防止
    chord = chord.replace('minor', 'm').replace('maj', '').replace('Maj', '')
    return chord

def get_diatonic_codes(root_idx, is_minor=False):
    """指定されたルート音とモードからダイアトニックコードのリストを生成"""
    # ダイアトニック・スケールのインターバル（全・全・半・全・全・全・半）
    intervals = [0, 2, 4, 5, 7, 9, 11]
    pattern = MINOR_PATTERN if is_minor else MAJOR_PATTERN
    
    codes = []
    for i, interval in enumerate(intervals):
        note = NOTES[(root_idx + interval) % 12]
        codes.append(f"{note}{pattern[i]}")
    return codes

def identify_key(input_chords):
    """最も合致するキーを検索する"""
    results = []
    normalized_inputs = [normalize_chord(c) for c in input_chords]
    
    # 全12音についてメジャー/マイナーの両方をチェック
    for i in range(12):
        # Major Key のチェック
        major_codes = get_diatonic_codes(i, is_minor=False)
        major_match = len(set(normalized_inputs) & set(major_codes))
        results.append({
            'key_name': f"{NOTES[i]} Major",
            'match': major_match,
            'diatonic': major_codes
        })

        # minor Key のチェック
        minor_codes = get_diatonic_codes(i, is_minor=True)
        minor_match = len(set(normalized_inputs) & set(minor_codes))
        results.append({
            'key_name': f"{NOTES[i]} minor",
            'match': minor_match,
            'diatonic': minor_codes
        })

    # 一致数が多い順にソート
    results.sort(key=lambda x: x['match'], reverse=True)
    return results, normalized_inputs

def main():
    print("==========================================")
    print("   音楽キー判定 & ダイアトニック表示ツール")
    print("==========================================")
    print("使用したいコードをスペース区切りで入力してください。")
    print("例: C Am F G  /  F#m B E  /  Db Eb Fm")
    
    try:
        user_input = input("\nコードを入力 > ").split()
    except EOFError:
        return

    if not user_input:
        print("エラー: コードが入力されませんでした。")
        return

    suggestions, normalized_inputs = identify_key(user_input)
    
    # 最もスコアが高い結果を取得
    best_match = suggestions[0]
    
    print("\n" + "-"*40)
    print(f"【判定されたキー】: {best_match['key_name']}")
    print(f"【入力コード】    : {', '.join(normalized_inputs)}")
    print(f"【一致数】        : {best_match['match']} / {len(normalized_inputs)}")
    print("-" * 40)
    
    # ダイアトニックコードの一覧表示
    print(f"\n{best_match['key_name']} のダイアトニックコード一覧:")
    degrees = ["I", "II", "III", "IV", "V", "VI", "VII"]
    
    # 表形式での出力
    header = " | ".join(f"{d:^7}" for d in degrees)
    row = " | ".join(f"{c:^7}" for c in best_match['diatonic'])
    
    print(header)
    print("-" * len(header))
    print(row)
    
    # 他に候補がある場合
    if len(suggestions) > 1 and suggestions[1]['match'] == best_match['match']:
        print(f"\n※ 同率の候補: {suggestions[1]['key_name']}")
    elif suggestions[1]['match'] > 0:
        print(f"\n次点の候補: {suggestions[1]['key_name']} (一致数: {suggestions[1]['match']})")

if __name__ == "__main__":
    main()
