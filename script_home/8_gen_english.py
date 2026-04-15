"""
8_gen_english.py — 生成「精通英語」所有課次的 Hugo Markdown 佔位頁面
================================================================
用法：
    cd C:\\Users\\erich\\Desktop\\my-portfolio
    python script_home/8_gen_english.py

功能：
    1. 依照 BOOKS 清單，每 3 課一組生成佔位頁面到 content/english/
    2. 自動生成 content/english/_index.md（目錄索引頁）

    ⚠️  警告：若對應 .md 已有內容，執行後會被空白佔位覆蓋！
    已有內容的頁面請「不要重跑」。

分組規則：
    每 3 課為一組，最後不足 3 課也納入（顯示實際範圍）
    例：19 課 → 01~03 / 04~06 / ... / 16~18 / 19

注意：
    DATE 請填「昨天」或更早，避免 buildFuture: false 造成 404
"""
from pathlib import Path

BASE = Path("C:/Users/erich/Desktop/my-portfolio")
DATE = "2026-04-14"      # ← 維護時確認 <= 昨天（UTC）
GROUP_SIZE = 3
SECTION = "精通英語"

# (category, book_name, slug, total_lessons)
BOOKS = [
    ("英文教材", "冠軍思維",    "champion",         6),
    ("英文教材", "旅遊英文 一", "travel-1",         12),
    ("英文教材", "旅遊英文 二", "travel-2",         14),
    ("英文教材", "職場英文",    "workplace",        19),
    ("英文教材", "校園英文 一", "campus-1",         12),
    ("英文教材", "校園英文 二", "campus-2",         13),
    ("英文教材", "中級英文 一", "intermediate-1",   19),
    ("英文教材", "中級英文 二", "intermediate-2",   14),
    ("Growme",  "Week 1",      "growme-week-1",    6),
    ("Growme",  "Week 2",      "growme-week-2",    6),
    ("Growme",  "Week 3",      "growme-week-3",    6),
    ("Growme",  "Week 4",      "growme-week-4",    6),
    ("Growme",  "Week 5",      "growme-week-5",    6),
    ("Growme",  "Week 6",      "growme-week-6",    6),
    ("Growme",  "Learning 1",  "growme-learning-1", 6),
    ("Growme",  "Learning 2",  "growme-learning-2", 6),
    ("Growme",  "Learning 3",  "growme-learning-3", 6),
    ("Growme",  "Learning 4",  "growme-learning-4", 6),
    ("Growme",  "Learning 5",  "growme-learning-5", 6),
    ("Growme",  "Learning 6",  "growme-learning-6", 6),
    ("Growme",  "Learning 7",  "growme-learning-7", 6),
]


def get_parts(total, group=GROUP_SIZE):
    """把 total 課依 group 大小分組，回傳 [(part_num, '01~03'), ...]"""
    parts = []
    start = 1
    num = 1
    while start <= total:
        end = min(start + group - 1, total)
        rng = f"{start:02d}~{end:02d}" if start != end else f"{start:02d}"
        parts.append((num, rng))
        start += group
        num += 1
    return parts


def build_index(english_dir):
    lines = [
        '---',
        f'title: "{SECTION}"',
        'description: "英語學習筆記：英文教材 + Growme"',
        'layout: single',
        'showToc: true',
        'TocOpen: true',
        'cascade:',
        '  showToc: true',
        '  TocOpen: false',
        '  ShowPostNavLinks: true',
        '---',
        '',
    ]

    cur_cat = None
    for category, book_name, slug, total in BOOKS:
        # 分類標題（## 層）
        if category != cur_cat:
            lines.append(f'## {category}')
            lines.append('')
            cur_cat = category

        # 書名標題 + 分隔線
        lines.append(f'**{book_name}**（{total} 課）')
        lines.append('---')

        for part_num, rng in get_parts(total):
            link_text = f"{SECTION}《{category}》《{book_name}》《{part_num}》{rng}"
            url = f"/english/{slug}-{part_num:02d}/"
            lines.append(f'[{link_text}]({url})')
            lines.append('')   # 空行讓每個連結換行

    (english_dir / "_index.md").write_text('\n'.join(lines), encoding="utf-8")
    print("_index.md 已生成")


def build_pages(english_dir):
    count = 0
    for category, book_name, slug, total in BOOKS:
        for part_num, rng in get_parts(total):
            title = f"{SECTION}《{category}》《{book_name}》《{part_num}》{rng}"
            filename = f"{slug}-{part_num:02d}.md"
            content = f"""---
title: "{title}"
date: {DATE}
draft: false
description: ""
category: "{category}"
book: "{book_name}"
part: {part_num}
chapters: "{rng}"
showToc: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
---

（內容待新增）
"""
            (english_dir / filename).write_text(content, encoding="utf-8")
            count += 1
    print(f"佔位頁面已生成：{count} 個")


if __name__ == "__main__":
    english_dir = BASE / "content/english"
    english_dir.mkdir(parents=True, exist_ok=True)
    build_index(english_dir)
    build_pages(english_dir)
    print(f"\n完成！請記得在 hugo.yaml 加入選單，並執行 git add + commit + push")
