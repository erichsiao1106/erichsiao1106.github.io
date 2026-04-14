---
title: "為什麼我花兩個月用 AI 重新學 IC 設計"
date: 2026-04-14
draft: false
description: "8 天 RTL 設計 + 4 個 Claude API 工具——紀錄我怎麼用 AI 把原本 3 個月的學習壓縮進來。"
tags: ["IC Design", "Claude API", "SystemVerilog", "CDC", "MCP"]
showToc: true
---

## 起點：一個讓我坐立難安的問題

「如果 AI 真的可以寫 RTL，IC 工程師還需要懂設計嗎？」

這個問題困擾我很久。不是因為我怕被取代，而是因為我不知道答案。所以我決定用兩個月，親自弄清楚這件事。

---

## 第一個月：重新走過 IC 設計的基礎

我給自己一個挑戰：**8 天內，從零建立一條完整的 IC 前端設計路徑**，包含所有工業界真正在用的技術。

不是用 AI 幫我寫，而是讓 AI 陪我學——查詢、解釋、驗證、討論。

8 天的軌跡大概是這樣：

- **Day 1-2**：同步 FIFO。最好的入門題，有 full/empty 狀態，但邏輯可以很乾淨。
- **Day 3-4**：APB Slave + SVA Assertions。刻意埋了一個 bug，練習 debug 流程。
- **Day 5-6**：**Async FIFO**。這才是真正的關卡。Gray code CDC、2-FF synchronizer——跨時鐘域設計是最容易出 metastability 的地方，也是教科書最容易說不清楚的地方。
- **Day 7**：BRAM 推斷。同樣的 FIFO，換一個寫法，合成面積縮減 83%（390 → 67 cells）。一個 `always_ff` 的細節，差別巨大。
- **Day 8**：Reset CDC + AXI-Lite Crossbar + Coverage-Driven Verification。從單一模組走到系統層級。

最後累積了 27 個 SystemVerilog 檔案、5 份規格文件，還有 8 天的設計日記。

---

## 第二個月：讓 AI 真的融入工具鏈

第一個月驗證了一件事：**AI 不會取代 IC 工程師，但會用 AI 工具的工程師會取代不會用的**。

所以第二個月，我開始用 Claude API 做工具。

### Tool Use + Agentic Loop

第一個工具最簡單也最直接：讓 Claude 自動 debug Verilog。

邏輯是這樣的：給 Claude 幾個工具（compile、simulate、read_file、write_file），讓它自己決定下一步要做什麼。出錯就修，修了再跑，最多 20 輪。整個過程不需要人工介入。

測試下來，大多數語法錯誤和簡單的邏輯 bug，Claude 2-3 輪就能修好。

### MCP Server

Week 2 把那些工具標準化成 MCP（Model Context Protocol）Server。

好處是：不只 Claude，任何支援 MCP 的工具（Cursor、Claude Code）都能直接用這些 EDA 工具。一份程式碼，整個工作流程都通了。

### Spec → RTL 自動生成

最後這個工具讓我最興奮：**把 register map table 直接轉成 APB Slave RTL**。

手工寫一個 register file 要半天——讀 spec、確認地址、處理 read/write 屬性、寫 case statement。用 Tool Use 讓 Claude 結構化解析 table，Python 生成程式碼，1 分鐘搞定。

---

## 結論：AI 改變的不是技術，是速度

兩個月下來，我的答案是：

**AI 不會取代需要深度判斷的設計決策**——CDC 架構選哪種、BRAM 要不要 pipeline、crossbar 的 arbitration 策略，這些還是需要工程師理解原理。

**但 AI 可以把重複性工作壓縮到幾乎為零**——debug、生成 boilerplate、查詢 spec、跑回歸測試，這些佔了工程師大量時間的事情，現在可以自動化。

這就是 RTL-AI-Lab 這個專案想說的事。

---

作品細節在[作品集頁面](/projects/rtl-ai-lab/)，歡迎去看看。
