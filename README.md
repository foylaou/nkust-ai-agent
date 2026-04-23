# 🚀 AI Agent Workshop · Demo 執行指南

本指南對應 `docs/demo_規劃書.md` 的三個實作階段，配合 `src/` 底下的程式碼進行演示。

---

## 🏗️ 準備工作 (Pre-requisites)

1. **啟動即時看板 (Dashboard)**
   所有 Demo 階段都需要啟動此服務，以即時看到會議室預約狀態。
   ```bash
   python src/server.py
   ```
   - 瀏覽器打開：`http://localhost:8000/`

---

## 🟢 階段一：Local Agent (最小可行性演示)
**目標：** 展示如何將 Python Function 快速轉換為 Agent 的工具技能。

1. **啟動 Agent：**
   ```bash
   python src/agent.py
   ```
2. **Demo 指令範例：**
   - `幫我查一下現在有哪些空房間？`
   - `幫我預約 A101，我的名字叫 Foy。`
3. **技術亮點：**
   - **Schema-free**：開發者只需寫好 Python docstring，Gemini 就能理解工具用途。
   - **視覺化反饋**：Agent 執行成功後，Dashboard 會立即變色。

---

## 🔵 階段二：MCP Power (企業級連接演示)
**目標：** 展示透過 MCP 協定，Agent 如何輕鬆連動外部 SaaS (Slack/Calendar)。

1. **啟動 Agent：**
   ```bash
   python src/agent_mcp.py
   ```
2. **Demo 指令範例：**
   - `幫我找一間 20 人的大會議室並幫我約起來，我叫 Foy 會議名稱是大型石化督導會議 4/28 早上8點到中午12點。並通知所有人到場`
   - `預約成功後，發 Slack 訊息給 #admin 頻道通知大家，並在我的日曆上記下這件事。`
3. **技術亮點：**
   - **跨系統閉環**：一個指令觸發本地看板、Slack 通知與 Google 日曆。
   - **安全治理**：強調金鑰託管於 MCP Toolbox，程式碼不落地。

---

## 🔴 階段三：Multi-Agent Orchestration (多代理人協作)
**目標：** 展示複雜任務拆解與「團隊運作」模式。

1. **啟動 Agent：**
   ```bash
   python src/multi_agent.py
   ```
2. **Demo 指令範例：**
   - `我需要一間能坐 5 個人的房間。找到後幫我預約，我叫 Foy，最後記得發送通知。`
3. **技術亮點：**
   - **角色化思考 (Agentic Reasoning)**：Agent 會主動說明現在是由 Searcher 查詢、Booker 預約。
   - **共享上下文 (Shared State)**：Agent 團隊會自動傳遞房間 ID 與預約資訊，無需人工干預。

---

