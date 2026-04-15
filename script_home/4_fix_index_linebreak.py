"""
4_fix_index_linebreak.py — 確保 _index.md 中每個連結之間都有空行
================================================================
用法：
    cd C:\\Users\\erich\\Desktop\\my-portfolio
    python script_home/4_fix_index_linebreak.py [目標檔案路徑]

    不指定路徑時，預設處理 content/fandeng/_index.md

    也可以處理聖經：
    python script_home/4_fix_index_linebreak.py content/bible/_index.md

功能：
    Markdown 裡兩個連結若緊連在一起（中間無空行），網頁顯示時
    會合併成同一行。本腳本自動在連續連結之間補上空行，
    讓每個連結在網頁上各自獨立成一行。

    只改格式（空行），不改任何文字內容。
"""
import re
import sys
from pathlib import Path

# 預設目標
DEFAULT_TARGET = Path("C:/Users/erich/Desktop/my-portfolio/content/fandeng/_index.md")

target = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_TARGET

if not target.exists():
    print(f"找不到檔案：{target}")
    sys.exit(1)

text = target.read_text(encoding="utf-8")
lines = text.split("\n")
new_lines = []

for i, line in enumerate(lines):
    new_lines.append(line)
    # 這行是連結、下一行也是連結 → 插入空行
    is_link = line.strip().startswith("[")
    next_is_link = (i + 1 < len(lines)) and lines[i + 1].strip().startswith("[")
    if is_link and next_is_link:
        new_lines.append("")

result = "\n".join(new_lines)
target.write_text(result, encoding="utf-8")
print(f"完成：{target}")
print("每個連結之間都已確保有空行（換行顯示）")
