"""
1. 修正所有 Bible 頁面的 showToc: false → showToc: true
2. 生成樊登讀書 2013-2026 所有頁面
"""
from pathlib import Path

BASE = Path("C:/Users/erich/Desktop/my-portfolio")
DATE = "2026-04-14"

# ── Task 1: Fix Bible showToc ──────────────────────────────
bible_dir = BASE / "content/bible"
fixed = 0
for f in bible_dir.glob("*.md"):
    if f.name == "_index.md":
        continue
    text = f.read_text(encoding="utf-8")
    if "showToc: false" in text:
        f.write_text(text.replace("showToc: false", "showToc: true"), encoding="utf-8")
        fixed += 1
print(f"Bible showToc fixed: {fixed} files")

# ── Task 2: Generate Fandeng pages ────────────────────────
MONTHS = [
    (1, "1、2月"),
    (2, "3、4月"),
    (3, "5、6月"),
    (4, "7、8月"),
    (5, "9、10月"),
    (6, "11、12月"),
]

fandeng_dir = BASE / "content/fandeng"
fandeng_dir.mkdir(parents=True, exist_ok=True)

count = 0
for year in range(2013, 2027):
    for part, months in MONTHS:
        title = f"{year} 樊登讀書《{months}》"
        slug = f"fandeng-{year}-{part:02d}"
        content = f"""---
title: "{title}"
date: {DATE}
draft: false
description: ""
year: {year}
part: {part}
months: "{months}"
showToc: true
TocOpen: false
---

（內容待新增）
"""
        (fandeng_dir / f"{slug}.md").write_text(content, encoding="utf-8")
        count += 1

print(f"Fandeng pages created: {count} files")
