---
title: "準備 AI 工程師面試：API 整合和 Fine-tuning 我踩過的坑"
date: 2026-04-14
draft: false
description: "從 Rate Limit 到 LoRA，從 Prompt Caching 到 Fine-tuning vs RAG 的選擇框架——這是我實際寫過程式之後整理的筆記，不是教科書。"
tags: ["Claude API", "Fine-tuning", "LoRA", "RAG", "AI Engineering", "面試準備"]
showToc: true
TocOpen: false
---

## 前情提要

在 RTL-AI-Lab 的第二個月，我花了兩週時間密集整理 AI 工程師面試會問到的東西。

不是因為我要換工作，而是因為我發現：我雖然用了很多 Claude API，但很多底層的東西我說不清楚。Rate limit 怎麼處理？Streaming 為什麼存在？Fine-tuning 和 RAG 到底什麼時候選哪個？

這篇文章是我實際寫過程式、踩過坑之後整理出來的，不是翻教科書。

---

## 一、API 整合：在正式環境裡用 AI 的四個關卡

### 關卡 1：Rate Limit

第一次遇到 HTTP 429 的時候我以為是我的程式壞了。後來才懂——Rate Limit 不是 bug，是設計。

正確處理方式是**指數退避（Exponential Backoff）**：第一次失敗等 1 秒，第二次等 2 秒，第三次等 4 秒，以此類推，中間加一點隨機 jitter 避免所有 client 同時重試：

```python
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
import anthropic

@retry(
    wait=wait_exponential(multiplier=1, min=1, max=60),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type(anthropic.RateLimitError)
)
def call_claude(prompt: str) -> str:
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text
```

手寫 retry loop 也可以，但用 `tenacity` 套件更乾淨，面試的時候說你用 `tenacity` 比手寫更加分。

---

### 關卡 2：Streaming

為什麼要 Streaming？

因為 Claude Opus 加上 extended thinking 有時候要跑 2 分鐘以上。如果你用一般的同步請求，連線很容易 timeout，使用者也只能看著空白頁面等。

用 Streaming 可以邊產生邊顯示，使用者看到文字一個字一個字出來，體感快很多：

```python
with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=2048,
    messages=[{"role": "user", "content": prompt}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)  # 邊收邊印

# 結束後取得完整 usage 統計
final_message = stream.get_final_message()
print(f"\n輸入 tokens: {final_message.usage.input_tokens}")
print(f"輸出 tokens: {final_message.usage.output_tokens}")
```

---

### 關卡 3：Prompt Caching（這個最省錢）

這是我覺得最值得花時間搞懂的功能。

場景：你有一份很長的 IC spec 文件（5000 tokens），每次問問題都要把它放進 prompt。如果每天問 100 次，光 input tokens 的費用就很可觀。

Prompt Caching 可以讓 Claude 把常用的長 context 快取 5 分鐘。第一次讀完整 context，之後 5 分鐘內的請求只讀 cache，費用省約 **90%**。

```python
# 把 spec 文件標記為可快取
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": long_spec_document,   # 你的 5000 token spec
            "cache_control": {"type": "ephemeral"}  # ← 加這個
        }
    ],
    messages=[{"role": "user", "content": "請問 APB write 流程是什麼？"}]
)

# 看 cache 有沒有命中
usage = response.usage
print(f"cache 命中: {usage.cache_read_input_tokens} tokens")
print(f"cache 未中: {usage.cache_creation_input_tokens} tokens")
```

第一次請求建立 cache，之後的請求 `cache_read_input_tokens` 會有值，費率是正常 input 的 10%。

---

### 關卡 4：Async 並行

同步呼叫 10 個問題要 20 秒，`asyncio.gather` 並行呼叫只要 2 秒。

```python
import asyncio
import anthropic

async def ask_single(client, question: str) -> str:
    message = await client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        messages=[{"role": "user", "content": question}]
    )
    return message.content[0].text

async def ask_parallel(questions: list[str]) -> list[str]:
    client = anthropic.AsyncAnthropic()
    # 同時跑所有請求
    results = await asyncio.gather(
        *[ask_single(client, q) for q in questions]
    )
    return results
```

如果怕打爆 rate limit，加 `asyncio.Semaphore` 限制同時最多幾個請求：

```python
async def ask_with_limit(questions: list[str], max_concurrent: int = 3):
    client = anthropic.AsyncAnthropic()
    semaphore = asyncio.Semaphore(max_concurrent)

    async def ask_one(q):
        async with semaphore:  # 最多 3 個同時跑
            return await ask_single(client, q)

    return await asyncio.gather(*[ask_one(q) for q in questions])
```

---

## 二、Fine-tuning：大部分時候你不需要它

這是我做完這段研究後最大的收穫：**大多數問題不需要 fine-tuning**。

### 三種方法的選擇框架

| 方法 | 適合的場景 | 不適合的場景 |
|------|-----------|------------|
| **Prompt Engineering** | 試所有方法的第一步，大多數問題在這裡就解決了 | 知識量超過 context 長度限制 |
| **RAG** | 需要查詢即時或大量文件（spec、規格書、公司資料）| 需要改變模型的「行為模式」或輸出風格 |
| **Fine-tuning** | 想讓模型輸出特定格式、學特定術語、有一致風格 | 用來補充「知識」（RAG 更適合這個）|

一個記法：

> **「知識」用 RAG，「行為」用 Fine-tuning，先試 Prompt Engineering。**

比如我想讓 Claude 每次都用特定的 register map 格式輸出，這是「行為」→ Fine-tuning 合適。但如果我想讓 Claude 懂我們公司的 spec 文件，這是「知識」→ RAG 更好，因為 spec 會更新。

---

### LoRA 是什麼，為什麼存在

Fine-tuning GPT-3（1750 億參數）需要 700GB 顯存。沒有人負擔得起。

LoRA（Low-Rank Adaptation）的想法很優雅：**不要動原始的 weight，在旁邊插兩個小矩陣。**

原理：原始 weight matrix W 是 `d × d` 的大矩陣，LoRA 插入兩個矩陣 B（`d × r`）和 A（`r × d`），其中 rank `r` 遠小於 `d`。

```
更新後的 weight = W + B × A
```

訓練時只更新 B 和 A，W 完全凍結。

實際參數量：以 Llama-7B（70 億參數）為例：
- Full fine-tuning：70 億個參數要更新
- LoRA（r=16）：大概 3000 萬個參數，**只有原來的 0.4%**

效果呢？在大多數任務上接近 full fine-tuning，但顯存需求低 10 倍以上。

```python
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(
    r=16,              # rank，越小越省，但效果也越小，通常 4-16
    lora_alpha=32,     # scaling factor，通常設 2*r
    target_modules=["q_proj", "v_proj"],  # 對 attention 層做 LoRA
    lora_dropout=0.1,
    bias="none"
)

model = get_peft_model(base_model, lora_config)
model.print_trainable_parameters()
# 輸出：trainable params: 0.4% || all params: 100%
```

---

### 面試的時候怎麼說

面試官問「Fine-tuning 和 RAG 怎麼選」，不要說「要看情況」（廢話），要說出決策流程：

> 「我會先問：這是知識問題還是行為問題。如果是需要查詢文件或最新資料，RAG 比較合適，因為知識可以隨時更新，不需要重新訓練。如果是要讓模型輸出特定格式、學特定風格或術語，才考慮 fine-tuning。然後兩個都試之前，我會先確認 prompt engineering 解不解得了，因為那是成本最低的做法。」

這樣回答展示了你有決策框架，不是隨機亂試。

---

## 後記

做完這兩週的研究，我最大的感受是：**AI 工程和 IC 設計有一個共同點——細節決定能不能用在生產環境。**

FIFO 的 gray code 指針如果沒做好，metastability 會在某個特定頻率出現。API 的 retry 邏輯如果沒做好，高流量的時候系統會自己打爆自己。

原理懂了之後，這些細節就不再是「碰運氣」，而是有跡可循的工程決策。

---

相關程式碼在 [rtl-ai-lab/second_month/interview_prep](https://github.com/erichsiao1106/rtl-ai-lab)（整理中）。
