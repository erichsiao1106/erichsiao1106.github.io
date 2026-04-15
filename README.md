# Eric Hsiao — Personal Website

> IC Design Engineer · AI 工具開發 · 數位工作術  
> 🌐 [erichsiao1106.github.io](https://erichsiao1106.github.io/)

---

## 關於這個網站

這是我的個人知識庫與作品集，用 [Hugo](https://gohugo.io/) 靜態網站框架 + [PaperMod](https://github.com/adityatelange/hugo-PaperMod) 主題建置，部署在 GitHub Pages。

記錄 IC 設計學習歷程、AI 工具開發實驗，以及長期閱讀與英語學習的筆記。

---

## 內容板塊

| 板塊 | 說明 |
|------|------|
| [作品集](https://erichsiao1106.github.io/projects/) | IC 設計 + AI 工具開發專案（RTL、CDC、Claude API、MCP Server） |
| [部落格](https://erichsiao1106.github.io/blog/) | 技術文章、學習心得 |
| [聖經](https://erichsiao1106.github.io/bible/) | 整本聖經每 6 章為一組的閱讀筆記（224 組） |
| [樊登讀書](https://erichsiao1106.github.io/fandeng/) | 2013–2026 每月書單與心得 |
| [精通英語](https://erichsiao1106.github.io/english/) | 英文教材 + Growme 課程學習筆記（65 組） |

---

## 技術架構

```
Hugo (Extended) v0.160.1
Theme: PaperMod
Deploy: GitHub Actions → GitHub Pages
Language: 繁體中文（zh-tw）
```

### 專案結構

```
my-portfolio/
├── content/
│   ├── about/          # 關於我
│   ├── projects/       # 作品集
│   ├── blog/           # 部落格文章
│   ├── bible/          # 聖經筆記（224 個頁面）
│   ├── fandeng/        # 樊登讀書（每月一頁）
│   └── english/        # 精通英語（65 個頁面）
├── static/images/      # 圖片資源
├── script_home/        # 批次生成 / 同步腳本
└── hugo.yaml           # 網站設定
```

---

## 本地開發

```bash
# 安裝 Hugo Extended（需要 v0.116+）
winget install Hugo.Hugo.Extended

# clone 專案（含 PaperMod submodule）
git clone --recurse-submodules https://github.com/erichsiao1106/erichsiao1106.github.io.git
cd erichsiao1106.github.io

# 啟動本地預覽（http://localhost:1313）
hugo server

# 建置靜態檔案
hugo --minify
```

---

## 維護腳本（`script_home/`）

| 腳本 | 功能 |
|------|------|
| `1_gen_bible.py` | 生成聖經佔位頁面 |
| `2_gen_fandeng.py` | 生成樊登讀書佔位頁面 |
| `3_sync_fandeng.py` | 同步樊登 `_index.md` 標題到各頁面 |
| `6_update_bible_index.py` | 更新聖經 `_index.md` 連結格式 |
| `7_sync_bible.py` | 同步聖經 `_index.md` 標題到各頁面 |
| `8_gen_english.py` | 生成精通英語佔位頁面 |
| `9_sync_english.py` | 同步精通英語 `_index.md` 標題到各頁面 |

---

## 聯絡

- GitHub：[@erichsiao1106](https://github.com/erichsiao1106)
- Email：erichsiao801106@gmail.com
