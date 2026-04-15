"""
6_update_bible_index.py — 更新 bible/_index.md 連結格式 + 加空行換行
================================================================
用法：
    cd C:\\Users\\erich\\Desktop\\my-portfolio
    python script_home/6_update_bible_index.py

功能：
    1. 把聖經 _index.md 的連結文字從簡短格式改成完整格式：
       舊：[《1》01~06](/bible/genesis-01/)
       新：[舊約聖經《摩西五經》《創世記》《1》01~06](/bible/genesis-01/)

    2. 移除連結之間的 ·（中點分隔符）

    3. 在每個連結之間補上空行，確保網頁上各自換行顯示

執行後請接著跑 7_sync_bible.py，把連結文字同步到各頁面的 title。

格式說明：
    [testament《category》《book》《part_num》chapters](url)
    例：[舊約聖經《摩西五經》《創世記》《1》01~06](/bible/genesis-01/)
"""
import re
from pathlib import Path

INDEX = Path("C:/Users/erich/Desktop/my-portfolio/content/bible/_index.md")

text = INDEX.read_text(encoding="utf-8")
lines = text.split("\n")

current_testament = ""
current_category = ""
current_book = ""

new_lines = []

for i, line in enumerate(lines):
    stripped = line.strip()

    # ── 追蹤聖約層級（## 舊約聖經 / ## 新約聖經）──
    if re.match(r'^## [^#]', stripped):
        current_testament = re.sub(r'^## ', '', stripped).strip()
        new_lines.append(line)
        continue

    # ── 追蹤分類層級（### 摩西五經 / ### 歷史書 ...）──
    if re.match(r'^### ', stripped):
        current_category = re.sub(r'^### ', '', stripped).strip()
        new_lines.append(line)
        continue

    # ── 追蹤書卷名稱（**創世記** / **詩篇** ...）──
    book_match = re.match(r'^\*\*(.+?)\*\*', stripped)
    if book_match:
        current_book = book_match.group(1)
        new_lines.append(line)
        continue

    # ── 處理連結行 ──
    if stripped.startswith("["):
        # 移除行尾的 ·（中點）與多餘空白
        clean = re.sub(r'\s*·\s*$', '', stripped).strip()

        # 解析連結：[《part》chapters](url)
        # 也相容已更新過的格式（idempotent）
        link_match = re.match(r'\[.*?《(\d+)》(.+?)\]\((/bible/[^)]+/)\)', clean)
        if link_match and current_testament:
            part_num = link_match.group(1)
            chapters = link_match.group(2).strip()
            url = link_match.group(3)
            new_text = (
                f"{current_testament}"
                f"《{current_category}》"
                f"《{current_book}》"
                f"《{part_num}》{chapters}"
            )
            new_line = f"[{new_text}]({url})"
        else:
            # 無法解析，保留原樣（只去掉·）
            new_line = clean

        new_lines.append(new_line)

        # 下一行也是連結 → 補空行（確保換行）
        next_stripped = lines[i + 1].strip() if i + 1 < len(lines) else ""
        if next_stripped.startswith("["):
            new_lines.append("")
        continue

    # ── 其他行（空行、---、說明文字）── 保留原樣
    new_lines.append(line)

result = "\n".join(new_lines)
INDEX.write_text(result, encoding="utf-8")
print("bible/_index.md 更新完成")
print("連結已改為完整格式，並在每個連結之間加上空行")
print("請接著執行：python script_home/7_sync_bible.py")
