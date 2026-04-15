"""
3_sync_fandeng.py — 從 _index.md 同步連結文字到各頁面的 title
================================================================
用法：
    cd C:\\Users\\erich\\Desktop\\my-portfolio
    python script_home/3_sync_fandeng.py

功能：
    讀取 content/fandeng/_index.md 裡每個連結的文字，
    自動更新對應 .md 檔案的 title: front matter。

    只改 title: 那一行，所有內文完全不動。

日常工作流程：
    1. 打開 content/fandeng/_index.md
    2. 把連結文字改成你想要的標題
       例：[《1月》]  →  [高效演講 × 幸福的方法]
    3. 執行本腳本：python script_home/3_sync_fandeng.py
    4. 對應的 fandeng-2013-01.md 的 title: 就會自動更新
    5. git add + commit + push

_index.md 連結格式規範：
    [顯示標題](/fandeng/fandeng-YYYY-MM/)
    例：[高效演講 × 幸福的方法](/fandeng/fandeng-2013-01/)
"""
import re
from pathlib import Path

BASE = Path("C:/Users/erich/Desktop/my-portfolio/content/fandeng")
INDEX = BASE / "_index.md"


def update_title_only(file_path: Path, new_title: str) -> bool:
    """
    只修改 front matter 的 title: 那一行，不動其他任何內容。
    回傳 True 表示有修改，False 表示無變化或略過。
    """
    text = file_path.read_text(encoding="utf-8")

    if not text.startswith("---"):
        print(f"  SKIP（找不到 front matter）：{file_path.name}")
        return False

    fm_end = text.find("---", 3)
    if fm_end == -1:
        print(f"  SKIP（front matter 未關閉）：{file_path.name}")
        return False

    front_matter = text[:fm_end]
    rest = text[fm_end:]

    new_fm = re.sub(
        r'^title:.*$',
        f'title: "{new_title}"',
        front_matter,
        flags=re.MULTILINE
    )

    if new_fm == front_matter:
        return False  # 標題沒變，跳過

    file_path.write_text(new_fm + rest, encoding="utf-8")
    return True


def main():
    index_text = INDEX.read_text(encoding="utf-8")

    # 找出所有 [連結文字](/fandeng/slug/) 配對
    pattern = r'\[([^\]]+)\]\(/fandeng/([^/]+)/\)'
    matches = re.findall(pattern, index_text)

    if not matches:
        print("_index.md 裡沒有找到任何連結，請確認格式是否正確。")
        return

    updated = 0
    skipped = 0

    for link_text, slug in matches:
        md_file = BASE / f"{slug}.md"

        if not md_file.exists():
            print(f"  SKIP（檔案不存在）：{slug}.md  ← 請先建立此檔或移除 _index.md 的連結")
            skipped += 1
            continue

        changed = update_title_only(md_file, link_text)
        if changed:
            print(f"  OK  {slug}.md  →  title: {link_text}")
            updated += 1

    print(f"\n完成：更新 {updated} 個，跳過 {skipped} 個")


if __name__ == "__main__":
    main()
