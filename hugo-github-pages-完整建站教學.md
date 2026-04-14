# Hugo + GitHub Pages 個人網站完整建站教學

> 從零開始建立免費個人網站，包含作品集、部落格、搜尋功能，自動部署。
> 費用：$0（只需 GitHub 帳號）
> 時間：約 1 小時

---

## 你會得到的成果

- 網址：`https://你的帳號.github.io`
- 功能：首頁 Profile、關於我、作品集、部落格、搜尋
- 部署：Push 到 GitHub 自動更新，約 30 秒上線
- 主題：PaperMod（支援深色/淺色切換、手機版面）

---

## 事前準備

需要準備的資訊：
- GitHub 帳號名稱（沒有的話先去 github.com 註冊）
- 你的名字
- Email
- 大頭照一張（正方形、JPG 格式，命名為 `profile.jpg`）

---

## 步驟一：安裝 Git

**Windows：**
到 https://git-scm.com/download/win 下載安裝，全部選預設即可。

安裝完成後開啟 PowerShell 或 Git Bash 驗證：
```bash
git --version
# 應顯示：git version 2.x.x
```

設定你的身份（email 必須和 GitHub 帳號一致）：
```bash
git config --global user.name "你的名字"
git config --global user.email "你的email@example.com"
```

**macOS：**
```bash
brew install git
```

---

## 步驟二：安裝 Hugo Extended

> 一定要安裝 **Extended** 版本，PaperMod 主題需要它。

**Windows（用 winget，Windows 10/11 內建）：**
```bash
winget install Hugo.Hugo.Extended --accept-source-agreements --accept-package-agreements
```

安裝完成後**重新開啟終端機**，再執行：
```bash
hugo version
# 應顯示：hugo v0.160.x+extended ...
# 確認有「extended」字樣
```

**macOS：**
```bash
brew install hugo
```

---

## 步驟三：建立 Hugo 專案

```bash
# 切到桌面（或你想放專案的地方）
cd ~/Desktop

# 建立網站（-f yaml 表示用 YAML 格式設定檔）
hugo new site my-portfolio -f yaml

# 進入專案資料夾
cd my-portfolio

# 初始化 Git
git init

# 安裝 PaperMod 主題（用 Git Submodule）
git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
```

---

## 步驟四：設定 hugo.yaml

打開 `my-portfolio/hugo.yaml`，**刪除所有內容**，貼上下面這份設定，並把所有 `← 改這裡` 的地方換成你自己的資訊：

```yaml
baseURL: "https://你的GitHub帳號.github.io/"   # ← 改這裡
title: "你的名字 | 你的職稱"                     # ← 改這裡
paginate: 10
theme: PaperMod

languageCode: zh-tw
defaultContentLanguage: zh-tw

enableRobotsTXT: true
buildDrafts: false
buildFuture: false
buildExpired: false
enableEmoji: true

outputs:
  home:
    - HTML
    - RSS
    - JSON

menu:
  main:
    - identifier: about
      name: "關於我"
      url: /about/
      weight: 10
    - identifier: projects
      name: "作品集"
      url: /projects/
      weight: 20
    - identifier: blog
      name: "部落格"
      url: /blog/
      weight: 30
    - identifier: search
      name: "搜尋"
      url: /search/
      weight: 40

params:
  env: production
  description: "你的一句話介紹"   # ← 改這裡
  author: "你的名字"              # ← 改這裡

  defaultTheme: auto
  ShowThemeToggle: true
  ShowReadingTime: true
  ShowShareButtons: true
  ShowPostNavLinks: true
  ShowBreadCrumbs: true
  ShowCodeCopyButtons: true
  ShowToc: true
  TocOpen: false

  profileMode:
    enabled: true
    title: "嗨，我是 你的名字 👋"   # ← 改這裡
    subtitle: |
      你的自我介紹，可以寫兩三句話。   # ← 改這裡
    imageUrl: "/images/profile.jpg"
    imageWidth: 160
    imageHeight: 160
    imageTitle: "你的名字"
    buttons:
      - name: "關於我"
        url: /about/
      - name: "作品集"
        url: /projects/
      - name: "部落格"
        url: /blog/

  socialIcons:
    - name: github
      url: "https://github.com/你的帳號"           # ← 改這裡
    - name: linkedin
      url: "https://linkedin.com/in/你的帳號"      # ← 改這裡（沒有就刪掉這兩行）
    - name: email
      url: "mailto:你的email@example.com"          # ← 改這裡

  fuseOpts:
    isCaseSensitive: false
    shouldSort: true
    location: 0
    distance: 1000
    threshold: 0.4
    minMatchCharLength: 0
    keys: ["title", "permalink", "summary", "content"]

  assets:
    favicon: "/images/favicon.ico"

markup:
  highlight:
    codeFences: true
    guessSyntax: true
    lineNos: false
    style: monokai
  goldmark:
    renderer:
      unsafe: true
```

---

## 步驟五：建立內容頁面

在終端機執行以下指令建立資料夾：
```bash
mkdir -p content/about content/projects content/blog content/search static/images .github/workflows
```

把你的大頭照放到 `static/images/profile.jpg`。

### 關於我頁面

建立 `content/about/index.md`：
```markdown
---
title: "關於我"
description: "你的職稱"
showToc: false
ShowBreadCrumbs: false
---

## 你的名字

**你的職稱**

---

### 關於我

在這裡寫你的自我介紹。

### 專業領域

- 項目一
- 項目二
- 項目三

### 聯絡方式

- Email：[你的email](mailto:你的email@example.com)
- GitHub：[github.com/你的帳號](https://github.com/你的帳號)
```

### 作品集

建立 `content/projects/_index.md`：
```markdown
---
title: "作品集"
description: "我做過的專案與作品"
---
```

建立第一個作品 `content/projects/第一個作品.md`：
```markdown
---
title: "作品名稱"
date: 2026-04-14
description: "一句話描述"
tags: ["標籤一", "標籤二"]
showToc: true
---

## 專案概述

寫你的作品介紹。

## 技術棧

- 技術一
- 技術二

## 原始碼

[GitHub Repository →](https://github.com/你的帳號/專案名稱)
```

### 部落格

建立 `content/blog/_index.md`：
```markdown
---
title: "部落格"
description: "技術筆記與分享"
---
```

建立第一篇文章 `content/blog/hello-world.md`：
```markdown
---
title: "Hello World — 第一篇文章"
date: 2026-04-14
draft: false
description: "網站上線了。"
tags: ["Hugo", "GitHub Pages"]
showToc: false
---

在這裡寫你的第一篇文章。
```

### 搜尋頁面

建立 `content/search/_index.md`：
```markdown
---
title: "搜尋"
layout: "search"
placeholder: "輸入關鍵字搜尋..."
---
```

### 文章模板

編輯 `archetypes/default.md`（覆蓋原本內容）：
```markdown
---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
date: {{ .Date }}
draft: true
description: ""
tags: []
showToc: true
TocOpen: false
---

```

---

## 步驟六：建立 .gitignore

在 `my-portfolio/` 根目錄建立 `.gitignore` 檔案，內容如下：
```
/public/
/.hugo_build.lock
```

---

## 步驟七：建立 GitHub Actions 自動部署

建立 `.github/workflows/hugo.yaml`：
```yaml
name: Deploy Hugo site to Pages

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

defaults:
  run:
    shell: bash

jobs:
  build:
    runs-on: ubuntu-latest
    env:
      HUGO_VERSION: 0.160.1
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: ${{ env.HUGO_VERSION }}
          extended: true

      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v5

      - name: Build with Hugo
        env:
          HUGO_CACHEDIR: ${{ runner.temp }}/hugo_cache
          HUGO_ENVIRONMENT: production
          TZ: Asia/Taipei
        run: |
          hugo \
            --gc \
            --minify \
            --baseURL "${{ steps.pages.outputs.base_url }}/"

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

---

## 步驟八：本機預覽（可選）

部署前可以先在本機看效果：
```bash
# 在 my-portfolio/ 目錄下執行
hugo server -D

# 打開瀏覽器到 http://localhost:1313
# Ctrl+C 停止
```

---

## 步驟九：在 GitHub 建立 Repository

1. 前往 https://github.com/new
2. **Repository name** 填入：`你的帳號.github.io`（例如：`ericchen.github.io`）
3. 選 **Public**
4. **不要**勾選任何額外選項（README、.gitignore、license 都不要）
5. 點「Create repository」

---

## 步驟十：推送到 GitHub

```bash
# 確認在 my-portfolio/ 目錄下
git add .
git commit -m "Initial commit: Hugo site with PaperMod theme"
git branch -M main
git remote add origin https://github.com/你的帳號/你的帳號.github.io.git
git push -u origin main
```

> 第一次推送時 GitHub 會要求登入，輸入你的帳號密碼（或 Personal Access Token）。
> 若遇到密碼驗證問題，去 https://github.com/settings/tokens 建立 Token，勾選 `repo` 權限。

---

## 步驟十一：設定 GitHub Pages 來源

1. 前往 `https://github.com/你的帳號/你的帳號.github.io/settings/pages`
2. 在「**Source**」下拉選單中選擇「**GitHub Actions**」
3. 頁面頂端會出現「GitHub Pages source saved.」

---

## 步驟十二：確認上線

1. 前往 `https://github.com/你的帳號/你的帳號.github.io/actions`
2. 等待最新的 workflow 顯示綠色勾勾（約 30-60 秒）
3. 打開 `https://你的帳號.github.io` 就能看到網站了

---

## 之後的工作流程

### 新增一篇部落格文章

```bash
cd ~/Desktop/my-portfolio

# 方法一：用指令建立（推薦）
hugo new blog/文章名稱.md

# 方法二：直接複製現有文章修改

# 用編輯器打開，撰寫內容
# 完成後把 front matter 的 draft: true 改成 draft: false

# 推送
git add .
git commit -m "新增文章：文章名稱"
git push
# 約 30 秒後網站自動更新
```

### 新增作品

```bash
hugo new projects/作品名稱.md
# 編輯內容 → 改 draft: false → git add . && git commit && git push
```

### 更新主題

```bash
cd ~/Desktop/my-portfolio
git submodule update --remote --merge
git add .
git commit -m "Update PaperMod theme"
git push
```

---

## 常見問題

| 問題 | 解決方法 |
|------|----------|
| 404 Page Not Found | 確認 repo 名稱是 `帳號.github.io`，Pages Source 設為 GitHub Actions |
| 首頁空白或樣式跑掉 | 確認 `hugo.yaml` 的 `baseURL` 結尾有 `/`，且 `theme: PaperMod` 拼寫正確 |
| 大頭照不顯示 | 確認圖片放在 `static/images/profile.jpg`（不是根目錄）|
| Actions 失敗 | 點進 Actions 頁面查看錯誤訊息；最常見原因是 submodule 沒有正確 clone |
| Push 要求輸入密碼 | GitHub 已停用密碼認證，改用 Personal Access Token（去 Settings → Developer settings → Tokens）|
| Hugo 指令找不到 | Windows 需要重新開啟終端機才能使用剛安裝的 Hugo |

---

## 目錄結構總覽

完成後的專案應該長這樣：
```
my-portfolio/
├── .github/
│   └── workflows/
│       └── hugo.yaml          ← GitHub Actions 部署設定
├── archetypes/
│   └── default.md             ← 文章模板
├── content/
│   ├── about/
│   │   └── index.md           ← 關於我頁面
│   ├── blog/
│   │   ├── _index.md          ← 部落格列表頁
│   │   └── hello-world.md     ← 文章
│   ├── projects/
│   │   ├── _index.md          ← 作品集列表頁
│   │   └── 第一個作品.md       ← 作品
│   └── search/
│       └── _index.md          ← 搜尋頁面
├── static/
│   └── images/
│       └── profile.jpg        ← 大頭照
├── themes/
│   └── PaperMod/              ← 主題（自動安裝）
├── .gitignore
├── .gitmodules
└── hugo.yaml                  ← 網站設定檔
```

---

## 快速指令速查

| 用途 | 指令 |
|------|------|
| 本機預覽（含草稿）| `hugo server -D` |
| 本機預覽（正式）| `hugo server` |
| 新增文章 | `hugo new blog/文章名.md` |
| 新增作品 | `hugo new projects/作品名.md` |
| 推送更新 | `git add . && git commit -m "說明" && git push` |
| 更新主題 | `git submodule update --remote --merge && git add . && git commit -m "Update theme" && git push` |
| 查看 Hugo 版本 | `hugo version` |

---

*教學完成。如有問題，可參考 Hugo 官方文件：https://gohugo.io/documentation/*
