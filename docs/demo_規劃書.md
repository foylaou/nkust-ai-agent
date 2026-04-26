# AI Agent Workshop · Demo 實戰規劃書

本文件定義了 **Chapter 5 · Live Demo** 的具體執行流程與代碼實作規劃。

## 0. Demo 核心場景
**「企業行政小幫手」**：透過自然語言指令，自動處理跨系統的會議室查詢、日曆預約與通訊通知。
> **指令範例：** 「幫我查一下明天下午兩點的會議室有沒有空，如果有的話幫我約起來，並在 Slack 通知主管。」

---

## 1. 階段一：Local Agent (最小可行性演示)
**目標：** 展示 ADK 如何快速將 Python Function 轉換為 Agent 的工具技能。

### 核心功能
- **工具 (Tool)：** `get_room_status(time: str)`
- **邏輯：** 模擬查詢本地資料庫或檔案，回傳會議室狀態。

### 實作要點
- 展示 `docstring` 如何自動變成 LLM 的工具說明書。
- 展示 `Agent` 物件的初始化與 `tools=[get_room_status]` 的簡單封裝。

---

## 2. 階段二：MCP Power (企業級連接演示)
**目標：** 展示如何透過 MCP Toolbox 輕鬆連接外部 SaaS 生態（Slack / Calendar）。

### 核心功能
- **連接器 (Connectors)：** 
    1. **Google Calendar MCP Server**: 負責執行 `create_event`。
    2. **Slack MCP Server**: 負責執行 `send_message`。
- **治理特點：** 強調 API Key 託管於 MCP Toolbox (Secret Manager)，Agent 程式碼中完全不落地。

### 演示流程
1. 開啟 MCP Toolbox UI 介面，展示已連線的 Slack 與 Calendar Server。
2. 在 ADK 代碼中使用 `McpTool(url=...)` 引用這些遠端工具。
3. 執行 Agent，觀察其如何「自發性」決定呼叫日曆與 Slack。

---

## 3. 階段三：Multi-Agent Orchestration (複雜流程協作)
**目標：** 展示將複雜任務拆解給多個專業 Agent 的「團隊運作」模式。

### 角色分配
1. **Searcher (查詢員)**: 專精於解析時間並確認空間可用性。
2. **Booker (預約員)**: 專精於串接日曆 API 並處理預約衝突。
3. **Notifier (通知員)**: 專精於根據結果撰寫格式化的 Slack 訊息。

### 實作架構
- 使用 ADK 的 `SequentialAgent` 或 `ParallelAgent`。
- 展示 **Shared Session State**: Searcher 查到的 `room_id` 如何自動傳遞給 Booker，無需開發者手動串接變數。

---

## 4. 環境準備清單 (Pre-requisites)

### 技術棧
- **Framework**: `google-adk`
- **Model**: `gemini-2.0-flash`
- **Protocol**: `MCP (Model Context Protocol)`
- **Platform**: `MCP Toolbox` (Managed Service)

### 必要金鑰 (Secrets)
- `GOOGLE_API_KEY` (Gemini)
- `SLACK_BOT_TOKEN` (存於 MCP Toolbox)
- `GOOGLE_CALENDAR_CREDENTIALS` (存於 MCP Toolbox)

---

## 5. Demo 成功指標
1. **零 Schema 開發**：全程不撰寫 JSON Schema，僅使用 Python 原生定義。
2. **跨系統閉環**：指令下達後，實體 Slack 頻道收到通知，日曆出現新活動。
3. **透明可追蹤**：透過 ADK Trace 介面清楚看到 Agent 的思考 (Thought) 與行動 (Action) 軌跡。



## demo prompt list
"""
早安 有空的會議室嗎？
我是foy 預計會有5人到場來開會 會議名稱是設計會議
我是enzo預計會有16人到場來開會 會議名稱是後端開發會議
我是tim預計會有8人到場來開會 會議名稱是前端端開發會議
"""