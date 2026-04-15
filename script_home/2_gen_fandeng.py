"""
2_gen_fandeng.py — 生成樊登讀書所有月份的 Hugo Markdown 佔位頁面
================================================================
用法：
    cd C:\\Users\\erich\\Desktop\\my-portfolio
    python script_home/2_gen_fandeng.py

功能：
    為 2013~2026 每年 12 個月各生成一個空白佔位頁面到 content/fandeng/。
    適合「第一次建立」或「補齊缺少的月份」時使用。

    ⚠️  警告：若對應 .md 檔案已有內容，執行後會被空白佔位覆蓋！
    已有內容的頁面請「不要重跑」，或改用 3_sync_fandeng.py 只更新標題。

檔案命名：
    content/fandeng/fandeng-{year}-{month:02d}.md
    例：fandeng-2013-01.md（1月）、fandeng-2026-12.md（12月）

注意：
    DATE 請填「昨天」或「更早」的日期，避免 GitHub Actions
    因 buildFuture: false 而跳過頁面（伺服器用 UTC 時間）。
"""
from pathlib import Path

BASE = Path("C:/Users/erich/Desktop/my-portfolio")
DATE = "2026-04-14"   # ← 維護時請確認這個日期 <= 昨天（UTC）

MONTH_NAMES = {
    1: "1月", 2: "2月", 3: "3月", 4: "4月",
    5: "5月", 6: "6月", 7: "7月", 8: "8月",
    9: "9月", 10: "10月", 11: "11月", 12: "12月"
}

fandeng_dir = BASE / "content/fandeng"
fandeng_dir.mkdir(parents=True, exist_ok=True)

count = 0
for year in range(2013, 2027):
    for month in range(1, 13):
        month_name = MONTH_NAMES[month]
        title = f"{year} 樊登讀書《{month_name}》"
        slug = f"fandeng-{year}-{month:02d}"
        content = f"""---
title: "{title}"
date: {DATE}
draft: false
description: ""
year: {year}
month: {month}
showToc: true
TocOpen: false
---

（內容待新增）
"""
        (fandeng_dir / f"{slug}.md").write_text(content, encoding="utf-8")
        count += 1

print(f"樊登讀書佔位頁面建立完成：{count} 個")
print("請記得在 content/fandeng/_index.md 中加入對應連結")
