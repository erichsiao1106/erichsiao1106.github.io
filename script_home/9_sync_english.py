"""
9_sync_english.py — 從 english/_index.md 同步連結文字到各頁面的 title
================================================================
用法：
    cd C:\\Users\\erich\\Desktop\\my-portfolio
    python script_home/9_sync_english.py

功能：
    讀取 content/english/_index.md 裡每個連結的文字，
    自動更新對應 .md 檔案的 title: front matter。

    只改 title: 那一行，所有內文完全不動。

日常工作流程：
    1. 打開 content/english/_index.md，修改連結文字
    2. 執行：python script_home/9_sync_english.py
    3. 對應 .md 的 title: 自動更新
    4. git add + commit + push
"""
import re
from pathlib import Path

BASE = Path("C:/Users/erich/Desktop/my-portfolio/content/english")
INDEX = BASE / "_index.md"


def update_title_only(file_path: Path, new_title: str) -> bool:
    text = file_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return False
    fm_end = text.find("---", 3)
    if fm_end == -1:
        return False
    front_matter = text[:fm_end]
    rest = text[fm_end:]
    new_fm = re.sub(r'^title:.*$', f'title: "{new_title}"', front_matter, flags=re.MULTILINE)
    if new_fm == front_matter:
        return False
    file_path.write_text(new_fm + rest, encoding="utf-8")
    return True


def main():
    index_text = INDEX.read_text(encoding="utf-8")
    pattern = r'\[([^\]]+)\]\(/english/([^/]+)/\)'
    matches = re.findall(pattern, index_text)

    if not matches:
        print("english/_index.md 裡沒有找到任何連結，請確認格式是否正確。")
        return

    updated, skipped = 0, 0
    for link_text, slug in matches:
        md_file = BASE / f"{slug}.md"
        if not md_file.exists():
            print(f"  SKIP（檔案不存在）：{slug}.md")
            skipped += 1
            continue
        if update_title_only(md_file, link_text):
            print(f"  OK  {slug}.md")
            updated += 1

    print(f"\n完成：更新 {updated} 個，跳過 {skipped} 個")


if __name__ == "__main__":
    main()
