---
title: "RTL-AI-Lab：用 Claude API 加速 IC 前端設計"
date: 2026-04-14
description: "8 天走完 IC 前端設計全流程，再用 Claude API 打造 EDA 工具鏈——Debug Agent、MCP Server、RAG 查詢、Spec 自動生成 RTL。"
tags: ["SystemVerilog", "Claude API", "MCP", "RAG", "IC Design", "CDC", "AXI"]
showToc: true
TocOpen: true
---

## 專案概述

IC 設計的學習曲線很陡：CDC、APB、AXI-Lite、Coverage-Driven Verification——每個概念都需要時間消化，更需要動手跑過才算真的懂。

這個專案分兩個月：**第一個月**用 Claude Code 輔助，8 天走完一條從基礎 FIFO 到 SoC Fabric 的完整 IC 前端設計路徑；**第二個月**用 Claude API 從頭打造四個 EDA 工具，把重複性工作自動化。

---

## 第一個月：IC 前端設計 8 天

### 設計進展

| Day | 主題 | 核心技術 | 亮點 |
|-----|------|---------|------|
| 1 | 同步 FIFO | MSB-trick pointer | 無計數器的 full/empty 判斷 |
| 2 | 參數化 FIFO | `$clog2()`、parameter | 可重用 IP 設計模式 |
| 3 | APB Slave | APB protocol、register map | 刻意埋 bug 示範 debug 流程 |
| 4 | APB-FIFO Wrapper | SVA Assertions | Formal verification 入門 |
| 5 | **Async FIFO** | Gray code CDC、2-FF sync | Cummings method，業界標準 |
| 6 | AXI-Lite Async FIFO | 雙時鐘 CDC 架構 | 完整 IP 規格書撰寫 |
| 7 | BRAM 推斷 | DP RAM inference pattern | 83% 面積縮減（390 → 67 cells）|
| 8 | 大型系統整合 | Reset CDC、AXI-Lite Crossbar | Coverage-Driven Testbench |

**成果**：27 個 SystemVerilog 檔案、5 份規格文件、8 天設計日記

---

### 技術亮點

#### Gray Code CDC（Day 5 核心）

跨時鐘域是 IC 設計最容易出 metastability bug 的地方。Async FIFO 用 Gray code 指針 + 2-FF 同步器解決：

```systemverilog
// Gray code 轉換：每次只變 1 bit，確保跨域採樣的安全性
assign wptr_gray = wptr_bin ^ (wptr_bin >> 1);

// 2-FF 同步器，每個 clock domain 各一組
always_ff @(posedge rclk or negedge rrst_n) begin
    {wptr_gray_sync, wptr_gray_meta} <= {wptr_gray_meta, wptr_gray};
end

// Full flag 判斷（MSB XOR 法）
assign full = (wptr_gray == {~rptr_gray_sync[ADDR_W:ADDR_W-1],
                               rptr_gray_sync[ADDR_W-2:0]});
```

#### BRAM Inference（Day 7）

同樣的 FIFO，換成 BRAM 版本後面積縮減 83%：

```systemverilog
// 關鍵：registered read，合成器才會推斷成 BRAM
always_ff @(posedge rclk) begin
    if (rd_en) rdata <= mem[raddr];  // ← 這行決定了 BRAM vs distributed RAM
end
// 不能寫 assign rdata = mem[raddr]，那會變成 分散式 RAM
```

**合成結果**：generic 390 cells → iCE40 67 cells（Yosys 合成）

#### Reset CDC（Day 8）

常被忽視但極關鍵的設計，reset 必須「非同步 assert、同步 deassert」：

```systemverilog
always_ff @(posedge clk or negedge rst_n_in) begin
    if (!rst_n_in)
        sync_ff <= '0;         // 非同步清零（立即生效）
    else
        sync_ff <= {sync_ff[SYNC_STAGES-2:0], 1'b1};  // 同步移入
end
assign rst_n_out = sync_ff[SYNC_STAGES-1];
```

---

## 第二個月：Claude API 工具開發

### Week 1：Verilog Debug Agent

讓 Claude 透過 Tool Use 自動完成 compile → simulate → debug 迴圈：

```
User: "幫我 debug async_fifo"
  ↓
Claude: [tool_use: list_files] → 取得檔案清單
  ↓
Claude: [tool_use: compile_verilog] → 取得編譯錯誤
  ↓
Claude: "第 93 行 empty 判斷反了"
  ↓
Claude: [tool_use: write_file] → 修正 → [tool_use: compile_verilog] → PASS
```

最多 20 輪 agentic loop，不需要人工介入。

---

### Week 2：EDA MCP Server

把 Week 1 的工具標準化成 MCP（Model Context Protocol）Server，讓 Claude Code、Cursor 等任何 MCP client 都能直接呼叫：

**6 個 EDA 工具**：
- `list_files` — 列出工作目錄的 RTL 檔案
- `read_file` — 讀取指定檔案內容
- `compile_verilog` — 用 iverilog 編譯，回傳錯誤日誌
- `simulate` — 執行 vvp 模擬，回傳波形和輸出
- `synthesize` — 用 Yosys 合成，回傳 cell 統計
- `report` — 統計分析（面積、timing estimate）

```python
# FastMCP 實作範例
@mcp.tool()
async def compile_verilog(filename: str) -> str:
    """編譯指定的 Verilog/SystemVerilog 檔案"""
    result = subprocess.run(
        ["iverilog", "-g2012", "-o", "/tmp/sim.vvp", filename],
        capture_output=True, text=True
    )
    return result.stdout + result.stderr
```

---

### Week 3–4：Chip Spec RAG

上傳 IC protocol spec（APB、AXI、公司內部文件），讓 Claude 查詢時先搜尋規格書再回答，準確度大幅提升：

- **向量化**：LlamaIndex + FAISS
- **Prompt Caching**：重複查詢省 token 費用

---

### Afternoon Tool：Spec Table → RTL

把 register map table 自動轉成 APB Slave RTL——原本手工半天的工作，1 分鐘完成：

```
輸入：Markdown register map table
  ↓
Claude [tool_use]：結構化解析 table（地址、位元定義、讀寫屬性）
  ↓
Python：根據解析結果生成 SystemVerilog APB slave 模組
  ↓
輸出：可直接用於合成的 RTL（含 testbench）
```

---

## 數字總結

| 指標 | 數量 |
|------|------|
| SystemVerilog 檔案 | 27 個 |
| IC 設計模組 | 10+ 個（FIFO、Async FIFO、APB Slave、AXI-Lite Crossbar 等）|
| IP 規格文件 | 5 份 |
| Python AI 工具 | 4 個（約 1,400 行）|
| BRAM 面積優化 | 83%（390 → 67 cells）|
| Debug Agent 最大迴圈數 | 20 輪 |

---

## 原始碼

[github.com/erichsiao1106/rtl-ai-lab](https://github.com/erichsiao1106/rtl-ai-lab)（整理中）
