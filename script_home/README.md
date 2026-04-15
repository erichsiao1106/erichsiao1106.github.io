# script_home — Eric 的網站維護腳本集

所有腳本在 `C:\Users\erich\Desktop\my-portfolio` 目錄下執行：

```
cd C:\Users\erich\Desktop\my-portfolio
python script_home\腳本名稱.py
```

---

## 腳本清單

| 編號 | 檔名 | 用途 | 頻率 |
|------|------|------|------|
| 1 | `1_gen_bible.py` | 生成聖經所有章節的空白佔位頁面（224 個） | 一次性 / 補頁時 |
| 2 | `2_gen_fandeng.py` | 生成樊登讀書 2013~2026 所有月份佔位頁面（168 個） | 一次性 / 補頁時 |
| 3 | `3_sync_fandeng.py` | 把樊登 `_index.md` 連結文字同步到各頁面 `title:` | **日常使用** |
| 4 | `4_fix_index_linebreak.py` | 確保 `_index.md` 每個連結間有空行（換行顯示） | 格式修正時 |
| 5 | `5_fix_dates.py` | 批次修正頁面日期（避免 buildFuture 404） | 遇到 404 時 |
| 6 | `6_update_bible_index.py` | 更新聖經 `_index.md` 連結格式為完整標題 + 加空行 | 一次性 / 格式變動時 |
| 7 | `7_sync_bible.py` | 把聖經 `_index.md` 連結文字同步到各頁面 `title:` | **日常使用** |

---

## 日常新增內容流程

```
1. 打開 content/fandeng/_index.md
   → 修改連結文字，例如：
     [高效演講 × 幸福的方法](/fandeng/fandeng-2013-01/)

2. 執行同步：
   python script_home/3_sync_fandeng.py

3. 打開對應的 .md 檔案，新增內文

4. git add . && git commit -m "新增xxx內容" && git push
```

---

## 常見問題

**頁面 404？**
→ 日期填了「今天台灣時間」但 GitHub Actions 用 UTC，可能被視為未來日期
→ 執行 `5_fix_dates.py`，把日期改成昨天

**_index.md 連結沒換行？**
→ Markdown 需要空行才換行
→ 執行 `4_fix_index_linebreak.py`
