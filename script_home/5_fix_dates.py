"""
5_fix_dates.py — 批次修正 content/ 下頁面的 date: front matter
================================================================
用法：
    cd C:\\Users\\erich\\Desktop\\my-portfolio
    python script_home/5_fix_dates.py

功能：
    GitHub Actions 伺服器使用 UTC 時間，hugo.yaml 設定 buildFuture: false。
    如果頁面的 date: 是「今天台灣時間」但 UTC 還沒到，頁面會被跳過 → 404。

    本腳本掃描指定資料夾下所有 .md 檔，
    把 WRONG_DATE 替換成 RIGHT_DATE（只改 front matter 的 date: 那一行）。

修改方式：
    1. 把 WRONG_DATE 改成你誤填的日期
    2. 把 RIGHT_DATE 改成要改成的日期（建議填昨天）
    3. 把 TARGET_DIR 改成要掃描的資料夾
    4. 執行腳本

注意：
    安全的日期原則：永遠填「今天台灣時間的前一天」或更早，
    這樣不論 Actions 幾點跑都不會被視為未來頁面。
"""
from pathlib import Path

# ── 設定區（修改這裡）────────────────────────────
WRONG_DATE = "2026-04-15"           # 要被換掉的日期
RIGHT_DATE = "2026-04-14"           # 替換成的日期
TARGET_DIR = Path("C:/Users/erich/Desktop/my-portfolio/content/fandeng")
# ─────────────────────────────────────────────────

fixed = 0
for f in TARGET_DIR.rglob("*.md"):
    text = f.read_text(encoding="utf-8")
    if f"date: {WRONG_DATE}" in text:
        # 只換 front matter 裡的 date:（前 500 字元內，避免誤改內文）
        fm_end = text.find("---", 3)
        if fm_end == -1:
            continue
        front_matter = text[:fm_end]
        rest = text[fm_end:]
        new_fm = front_matter.replace(f"date: {WRONG_DATE}", f"date: {RIGHT_DATE}")
        if new_fm != front_matter:
            f.write_text(new_fm + rest, encoding="utf-8")
            print(f"  Fixed: {f.name}")
            fixed += 1

print(f"\n完成：修正 {fixed} 個檔案（{WRONG_DATE} → {RIGHT_DATE}）")
