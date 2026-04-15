"""
sync_fandeng.py
==============
用法：python sync_fandeng.py

功能：
  讀取 content/fandeng/_index.md 裡的連結文字，
  自動同步到對應頁面的 title: front matter。
  只修改 title: 那一行，不碰內容。

工作流程：
  1. 在 _index.md 把連結文字改成你想要的標題
     例：[《1月》]  →  [高效演講 × 幸福的方法]
  2. 執行 python sync_fandeng.py
  3. 對應的 fandeng-2013-01.md 的 title: 就會更新
"""
import re
from pathlib import Path

BASE = Path("C:/Users/erich/Desktop/my-portfolio/content/fandeng")
INDEX = BASE / "_index.md"


def update_title_only(file_path: Path, new_title: str) -> bool:
    """只修改 front matter 的 title: 那一行，不動其他任何內容"""
    text = file_path.read_text(encoding="utf-8")

    if not text.startswith("---"):
        print(f"  SKIP (no front matter): {file_path.name}")
        return False

    # 找到 front matter 的結尾
    fm_end = text.find("---", 3)
    if fm_end == -1:
        print(f"  SKIP (front matter not closed): {file_path.name}")
        return False

    front_matter = text[:fm_end]
    rest = text[fm_end:]

    # 只換 title: 那一行
    new_fm = re.sub(
        r'^title:.*$',
        f'title: "{new_title}"',
        front_matter,
        flags=re.MULTILINE
    )

    if new_fm == front_matter:
        return False  # 沒變化

    file_path.write_text(new_fm + rest, encoding="utf-8")
    return True


def main():
    index_text = INDEX.read_text(encoding="utf-8")

    # 找出所有 [連結文字](/fandeng/slug/) 的配對
    pattern = r'\[([^\]]+)\]\(/fandeng/([^/]+)/\)'
    matches = re.findall(pattern, index_text)

    if not matches:
        print("_index.md 裡沒有找到任何連結，請確認格式正確。")
        return

    updated = 0
    skipped = 0

    for link_text, slug in matches:
        md_file = BASE / f"{slug}.md"

        if not md_file.exists():
            print(f"  SKIP (檔案不存在): {slug}.md")
            skipped += 1
            continue

        changed = update_title_only(md_file, link_text)
        if changed:
            print(f"  OK  {slug}.md  →  title: {link_text}")
            updated += 1

    print(f"\n完成：更新 {updated} 個，跳過 {skipped} 個")


if __name__ == "__main__":
    main()
