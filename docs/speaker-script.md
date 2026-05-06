# 講稿：自動化工作流新範式
> 劉名政 · NKUST 碩專電子一甲 · May 2026  
> 預計總時長：50–60 分鐘｜🟢 = 換頁提示

---

## 開場前準備

進場後先確認：
- `adk web src/muilt-agents` 已開在背景（Ch5 Demo 用）
- `uvicorn server:app --port 8080` 已開（room booking API）
- 瀏覽器開好 ADK Web UI（`http://localhost:8000`）
- 投影片在封面頁待命

---

## 封面頁

> *深呼吸，對著大家微笑*

「大家好，我是劉名政，今天要跟大家聊的是——**會做事的 AI**。

不是那種你問它、它回答你一段話的 AI，而是你說一句話，它自己去查資料、預約會議室、發通知、建行事曆——全部搞定。

這不是未來，這是我這學期做的東西。」

> 🟢 換頁

---

## Ch1 · 開場

### 投影片：三個問題

「在開始之前，我想先問三個問題。」

*(Click 1)* 「第一個問題：你們最常用 AI 幫你做什麼？」

> 停頓 3 秒，讓大家心裡想

「大概是——寫 email、查資料、改程式碼，對嗎？」

*(Click 2)* 「第二個問題：AI 幫你『查好資料』之後，你還需要做什麼？」

> 停頓

「你還是要自己複製貼上、自己整理、自己發出去。它只是給了你**建議**，動作還是你在做。」

*(Click 3)* 「第三個問題：如果 AI 不只給建議，而是幫你把後面那些步驟也做掉——你的工作會變成什麼樣？」

「**這就是 AI Agent 想解決的事。**」

> 🟢 換頁

---

### 投影片：同一個需求，兩種世界

「我舉一個例子。業務說：我想知道上個月 Top 10 客戶是誰。」

*(逐步 click 左邊)*

「傳統做法——找資料庫管理員、等他們出 report、等 IT 幫忙、去找 BI 工具、寫 SQL、匯出 Excel……最後回到步驟一，因為需求改了。」

> 可以笑著說：「大家是不是都有這種經驗？」

*(右邊整塊出現)*

「Agent 的做法：你說一句話，它自己去查資料庫、整理、回你答案。

重點不是快，是**節奏改變了**——你不再需要轉手給別人。」

> 🟢 換頁

---

### 投影片：你會帶走三件事

「今天結束後，我希望你帶走三件事：

第一，**理解**什麼是真正的 AI Agent，不是 Chatbot。

第二，**看過** ADK + MCP 怎麼讓 Agent 連上企業系統。

第三，**能判斷**你自己的工作場景，有沒有機會導入 Agent。

如果你只記得一件事——希望是第三點。」

> 🟢 換頁

---

## Ch2 · AI Agent 核心概念

### 投影片：章節過場

「我們先退一步，把 LLM 和 Agent 講清楚。因為這兩個詞很多人混著用，但它們本質上差很多。」

> 🟢 換頁

---

### 投影片：LLM vs Agent

「我把它們畫在同一張紙上。」

*(Click 1-3 左邊 LLM)*

「LLM 是這樣運作的：你輸入問題，它的大腦想一想，輸出答案。**單向，結束。**

它用的是訓練時學到的知識，沒辦法查今天的資料，給了答案就結束了。」

*(Click 4 右邊 Agent)*

「Agent 是這樣：它有大腦、有手腳、有記憶。

它會**想**、**行動**、**觀察結果**、再**想**、再**行動**——一直到任務完成。

這個循環叫 ReAct pattern——Reasoning + Acting。

一句話：**LLM 只有大腦；Agent 有大腦、有手腳、有記憶。**」

> 🟢 換頁

---

### 投影片：四大組件

「拆解一個 Agent，它有四個核心組件：

- **Brain（大腦）**：就是 LLM，負責理解和推理
- **Tools（工具）**：Python function、API、資料庫——Agent 的手腳
- **Memory（記憶）**：短期記憶是對話歷史，長期記憶是向量資料庫
- **Orchestration（協作）**：如何安排多個 Agent 分工

今天我們主要講前兩個：用 ADK 把 Brain 和 Tools 接起來。」

> 🟢 換頁

---

### 投影片：四道門檻

「好，那自己做 Agent 難不難？

我從自己的經驗整理出四道門檻——

*(逐一 click)*

**第一道：Observable（可觀測）**——你怎麼知道 Agent 在想什麼？它做了什麼決定？出錯了怎麼 debug？

**第二道：Governable（可治理）**——怎麼防止它做不該做的事？怎麼設權限？

**第三道：Composable（可組合）**——一個 Agent 搞不定複雜任務，怎麼讓多個 Agent 分工？

**第四道：Deployable（可部署）**——Demo 跑起來了，怎麼上線給真實用戶用？

這四道門檻，就是接下來 ADK 要幫我們解決的事。」

> 🟢 換頁

---

## Ch3 · Agent Development Kit (ADK)

### 投影片：章節過場

「我們剛剛列了四道門檻，Google 想：乾脆我做一套框架幫大家。這就是 ADK。」

> 🟢 換頁

---

### 投影片：為什麼選 ADK？

「市場上有很多選擇，我先告訴你三條路：」

*(Click 1)* 「**自己刻**——很多團隊從這裡開始，完全可控，但四道門檻全部要自己扛。原型做得快，生產環境做得很慢。」

*(Click 2)* 「**LangChain**——社群最廣，整合最多，是目前最流行的選項。但它抽象層很深，debug 很痛苦。它是一把通用瑞士刀，不是生產線機器。」

*(Click 3)* 「**ADK**——Google 官方，從第一天就為生產環境設計。Gemini 原生優化，Cloud Run、Vertex AI 直接整合。

ADK 不是另一個 AI 玩具——**它是為「第一天就要上線」設計的生產工具。**」

> 🟢 換頁

---

### 投影片：三根支柱

「ADK 有三個設計哲學：」

*(Click 1)* 「**Code-first**——用 Python 寫 Agent，不是拖 UI、不是填 YAML。IDE 自動完成、斷點除錯、Git 版本控制，工程師熟悉的工具全都能用。」

*(Click 2)* 「**Model-agnostic**——雖然出自 Google，不綁 Gemini。OpenAI、Claude、Ollama 本地模型，都能跑。模型市場變化很快，今天最好的不代表明天最好，所以不能綁死。」

*(Click 3)* 「**Deployment-ready**——`adk deploy cloud_run` 一行搞定。Session 管理、認證、Trace 都幫你接好了。Demo 做完隔天就能上線。

一句話總結：**工程師友好 + 不綁廠商 + 馬上能上線。**」

> 🟢 換頁

---

### 投影片：五個主角

「ADK 的世界裡有五個主角，看懂這張圖，任何 ADK 程式碼你都能讀懂。」

*(Click 1)* 「**Runner（導演）**——統籌整場，把 user 輸入餵給 Agent，管生命週期。

*(Click 2)* **Agent（主角）**——綁定 LLM、instruction、可用的 tools。

*(Click 3)* **Tool（道具）**——Python function、API、或 MCP 工具，Agent 的手腳。

*(Click 4)* **Session（劇本）**——對話上下文與狀態的容器，重開也能接續。

*(Click 5)* **Callbacks（場務）**——before_tool、after_model 等鉤子，做審計、改寫、權限檢查。

我最喜歡用電影劇組打比方：Runner 是導演、Agent 是主角、Tools 是道具、Session 是劇本、Callbacks 是場務。」

> 🟢 換頁

---

### 投影片：10 行程式

「現在看程式碼。這是 ADK 的 Hello World。」

*(Step 1)* 「三行就是一個 Agent：`model` 選腦、`instruction` 給人設、`name` 給身份。對比自己用 OpenAI SDK 大概要 20-30 行。」

*(Step 2)* 「加一個工具——**普通 Python function 就是 tool**。沒有 decorator、沒有 JSON schema、沒有手動註冊。

注意：docstring 很重要，LLM 讀它決定要不要呼叫這個工具。type hint 會自動變成 function calling schema。」

*(Step 3)* 「交給 Runner 執行。ReAct 循環、tool 呼叫、結果回灌 LLM——全部內建，你只要 `async for`。

**沒有 ChatCompletion 迴圈、沒有手寫 tool schema、沒有 function-call 解析——ADK 幫你處理掉了。**」

> 🟢 換頁

---

### 投影片：三種 Workflow Agent

「一個 Agent 不夠？ADK 內建三種組合方式：」

*(Click 1)* 「**Sequential（一棒接一棒）**——前一個 Agent 的輸出是下一個的輸入。適合文件審核、多階段推理。」

*(Click 2)* 「**Parallel（同時派工）**——多個 Agent 同時跑，各自查不同資料來源。適合加速查詢、多觀點投票。」

*(Click 3)* 「**Loop（反覆修）**——重複執行直到品質達標。適合自動 QA、程式碼自我修正。

結尾重點：這三種加上下一張的委派模式，**像樂高一樣堆出複雜流程**，不用自己寫排程器。」

> 🟢 換頁

---

### 投影片：Manager & Sub-Agents *(新增)*

「這是今天 Demo 用的實際架構，叫做**委派模式**。

跟 Sequential 不一樣——Sequential 是死板的順序，sub_agents 是**動態判斷**：Manager 根據使用者說的話，決定叫哪個 Agent、什麼時候叫、叫幾次。

*(Click 1)* root_agent 是 Manager，用 Gemini 做精確的路由判斷。

*(Click 2)* 底下四個專員各自有自己的 model 和 tools。

程式碼很簡單：`Agent(sub_agents=[...])` 就好了。ADK 內建 `transfer_to_agent` 工具，Manager 呼叫它就能把控制權移交給子 Agent。

**一個很重要的點：各 Agent 可以用不同模型。** Manager 用 Gemini 做精確路由，sub-agents 可以用本地 Ollama 節省成本——這是真實場景中的重要優化。」

> 🟢 換頁

---

### 投影片：Ch3 Recap

「Ch3 三個帶走：

一、ADK 是為生產設計的框架，不是玩具。

二、五個主角：Runner 導演、Agent 主角、Tool 道具、Session 劇本、Callbacks 場務。

三、複雜流程用 Workflow Agent 組，像樂高。

現在問題來了：Agent 的手腳——Tool——從哪來？下一章，MCP。」

> 🟢 換頁

---

## Ch4 · MCP 與 MCP Toolbox

### 投影片：章節過場

「ADK 幫我們解決了大腦的問題。但大腦需要手腳，手腳就是 Tool。

工具接起來有一個大麻煩——」

> 🟢 換頁

---

### 投影片：整合地獄

「接一個 Slack 要一套 SDK，接一個資料庫要另一套，接 Google Calendar 又是一套。

N 個模型 × M 個資料來源 = 噩夢。

更慘的是：如果你今天想從 Gemini 換到 Claude，所有 Tooling 都要重寫。

**我們需要 AI 界的 USB 接口。**」

> 🟢 換頁

---

### 投影片：MCP — AI 時代的 USB

「這就是 MCP——Model Context Protocol，Anthropic 在 2024 年底提出的開放標準。

概念很簡單：不管哪個 AI 模型，不管接哪個資料來源，都用同一個協議說話。

就像 USB——手機、硬碟、鍵盤，插同一個孔，電腦不需要知道裡面是什麼。

MCP 之後，**模型只需要實作一次 MCP Client，就能用所有 MCP Server 的工具。**」

> 🟢 換頁

---

### 投影片：理想與現實

「但……現實是這樣的：

你自己跑 MCP Server，Secret 怎麼管？工具權限怎麼控制？誰用了哪個工具怎麼稽核？出問題怎麼 debug？

企業要的不是一個 protocol，而是一個**管理平台**。

這就是 MCP Toolbox 出現的原因。」

> 🟢 換頁

---

### 投影片：MCP Toolbox

「MCP Toolbox 是 Google 做的**企業級 MCP 管理平台**。

它幫你解決了：
- Secret 安全託管（不用把 API key 寫死在程式碼裡）
- 工具粒度控制（只開放特定工具，不是全部）
- 即時監控（誰在用哪個工具、傳了什麼參數）

對 ADK 來說，接上 MCP Toolbox 只是**一個 URL 的距離**。」

*(Click 4 程式碼出現)*

「你看，`MCPToolset` 傳一個 URL 就接上了我們自己的石化督導資料庫——實際上後面跑的是 MSSQL，有幾千筆督導案件資料。」

> 🟢 換頁

---

### 投影片：Ch4 Recap

「ADK + MCP Toolbox = 完整解決方案。

ADK 負責 Agent 邏輯——如何思考、如何對話、如何協調。

MCP Toolbox 負責基礎設施——如何連接、如何安全、如何監控。

兩者通過 MCP 協議對接。」

> 🟢 換頁

---

## Ch5 · Live Demo

### 投影片：章節過場

「理論夠了，現在來看真的。」

> 🟢 換頁

---

### 投影片：Demo 目標

「我們的 Demo 分三個層次：

Phase 1：Python function 變成 Agent 的工具。

Phase 2：連上 MCP Toolbox，查真實資料庫。

Phase 3：多個 Agent 分工，完成完整的預約流程。

場景：*幫我查有沒有空的會議室，有的話幫我預約，然後在 Discord 通知。*」

> 🟢 換頁

---

### 投影片：Phase 01

*(切換 Magic Move 程式碼)*

「Step 1：定義一個 Python function。這就是工具，沒有任何特殊語法。

Step 2：把它塞進 Agent 的 `tools` 列表。docstring 就是工具說明書。

Step 3：交給 Runner 執行。

你看右邊的 trace——Agent 收到問題，思考，呼叫工具，得到結果，回答。這個 ReAct 循環是自動的。

Phase 2 的時候，我們把工具換成 MCPToolset，接上石化督導資料庫——它查的就是真實的 MSSQL，`getOrganizationStats`、`get-improvement-progress` 這些都是真實跑過的。」

> 🟢 換頁

---

### 投影片：Phase 02 — MCP Toolbox 實戰

「現在連到真實世界。

*(指著 MCP Toolbox 面板)*

這個是我們公司自己架的 MCP Toolbox，裡面有石化督導系統和 KPI 系統的工具。

有一個很重要的功能——Secret Manager。你看這裡，API token 是加密的，Agent 用工具的時候 token 自動帶入，不會出現在程式碼或 log 裡。

這對企業來說非常重要：**工具能用，但不能看到密碼。**」

> 🟢 換頁

---

### 投影片：Phase 03 — Multi-Agent 架構

「現在來看今天的重頭戲。」

*(打開 ADK Web UI，選 root_agent)*

「這是我用 ADK 建的四人專員團隊。

*(Click 1)* root_agent 是 Manager，用 Gemini，負責判斷和路由。

*(Click 2-6)* 底下有：
- room_agent：查會議室狀態
- book_agent：執行預約
- search_agent：網路搜尋
- alert_agent：建 Google 行事曆 + 發 Discord 通知

**讓我直接示範：** 我輸入——『早安，有空的會議室嗎？』

*(在 ADK Web UI 輸入)*

你看 trace：root_agent 收到，判斷需要查房間，`transfer_to_agent` 到 room_agent，room_agent 呼叫工具，得到結果，回來給 Manager，Manager 整理回答你。

整個過程透明可見，這就是 Observable 的意義。」

> 🟢 換頁

---

### 投影片：Demo 重點總結

「Demo 三個收穫：

一、**定義即功能**——Python function 不需要任何複雜修飾。

二、**隨插即用的 MCP 生態**——MCPToolset 接一個 URL，背後是企業 MSSQL。

三、**Multi-Agent 的力量**——複雜業務流程拆成多個角色分工，每個角色只做一件事，但合在一起能完成很複雜的任務。」

> 🟢 換頁

---

## Ch6 · Deploy & Scale

### 投影片：章節過場

「有了 Agent，下一步是——怎麼讓它上線？怎麼讓它不出事？」

> 🟢 換頁

---

### 投影片：兩條部署路線

「ADK 提供兩條路：

**Cloud Run**——你控制 infra，Docker 容器，`adk deploy cloud_run` 一行搞定。彈性高，適合有特殊需求的情境。

**Vertex AI Agent Engine**——完全 managed，不用管 server。Auto-scale、Session 持久化、監控全都幫你處理。適合快速上線。

兩條路都是 `adk deploy` 一行指令，不需要手寫 Kubernetes。」

> 🟢 換頁

---

### 投影片：治理與 Callbacks

「Agent 上線了，怎麼防止它做不該做的事？

答案是 Callbacks——ADK 的生命週期鉤子。

**事前過濾**：`before_model_callback`——請求進來時，檢查有沒有 PII、敏感詞。

**事中稽核**：`before_tool_callback`——Agent 要呼叫工具時，攔截、記錄審計日誌，甚至可以擋下來。

**事後清洗**：`after_model_callback`——輸出前，確保沒有機密資訊外洩。

你在我們的 sql_agent 裡看到的 `before_tool_callback=confirm_sensitive_tools`，就是這樣用的——查 KPI 資料之前要先確認使用者有權限。」

> 🟢 換頁

---

### 投影片：可觀測性

「最後，可觀測性。

ADK Web UI 你剛剛看到了——每一個 event、每一次 tool call、每一輪 LLM 思考，全部有 trace。

部署到 Vertex AI 之後，還能整合 Cloud Monitoring 和 Cloud Logging，做 alerting 和 cost analysis。

**不透明是 AI 上線最大的風險。** ADK 從設計上就把這件事解決掉了。」

> 🟢 換頁

---

## Ch7 · 收尾

### 投影片：全景回顧

「讓我們把今天串連起來。

*（指著投影片）*

**LLM**——大腦，推理能力。

**ADK**——讓 LLM 有手腳、有記憶、能協調、能部署。

**MCP Toolbox**——讓 Agent 安全地連上所有企業系統。

這三層疊在一起，就是今天演講的全部。」

> 🟢 換頁

---

### 投影片：Agentic Era

「我想用一個觀點收尾。

我們正在從『AI 助理時代』走向『Agentic 時代』。

以前：你問 AI，AI 給建議，你執行。

現在：你描述目標，Agent 自己計畫、執行、回報。

這不只是技術變化，是**工作流程的根本重構**。

很多現在需要人轉手的流程——查資料、填表、發通知、更新系統——Agent 都可以接管。

**你的機會，不是學會用 AI，而是學會設計用 AI 工作的系統。**」

> 🟢 換頁

---

### 最後一頁

「謝謝大家。

程式碼和今天的投影片我都會放在 GitHub，有興趣的同學可以拿去跑。

如果有問題，現在或課後都可以找我。」

> *鞠躬，等待提問*

---

## Q&A 備用答案

**Q：Ollama 的 function calling 不穩定，怎麼辦？**
> 用 `openai/` provider 走 Ollama 的 `/v1/chat/completions` 接口，繞過 LiteLLM 的 Ollama-specific 處理，大幅提升穩定性。

**Q：這套東西能不能用在自己的公司？**
> 完全可以。MCP Toolbox 支援 PostgreSQL、MySQL、MSSQL、BigQuery、Cloud SQL，幾乎所有主流資料庫。

**Q：費用怎麼算？**
> ADK 本身是免費的。Gemini API 有免費額度，生產環境的費用主要看 token 用量。如果用 Ollama 本地模型做 sub-agents，可以大幅降低費用。

**Q：Multi-Agent 這麼複雜，值得嗎？**
> 當單一 Agent 開始出現「工具太多、指令太長、任務太複雜」的問題，就是 Multi-Agent 的時機。簡單任務用單一 Agent，複雜業務流程用 Multi-Agent。

---

*加油！你做的東西很厲害，講出去就好了。🎤*
