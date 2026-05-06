---
# ========================================
#  Chapter 3 · Agent Development Kit (ADK)
# ========================================
layout: section
class: bg-slate-950 text-white
---

<div class="text-xs uppercase tracking-[0.3em] text-blue-400 mb-3">Chapter 03</div>

# Agent Development Kit (ADK)

<div class="text-white/60 mt-2">Google 的 Agent 開發框架</div>

<!--
講者備註：
- 章節過場，從 Ch2 的四道門檻自然接過來
- 開場白：「我們剛剛列了四道門檻，Google 想：乾脆我做一套框架幫大家」
-->

---
layout: default
class: bg-slate-950 text-white
transition: slide-left
---

<div class="h-full flex flex-col py-2 px-6">

<div class="text-center mb-4">
<div class="text-xs uppercase tracking-[0.3em] text-blue-400 mb-1">The Landscape</div>
<h2 class="text-2xl font-light text-white !my-0">既然要用框架，為什麼是 ADK？</h2>
<div class="text-sm text-white/50 mt-1 italic">三條路攤在你面前</div>
</div>

<div class="grid grid-cols-3 gap-4 flex-1 min-h-0">

<!-- Path 1 · DIY -->
<div v-click="1" class="flex flex-col bg-slate-900/60 border border-slate-700/50 rounded-xl p-4 shadow">
<div class="flex items-center gap-2 mb-3">
<div class="text-2xl">🧱</div>
<div>
<div class="text-[10px] uppercase tracking-wider text-slate-400">Path 1</div>
<div class="text-base font-semibold text-white">自己刻</div>
</div>
</div>

<div class="text-xs text-white/70 leading-relaxed mb-3 flex-1">
直接呼叫 OpenAI / Gemini API，自己寫 tool 呼叫、記憶、重試、日誌。
</div>

<div class="space-y-1 text-[11px] border-t border-slate-700/50 pt-2">
<div class="flex items-center gap-2"><span class="text-emerald-400">✓</span><span class="text-white/70">完全可控</span></div>
<div class="flex items-center gap-2"><span class="text-red-400">✕</span><span class="text-white/70">4 道門檻全自己扛</span></div>
<div class="flex items-center gap-2"><span class="text-red-400">✕</span><span class="text-white/70">原型快、生產慢</span></div>
</div>
</div>

<!-- Path 2 · LangChain -->
<div v-click="2" class="flex flex-col bg-slate-900/60 border border-slate-700/50 rounded-xl p-4 shadow">
<div class="flex items-center gap-2 mb-3">
<div class="text-2xl">🔗</div>
<div>
<div class="text-[10px] uppercase tracking-wider text-slate-400">Path 2</div>
<div class="text-base font-semibold text-white">LangChain / LlamaIndex</div>
</div>
</div>

<div class="text-xs text-white/70 leading-relaxed mb-3 flex-1">
開源生態最廣，抽象層豐富，社群資源多。適合做 prototype 和 RAG。
</div>

<div class="space-y-1 text-[11px] border-t border-slate-700/50 pt-2">
<div class="flex items-center gap-2"><span class="text-emerald-400">✓</span><span class="text-white/70">社群龐大、整合廣</span></div>
<div class="flex items-center gap-2"><span class="text-amber-400">△</span><span class="text-white/70">抽象層深、debug 難</span></div>
<div class="flex items-center gap-2"><span class="text-amber-400">△</span><span class="text-white/70">部署與治理要自己接</span></div>
</div>
</div>

<!-- Path 3 · ADK (強調) -->
<div v-click="3" class="relative flex flex-col bg-gradient-to-br from-blue-900/50 to-indigo-900/50 border-2 border-blue-400 rounded-xl p-4 shadow-xl shadow-blue-500/20">
<div class="absolute -top-2.5 right-3 bg-blue-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full tracking-wider">RECOMMENDED</div>

<div class="flex items-center gap-2 mb-3">
<div class="text-2xl">🚀</div>
<div>
<div class="text-[10px] uppercase tracking-wider text-blue-300">Path 3 · 今天主角</div>
<div class="text-base font-semibold text-white">Agent Development Kit</div>
</div>
</div>

<div class="text-xs text-white/80 leading-relaxed mb-3 flex-1">
Google 官方打造，<span class="text-blue-300 font-semibold">從第一天就為 Production 設計</span>。內建 4 道門檻所需工具。
</div>

<div class="space-y-1 text-[11px] border-t border-blue-400/30 pt-2">
<div class="flex items-center gap-2"><span class="text-emerald-400">✓</span><span class="text-white">Observable · 內建 trace + Web UI</span></div>
<div class="flex items-center gap-2"><span class="text-emerald-400">✓</span><span class="text-white">Governable · Callbacks + Auth</span></div>
<div class="flex items-center gap-2"><span class="text-emerald-400">✓</span><span class="text-white">Deployable · Cloud Run / Agent Engine</span></div>
</div>
</div>

</div>

<div v-click="4" class="text-center mt-4 text-xs text-white/60">
ADK 不是「另一個 AI 玩具」——<span class="text-white font-semibold">它是為「第一天就要上線」設計的生產工具</span>
</div>

</div>

<!--
講者備註：
- 主訴求：市場上已經有很多選擇，為什麼推 ADK
- Click 1 自己刻：誠實說「很多團隊從這裡開始」，但碰到四道門檻就卡住
- Click 2 LangChain：先肯定它「生態最廣」，再客觀指出抽象層深、debug 挑戰
  - 可以加一句：「LangChain 很強，但它是『通用瑞士刀』，不是『生產線機器』」
- Click 3 ADK：強調「Google 官方」「Gemini 原生優化」「Deploy 整合」三點
  - 重點台詞：「你熟的 Cloud Run、Vertex AI，它都直接吃」
- 最後一句：定位 ADK 是「生產工具」，不是玩具；呼應 Ch2 四道門檻
- 下一張：ADK 的設計哲學三大支柱（Code-first / Model-agnostic / Deployment-ready）
-->

---
layout: default
class: bg-slate-950 text-white
transition: slide-left
---

<div class="h-full flex flex-col py-4 px-8">

<div class="text-center mb-6">
<div class="text-xs uppercase tracking-[0.4em] text-blue-400 mb-2">Design Philosophy</div>
<h2 class="text-2xl font-light text-white !my-0">ADK 的三根支柱</h2>
<div class="text-sm text-white/50 mt-2 italic">這三件事決定了它和其他框架不一樣</div>
</div>

<div class="grid grid-cols-3 gap-8 flex-1 min-h-0 items-stretch">

<!-- Pillar 01 · Code-first -->
<div v-click="1" class="flex flex-col items-center text-center relative">
<div class="absolute top-0 left-1/2 -translate-x-1/2 w-px h-3 bg-blue-400/50"></div>

<div class="text-5xl mb-3 mt-4">💻</div>
<div class="text-[11px] uppercase tracking-[0.3em] text-blue-400 mb-1">Pillar 01</div>
<div class="text-xl font-semibold text-white mb-1">Code-first</div>
<div class="text-base text-white/80 mb-4">程式碼優先</div>

<div class="h-px w-12 bg-blue-400/40 mb-4"></div>

<div class="text-xs text-white/70 leading-relaxed mb-3">
用 Python <span class="text-blue-300 font-semibold">寫</span> Agent，不是拖 UI、不是填 YAML。工程師熟悉的工具鏈：Git / Test / Review 全能用。
</div>

<div class="text-[11px] text-blue-200/70 bg-blue-500/10 rounded px-3 py-1.5 border border-blue-400/20">
<span class="font-semibold">結果：</span> IDE 自動完成、斷點除錯、版本控制
</div>
</div>

<!-- Pillar 02 · Model-agnostic -->
<div v-click="2" class="flex flex-col items-center text-center relative">
<div class="absolute top-0 left-1/2 -translate-x-1/2 w-px h-3 bg-purple-400/50"></div>

<div class="text-5xl mb-3 mt-4">🔌</div>
<div class="text-[11px] uppercase tracking-[0.3em] text-purple-400 mb-1">Pillar 02</div>
<div class="text-xl font-semibold text-white mb-1">Model-agnostic</div>
<div class="text-base text-white/80 mb-4">模型中立</div>

<div class="h-px w-12 bg-purple-400/40 mb-4"></div>

<div class="text-xs text-white/70 leading-relaxed mb-3">
雖然出自 Google，<span class="text-purple-300 font-semibold">不綁</span> Gemini。OpenAI、Claude、開源模型、甚至本地 Ollama 都能跑。
</div>

<div class="text-[11px] text-purple-200/70 bg-purple-500/10 rounded px-3 py-1.5 border border-purple-400/20">
<span class="font-semibold">結果：</span> 模型換人，程式碼不用改
</div>
</div>

<!-- Pillar 03 · Deployment-ready -->
<div v-click="3" class="flex flex-col items-center text-center relative">
<div class="absolute top-0 left-1/2 -translate-x-1/2 w-px h-3 bg-emerald-400/50"></div>

<div class="text-5xl mb-3 mt-4">🚀</div>
<div class="text-[11px] uppercase tracking-[0.3em] text-emerald-400 mb-1">Pillar 03</div>
<div class="text-xl font-semibold text-white mb-1">Deployment-ready</div>
<div class="text-base text-white/80 mb-4">生產就緒</div>

<div class="h-px w-12 bg-emerald-400/40 mb-4"></div>

<div class="text-xs text-white/70 leading-relaxed mb-3">
<span class="text-emerald-300 font-semibold">一行指令</span>推到 Cloud Run 或 Vertex AI Agent Engine。Session / Auth / Trace 都幫你接好了。
</div>

<div class="text-[11px] text-emerald-200/70 bg-emerald-500/10 rounded px-3 py-1.5 border border-emerald-400/20">
<span class="font-semibold">結果：</span> Demo 隔天就能上線給客戶試
</div>
</div>

</div>

<div v-click="4" class="text-center mt-6 text-xs text-white/60">
一句話：<span class="text-white font-semibold">工程師友好 + 不綁廠商 + 馬上能上線</span>
</div>

</div>

<!--
講者備註：
- 這張放慢，用「為什麼」的角度講，不是名詞解釋
- Code-first：
  - 反例：某些 no-code 工具做 Demo 很快，但要交接給工程團隊就卡住
  - 正例：ADK 讓你「像寫普通 Python 服務」一樣寫 Agent
- Model-agnostic：
  - 破解疑慮：「這是 Google 做的，我是不是要綁 Gemini？」→ 不用
  - 支援 OpenAI / Anthropic / LiteLLM（幾乎所有主流模型）
  - 為什麼重要：模型市場變很快，今天選 A 明天可能 B 更好
- Deployment-ready：
  - 最實際的賣點
  - `adk deploy cloud_run` 一行搞定
  - Vertex AI Agent Engine 是 managed service，不用管 infra
- 結尾金句「工程師友好 + 不綁廠商 + 馬上能上線」是本張總結
- 下一張：ADK 的核心元件（Agent / Tool / Session / Runner / Callbacks）
-->

---
layout: default
class: bg-slate-950 text-white
transition: slide-left
---

<div class="h-full flex flex-col py-2 px-6">

<div class="text-center mb-3">
<div class="text-xs uppercase tracking-[0.3em] text-blue-400 mb-1">Core Architecture</div>
<h2 class="text-2xl font-light text-white !my-0">ADK 的五個主角</h2>
<div class="text-sm text-white/50 mt-1 italic">看懂這張圖 · 就能讀懂任何 ADK 程式碼</div>
</div>

<div class="grid grid-cols-5 gap-5 flex-1 min-h-0">

<!-- 左：架構圖（佔 3 欄） -->
<div class="col-span-3 relative">

<!-- Runner 外框 -->
<div v-click="1" class="absolute inset-0 border-2 border-dashed border-amber-400/60 rounded-xl bg-amber-500/5 p-3">
<div class="absolute -top-3 left-4 bg-slate-950 px-2 text-xs text-amber-300 font-semibold tracking-wider">⚙️ Runner · 執行引擎</div>

<!-- Agent 內框 -->
<div v-click="2" class="absolute top-8 left-4 right-4 bg-blue-500/10 border border-blue-400/60 rounded-lg p-3">
<div class="flex items-center gap-2 mb-2">
<div class="text-xl">🤖</div>
<div>
<div class="text-[10px] uppercase tracking-wider text-blue-300">Agent</div>
<div class="text-sm font-semibold text-white">大腦 · LLM + 指令</div>
</div>
</div>
<div class="text-[10px] text-white/60 font-mono bg-slate-900/60 rounded px-2 py-1">
instruction + model + tools[]
</div>
</div>

<!-- Tools 側 -->
<div v-click="3" class="absolute top-24 right-4 flex flex-col gap-1.5">
<div class="bg-orange-500/20 border border-orange-400 rounded px-2.5 py-1 text-[11px] text-white flex items-center gap-1.5">
<span>🛠️</span><span class="font-mono">search_db</span>
</div>
<div class="bg-orange-500/20 border border-orange-400 rounded px-2.5 py-1 text-[11px] text-white flex items-center gap-1.5">
<span>🛠️</span><span class="font-mono">send_email</span>
</div>
<div class="bg-orange-500/20 border border-orange-400 rounded px-2.5 py-1 text-[11px] text-white/60 flex items-center gap-1.5 italic">
<span>🛠️</span><span>...more</span>
</div>
</div>

<!-- Session -->
<div v-click="4" class="absolute bottom-12 left-4 w-[45%] bg-purple-500/15 border border-purple-400/70 rounded-lg p-2.5">
<div class="flex items-center gap-1.5 mb-1">
<div class="text-lg">💾</div>
<div class="text-[10px] uppercase tracking-wider text-purple-300 font-semibold">Session</div>
</div>
<div class="text-[10px] text-white/70 leading-snug">對話狀態 / 歷史 / 記憶</div>
</div>

<!-- Callbacks -->
<div v-click="5" class="absolute bottom-12 right-4 w-[45%] bg-cyan-500/15 border border-cyan-400/70 rounded-lg p-2.5">
<div class="flex items-center gap-1.5 mb-1">
<div class="text-lg">🪝</div>
<div class="text-[10px] uppercase tracking-wider text-cyan-300 font-semibold">Callbacks</div>
</div>
<div class="text-[10px] text-white/70 leading-snug">生命週期鉤子 · 審計 / 改寫</div>
</div>

</div>

<!-- 使用者輸入（在外框下方） -->
<div class="absolute -bottom-1 left-1/2 -translate-x-1/2 flex flex-col items-center gap-0.5">
<div class="text-amber-400 text-sm leading-none">↑</div>
<div class="text-[10px] text-white/60">👤 User Request</div>
</div>

</div>

<!-- 右：五個元件清單（佔 2 欄） -->
<div class="col-span-2 flex flex-col gap-1.5 text-[11px] pt-1">

<div v-click="1" class="flex items-start gap-2 p-2 rounded bg-amber-500/10 border-l-2 border-amber-400">
<div class="text-base leading-none">⚙️</div>
<div>
<div class="font-semibold text-amber-200">Runner</div>
<div class="text-white/70 leading-snug">整場的「導演」——負責把 user 輸入餵給 Agent、管生命週期、處理 session。</div>
</div>
</div>

<div v-click="2" class="flex items-start gap-2 p-2 rounded bg-blue-500/10 border-l-2 border-blue-400">
<div class="text-base leading-none">🤖</div>
<div>
<div class="font-semibold text-blue-200">Agent</div>
<div class="text-white/70 leading-snug">核心抽象：綁定 LLM + instruction + 可用的 tools。</div>
</div>
</div>

<div v-click="3" class="flex items-start gap-2 p-2 rounded bg-orange-500/10 border-l-2 border-orange-400">
<div class="text-base leading-none">🛠️</div>
<div>
<div class="font-semibold text-orange-200">Tool</div>
<div class="text-white/70 leading-snug">Python function、API、或 MCP 工具——Agent 的手腳。</div>
</div>
</div>

<div v-click="4" class="flex items-start gap-2 p-2 rounded bg-purple-500/10 border-l-2 border-purple-400">
<div class="text-base leading-none">💾</div>
<div>
<div class="font-semibold text-purple-200">Session</div>
<div class="text-white/70 leading-snug">對話上下文與狀態的容器——重開也能接續。</div>
</div>
</div>

<div v-click="5" class="flex items-start gap-2 p-2 rounded bg-cyan-500/10 border-l-2 border-cyan-400">
<div class="text-base leading-none">🪝</div>
<div>
<div class="font-semibold text-cyan-200">Callbacks</div>
<div class="text-white/70 leading-snug">before_tool / after_model 等鉤子——做審計、改寫、權限檢查。</div>
</div>
</div>

</div>

</div>

</div>

<!--
講者備註：
- 這張是 Ch3 的技術核心，其他章節會一直回來引用這張
- Click 順序：Runner（大外框）→ Agent（中框）→ Tools（右側）→ Session（左下）→ Callbacks（右下）
- 用「電影劇組」的比喻會很好懂：
  - Runner = 導演（統籌整場）
  - Agent = 主角（有台詞有動機）
  - Tool = 道具（主角拿起來用）
  - Session = 劇本（記錄進度）
  - Callbacks = 場務（每場戲開拍前後做事）
- 這張停留久一點（30-40 秒），讓同學真的記住 5 個名詞
- 重點：Callbacks 是 ADK 做「企業級治理」的秘密武器，Ch6 會再細講
- 下一張：最小可執行的 ADK 程式碼範例（10 行）
-->

---
layout: default
class: bg-slate-950 text-white
transition: slide-left
---

<div class="h-full flex flex-col py-3 px-8">

<div class="text-center mb-3">
<div class="text-xs uppercase tracking-[0.3em] text-blue-400 mb-1">Hello, Agent</div>
<h2 class="text-2xl font-light text-white !my-0">10 行程式，從「只會聊天」到「會做事」</h2>
<div class="text-sm text-white/50 mt-1 italic">跟著三步走 · 程式碼會自己變化</div>
</div>

<div class="grid grid-cols-5 gap-5 flex-1 min-h-0">

<!-- 左：程式碼 Magic Move -->
<div class="col-span-3 min-h-0 flex flex-col">

````md magic-move {lines: true}
```python
# Step 1 · 純聊天版 Agent
from google.adk.agents import Agent

agent = Agent(
    name="kh_helper",
    model="gemini-2.0-flash",
    instruction="你是高雄在地生活助理，用繁中回答。",
)
```

```python
# Step 2 · 給它一個工具（Python function 就是 Tool）
from google.adk.agents import Agent

def get_weather(city: str) -> dict:
    """查詢指定城市目前天氣"""
    return {"city": city, "temp": 26, "cond": "晴時多雲"}

agent = Agent(
    name="kh_helper",
    model="gemini-2.0-flash",
    instruction="你是高雄在地生活助理，查天氣請呼叫工具。",
    tools=[get_weather],
)
```

```python
# Step 3 · 丟進 Runner，真的跑起來
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner

def get_weather(city: str) -> dict:
    """查詢指定城市目前天氣"""
    return {"city": city, "temp": 26, "cond": "晴時多雲"}

agent = Agent(
    name="kh_helper", model="gemini-2.0-flash",
    instruction="你是高雄在地生活助理，查天氣請呼叫工具。",
    tools=[get_weather],
)

runner = InMemoryRunner(agent)
async for event in runner.run_async("明天高雄適合出門嗎？"):
    print(event)  # → Agent 自動呼叫 get_weather("高雄") 再回答
```
````

</div>

<!-- 右：三步驟說明 -->
<div class="col-span-2 flex flex-col gap-2.5 text-[11px]">

<div class="flex items-start gap-2 p-2.5 rounded bg-blue-500/10 border-l-2 border-blue-400">
<div class="w-6 h-6 rounded-full bg-blue-500 text-white flex items-center justify-center text-xs font-bold shrink-0">1</div>
<div>
<div class="font-semibold text-blue-200 mb-0.5">Agent 本體</div>
<div class="text-white/70 leading-snug">三個關鍵字：<span class="font-mono text-blue-300">model</span> 選腦、<span class="font-mono text-blue-300">instruction</span> 給人設、<span class="font-mono text-blue-300">name</span> 給身份。</div>
</div>
</div>

<div class="flex items-start gap-2 p-2.5 rounded bg-orange-500/10 border-l-2 border-orange-400">
<div class="w-6 h-6 rounded-full bg-orange-500 text-white flex items-center justify-center text-xs font-bold shrink-0">2</div>
<div>
<div class="font-semibold text-orange-200 mb-0.5">加一個工具</div>
<div class="text-white/70 leading-snug">普通 Python function 就是 tool。<span class="font-mono text-orange-300">docstring</span> 和 type hints 會變成 LLM 的「工具說明書」。</div>
</div>
</div>

<div class="flex items-start gap-2 p-2.5 rounded bg-amber-500/10 border-l-2 border-amber-400">
<div class="w-6 h-6 rounded-full bg-amber-500 text-slate-900 flex items-center justify-center text-xs font-bold shrink-0">3</div>
<div>
<div class="font-semibold text-amber-200 mb-0.5">交給 Runner 執行</div>
<div class="text-white/70 leading-snug">ReAct 迴圈、tool 呼叫、結果回灌 LLM —— <span class="text-white font-semibold">全部內建</span>，你只要 <span class="font-mono text-amber-300">async for</span>。</div>
</div>
</div>

<div class="mt-1 p-2.5 rounded bg-emerald-500/10 border border-emerald-400/40">
<div class="text-[10px] uppercase tracking-wider text-emerald-300 font-semibold mb-1">💡 關鍵洞察</div>
<div class="text-white/85 leading-snug">沒有 <span class="font-mono text-emerald-200">ChatCompletion</span> 迴圈、沒有手寫 tool schema、沒有 function-call 解析 —— ADK 幫你處理掉了。</div>
</div>

</div>

</div>

</div>

<!--
講者備註：
- 這張是「AHA moment」，目的：讓大家看到 ADK 真的很簡潔
- 按方向鍵，程式碼會自動變化（Shiki Magic Move）—— 視覺很強，停下來講解
- Step 1：強調「這就是一個完整 Agent」。model + instruction + name = 三句話
  - 對比：自己用 openai SDK 大概要 20-30 行才能達到這效果
- Step 2：強調「function 就是 tool」——
  - 沒有 decorator、沒有註冊表、沒有 JSON schema
  - docstring 很重要（LLM 讀它決定要不要呼叫），type hint 會轉成 function-calling schema
- Step 3：Runner 是執行引擎（回到上一張的圖）
  - 這裡跑的是 ReAct 迴圈：思考 → 呼叫 tool → 看結果 → 再思考 → 最後回答
  - 可以現場跑給大家看（Ch5 Demo 會跑）
- 結語可以說：「這 15 行就是一個會查天氣的 Agent。但它還不能查你公司資料庫——下一個重點：MCP Toolbox」
- 下一張：Workflow Agents（Sequential / Parallel / Loop 三種）
-->

---
layout: default
class: bg-slate-950 text-white
transition: slide-left
---

<div class="h-full flex flex-col py-3 px-8">

<div class="text-center mb-4">
<div class="text-xs uppercase tracking-[0.3em] text-blue-400 mb-1">Multi-Agent Orchestration</div>
<h2 class="text-2xl font-light text-white !my-0">一個 Agent 不夠用？把它們組起來</h2>
<div class="text-sm text-white/50 mt-1 italic">ADK 內建三種 Workflow Agent · 管複雜流程不用自己寫排程</div>
</div>

<div class="grid grid-cols-3 gap-5 flex-1 min-h-0">

<!-- Sequential -->
<div v-click="1" class="flex flex-col bg-slate-900/60 border border-blue-500/40 rounded-xl p-4 shadow-lg">

<div class="flex items-center gap-2 mb-2">
<div class="text-2xl">➡️</div>
<div>
<div class="text-[10px] uppercase tracking-[0.2em] text-blue-300">Pattern 01</div>
<div class="text-lg font-semibold text-white">SequentialAgent</div>
</div>
</div>

<div class="text-xs text-white/60 mb-3 italic">一棒接一棒 · 像流水線</div>

<!-- 視覺：A → B → C -->
<div class="flex items-center justify-between gap-1 py-3 px-1 bg-slate-950/60 rounded border border-slate-700/50 mb-3">
<div class="flex-1 text-center bg-blue-500/20 border border-blue-400/60 rounded py-1.5 text-[11px] text-white font-semibold">研究</div>
<div class="text-blue-300 text-sm">→</div>
<div class="flex-1 text-center bg-blue-500/20 border border-blue-400/60 rounded py-1.5 text-[11px] text-white font-semibold">寫稿</div>
<div class="text-blue-300 text-sm">→</div>
<div class="flex-1 text-center bg-blue-500/20 border border-blue-400/60 rounded py-1.5 text-[11px] text-white font-semibold">潤稿</div>
</div>

<div class="text-[11px] text-white/75 leading-relaxed mb-2">
前一個 Agent 的輸出 = 下一個的輸入。state 在 session 中自動傳遞。
</div>

<div class="mt-auto text-[10px] text-blue-200/80 bg-blue-500/10 rounded px-2 py-1.5 border border-blue-400/20">
<span class="font-semibold">適合：</span>文件審核、資料清洗、多階段推理
</div>
</div>

<!-- Parallel -->
<div v-click="2" class="flex flex-col bg-slate-900/60 border border-purple-500/40 rounded-xl p-4 shadow-lg">

<div class="flex items-center gap-2 mb-2">
<div class="text-2xl">🔀</div>
<div>
<div class="text-[10px] uppercase tracking-[0.2em] text-purple-300">Pattern 02</div>
<div class="text-lg font-semibold text-white">ParallelAgent</div>
</div>
</div>

<div class="text-xs text-white/60 mb-3 italic">同時派工 · 像分頭偵查</div>

<!-- 視覺：A / B / C -->
<div class="py-3 px-1 bg-slate-950/60 rounded border border-slate-700/50 mb-3">
<div class="flex items-center gap-2">
<div class="text-purple-300 text-lg">⎰</div>
<div class="flex-1 space-y-1">
<div class="text-center bg-purple-500/20 border border-purple-400/60 rounded py-1 text-[11px] text-white font-semibold">查 DB</div>
<div class="text-center bg-purple-500/20 border border-purple-400/60 rounded py-1 text-[11px] text-white font-semibold">查 API</div>
<div class="text-center bg-purple-500/20 border border-purple-400/60 rounded py-1 text-[11px] text-white font-semibold">查 Web</div>
</div>
<div class="text-purple-300 text-lg">⎱</div>
</div>
</div>

<div class="text-[11px] text-white/75 leading-relaxed mb-2">
多個 sub-agent 同時跑，各自寫入不同 state key，最後合併。
</div>

<div class="mt-auto text-[10px] text-purple-200/80 bg-purple-500/10 rounded px-2 py-1.5 border border-purple-400/20">
<span class="font-semibold">適合：</span>多來源資料抓取、多模型投票、加速查詢
</div>
</div>

<!-- Loop -->
<div v-click="3" class="flex flex-col bg-slate-900/60 border border-emerald-500/40 rounded-xl p-4 shadow-lg">

<div class="flex items-center gap-2 mb-2">
<div class="text-2xl">🔁</div>
<div>
<div class="text-[10px] uppercase tracking-[0.2em] text-emerald-300">Pattern 03</div>
<div class="text-lg font-semibold text-white">LoopAgent</div>
</div>
</div>

<div class="text-xs text-white/60 mb-3 italic">反覆修 · 像磨稿子</div>

<!-- 視覺：A ↻ B -->
<div class="flex items-center justify-center gap-2 py-3 px-1 bg-slate-950/60 rounded border border-slate-700/50 mb-3">
<div class="text-center bg-emerald-500/20 border border-emerald-400/60 rounded py-1.5 px-3 text-[11px] text-white font-semibold">產生</div>
<div class="text-emerald-300 text-xl">↻</div>
<div class="text-center bg-emerald-500/20 border border-emerald-400/60 rounded py-1.5 px-3 text-[11px] text-white font-semibold">檢查</div>
</div>

<div class="text-[11px] text-white/75 leading-relaxed mb-2">
重複執行直到「退出條件」成立（品質達標、迭代上限、工具回傳 done）。
</div>

<div class="mt-auto text-[10px] text-emerald-200/80 bg-emerald-500/10 rounded px-2 py-1.5 border border-emerald-400/20">
<span class="font-semibold">適合：</span>自動 QA、Self-refine、Agent 自我修正
</div>
</div>

</div>

<div v-click="4" class="text-center mt-4 text-xs text-white/60">
三種 Workflow Agent + 一般 <span class="font-mono text-white/80">LlmAgent</span>，<span class="text-white font-semibold">像樂高一樣</span>堆出複雜流程，不用自己寫排程器
</div>

</div>

<!--
講者備註：
- Ch3 技術最後一張，把「Agent 組合」這件事講清楚
- Click 1 Sequential：最直覺的組合——像 CI/CD pipeline
  - 舉例：研究員 Agent → 寫稿 Agent → 編輯 Agent，三棒接力完成一篇文章
  - 重點：state 自動傳遞（不用自己管中間結果）
- Click 2 Parallel：為了「速度」和「多觀點」
  - 舉例：同時查內部 DB、外部 API、網路，最後讓 LLM 做 summary
  - 注意：各 sub-agent 要寫不同的 state key，否則會互相覆蓋
- Click 3 Loop：為了「品質」
  - 舉例：產生程式碼 → 跑測試 → 不過就改 → 再跑，直到通過
  - 退出條件：max_iterations 或 sub-agent 主動設定 escalate
- 結尾重點：這些 Workflow Agent 本身也是 Agent，可以互相巢狀（Parallel 裡面包 Sequential 都行）
- 銜接 Ch4：我們現在會用 ADK 組 Agent 了，但工具從哪裡來？
  - 自己寫 Python function 當然可以
  - 但如果要接「Postgres、BigQuery、Slack、Jira」呢？→ MCP 上場
-->

---
layout: default
class: bg-slate-950 text-white
transition: slide-left
---

<div class="h-full flex flex-col py-3 px-8">

<div class="text-center mb-4">
<div class="text-xs uppercase tracking-[0.3em] text-blue-400 mb-1">Sub-Agent Delegation</div>
<h2 class="text-2xl font-light text-white !my-0">第四種模式：Manager & Sub-Agents</h2>
<div class="text-sm text-white/50 mt-1 italic">不只是流程排程 · 而是職責委派</div>
</div>

<div class="grid grid-cols-2 gap-6 flex-1 min-h-0">

<!-- 左：架構圖 -->
<div class="flex flex-col items-center justify-center">

<!-- Manager -->
<div v-click="1" class="w-64 bg-gradient-to-r from-blue-900/60 to-indigo-900/60 border-2 border-blue-400 rounded-xl px-5 py-3 text-center shadow-lg shadow-blue-500/20 mb-2">
<div class="text-[10px] uppercase tracking-wider text-blue-300 mb-0.5">Manager · Gemini</div>
<div class="text-lg font-bold text-white">root_agent</div>
<div class="text-[11px] text-white/60 mt-0.5">接收任務 · 判斷 · 委派</div>
</div>

<!-- 分叉箭頭 -->
<div v-click="2" class="flex items-start gap-4 pt-2">
<div class="flex flex-col items-center">
<div class="w-px h-4 bg-blue-400/40"></div>
<div class="flex gap-12 relative">
<div class="absolute top-0 left-1/4 right-1/4 h-px bg-blue-400/30"></div>
<!-- sub agents -->
<div class="flex flex-col gap-1.5 pt-1">
<div class="bg-emerald-500/20 border border-emerald-400/60 rounded-lg px-3 py-1.5 text-center">
<div class="text-[10px] font-semibold text-emerald-300">room_agent</div>
<div class="text-[9px] text-white/50">查詢會議室</div>
</div>
<div class="bg-orange-500/20 border border-orange-400/60 rounded-lg px-3 py-1.5 text-center">
<div class="text-[10px] font-semibold text-orange-300">book_agent</div>
<div class="text-[9px] text-white/50">執行預約</div>
</div>
</div>
<div class="flex flex-col gap-1.5 pt-1">
<div class="bg-purple-500/20 border border-purple-400/60 rounded-lg px-3 py-1.5 text-center">
<div class="text-[10px] font-semibold text-purple-300">search_agent</div>
<div class="text-[9px] text-white/50">網路搜尋</div>
</div>
<div class="bg-cyan-500/20 border border-cyan-400/60 rounded-lg px-3 py-1.5 text-center">
<div class="text-[10px] font-semibold text-cyan-300">alert_agent</div>
<div class="text-[9px] text-white/50">行事曆 + Discord</div>
</div>
</div>
</div>
</div>
</div>

</div>

<!-- 右：程式碼 + 說明 -->
<div class="flex flex-col gap-2 text-[11px] min-h-0">

<div v-click="1" class="text-[10px]">

```python {monaco-diff}
root_agent = Agent(
    name="root_agent",
    model="gemini-2.0-flash",
    instruction="你是行政管理員...",
    sub_agents=[
        room_agent, search_agent,
        book_agent, alert_agent,
    ],
)
```

</div>

<div v-click="3" class="px-2 py-1.5 bg-amber-500/10 border-l-2 border-amber-400 rounded-r">
<div class="font-semibold text-amber-200 text-[11px]">與 SequentialAgent 的差別</div>
<div class="text-[10px] text-white/70 leading-snug mt-0.5">
Sequential = 死板順序 ／ sub_agents = <span class="text-white font-semibold">動態判斷</span>，Manager 決定叫誰、何時叫
</div>
</div>

<div v-click="4" class="px-2 py-1.5 bg-emerald-500/10 border-l-2 border-emerald-400 rounded-r">
<div class="font-semibold text-emerald-200 text-[11px]">各 Agent 模型可以不同</div>
<div class="text-[10px] text-white/70 leading-snug mt-0.5">
Manager 用 Gemini 精確路由，Sub-agents 用本地 Ollama 節省成本
</div>
</div>

</div>

</div>

</div>

<!--
講者備註：
- 這是今天 Demo 用的實際架構
- 重點：sub_agents 是「委派」不是「排程」——Manager 讀使用者意圖後決定轉給誰
- ADK 內建 transfer_to_agent 工具，Manager 呼叫它就能把控制權移交給子 Agent
- 混用模型是真實場景中的重要優化：強模型做 routing，弱模型做執行
- 下一章 Demo 就是跑這個架構
-->

---
layout: center
class: bg-slate-950 text-white text-center
transition: fade
---

<div class="text-xs uppercase tracking-[0.3em] text-blue-400 mb-4">Chapter 3 · Recap</div>

<h2 class="text-3xl font-light text-white mb-8">Ch3 三個重點，帶著走</h2>

<div class="max-w-3xl mx-auto space-y-4 text-left">

<div v-click class="flex items-start gap-4 p-4 bg-blue-500/10 border-l-4 border-blue-400 rounded-r">
<div class="text-3xl">1️⃣</div>
<div>
<div class="text-lg font-semibold text-blue-200 mb-1">ADK = 為生產設計的 Agent 框架</div>
<div class="text-sm text-white/70">Code-first · Model-agnostic · Deployment-ready —— 不是另一個原型玩具。</div>
</div>
</div>

<div v-click class="flex items-start gap-4 p-4 bg-purple-500/10 border-l-4 border-purple-400 rounded-r">
<div class="text-3xl">2️⃣</div>
<div>
<div class="text-lg font-semibold text-purple-200 mb-1">五個主角撐起整個系統</div>
<div class="text-sm text-white/70">Runner 導演 · Agent 主角 · Tool 道具 · Session 劇本 · Callbacks 場務。</div>
</div>
</div>

<div v-click class="flex items-start gap-4 p-4 bg-emerald-500/10 border-l-4 border-emerald-400 rounded-r">
<div class="text-3xl">3️⃣</div>
<div>
<div class="text-lg font-semibold text-emerald-200 mb-1">複雜流程用 Workflow Agent 組</div>
<div class="text-sm text-white/70">Sequential / Parallel / Loop 像樂高，不用自己寫排程器。</div>
</div>
</div>

</div>

<div v-click class="mt-10 text-white/50 text-sm italic">
但 Agent 的「手腳」從哪裡來？下一章 → <span class="text-white/80 font-semibold not-italic">MCP 與 MCP Toolbox</span>
</div>

<!--
講者備註：
- Ch3 Recap 頁，給同學一個「停下來喘氣」的時刻
- 三個 bullet 依序 click 出現，對應 Ch3 的三個主題
- 強調「五個主角」的劇組比喻——同學應該還記得
- 最後一句過場，自然接到 Ch4 MCP
- 可以自問自答：「我現在懂 ADK 了，那 tools 從哪來？」→ 引出 MCP 的動機
-->


