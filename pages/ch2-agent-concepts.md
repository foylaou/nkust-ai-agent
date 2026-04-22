---
# ========================================
#  Chapter 2 · AI Agent 核心概念
# ========================================
layout: section
class: bg-slate-950 text-white
---

<div class="text-xs uppercase tracking-[0.3em] text-blue-400 mb-3">Chapter 02</div>

# AI Agent 核心概念

<div class="text-white/60 mt-2">從 LLM 到會做事的 Agent</div>

<!--
講者備註：
- 章節過場頁，停留約 2-3 秒
- 開場白：「我們先退一步，把 LLM 和 Agent 講清楚」
-->

---
layout: default
class: bg-slate-950 text-white
transition: slide-left
---

<div class="h-full flex flex-col py-2">

<div class="text-center mb-3">
<div class="text-xs uppercase tracking-[0.3em] text-blue-400 mb-1">LLM vs Agent</div>
<h2 class="text-2xl font-light text-white !my-0">為什麼「會回答」不等於「會做事」</h2>
</div>

<div class="grid grid-cols-2 gap-6 flex-1 px-4 min-h-0">

<!-- ============ 左：LLM 的世界 ============ -->
<div class="flex flex-col bg-slate-900/60 border border-slate-700/50 rounded-xl p-4 shadow-xl">

<div class="flex items-center gap-2 mb-3">
<div class="text-xl">💬</div>
<div>
<div class="text-[10px] uppercase tracking-wider text-slate-400">LLM Only</div>
<div class="text-base font-semibold text-slate-200">純 LLM · 單向問答</div>
</div>
</div>

<div class="flex-1 flex flex-col items-center justify-center gap-1">

<div v-click="1" class="px-3 py-1.5 bg-slate-800 border border-slate-600 rounded-lg text-xs text-white/80">
👤 使用者問題
</div>

<div v-click="1" class="text-slate-500 text-sm leading-none">↓</div>

<div v-click="2" class="px-4 py-2 bg-gradient-to-r from-slate-700 to-slate-800 border border-slate-500 rounded-lg text-white text-sm font-semibold shadow">
🧠 LLM
</div>

<div v-click="2" class="text-slate-500 text-sm leading-none">↓</div>

<div v-click="3" class="px-3 py-1.5 bg-slate-800 border border-slate-600 rounded-lg text-xs text-white/80">
📝 文字回答
</div>

</div>

<div v-click="3" class="mt-2 text-center text-[11px] text-slate-400 italic">
無外部工具 · 無記憶 · 單次往返
</div>

</div>

<!-- ============ 右：Agent 的世界 ============ -->
<div v-click="4" class="flex flex-col bg-gradient-to-br from-emerald-900/40 to-cyan-900/40 border border-emerald-500/30 rounded-xl p-4 shadow-2xl shadow-emerald-500/10">

<div class="flex items-center gap-2 mb-3">
<div class="text-xl">🤖</div>
<div>
<div class="text-[10px] uppercase tracking-wider text-emerald-300">Agent</div>
<div class="text-base font-semibold text-emerald-100">AI Agent · 循環推理</div>
</div>
</div>

<div class="flex-1 flex flex-col items-center justify-center gap-1">

<div class="px-3 py-1.5 bg-emerald-500/20 border border-emerald-400 rounded-lg text-xs text-white">
👤 使用者目標
</div>

<div class="text-emerald-400 text-sm leading-none">↓</div>

<div class="relative w-full max-w-[240px]">
<div class="absolute -left-2 top-3 bottom-3 w-0.5 bg-emerald-400/40 rounded"></div>
<div class="absolute -left-3 top-0 text-emerald-300 text-xs">↻</div>

<div class="space-y-1 pl-2">

<div class="px-3 py-1.5 bg-cyan-500/20 border border-cyan-400 rounded-lg text-xs text-white">
🧠 <span class="font-semibold">Thought</span> · 思考下一步
</div>

<div class="text-center text-emerald-400 text-xs leading-none">↓</div>

<div class="px-3 py-1.5 bg-cyan-500/20 border border-cyan-400 rounded-lg text-xs text-white">
🛠️ <span class="font-semibold">Action</span> · 呼叫工具
</div>

<div class="text-center text-emerald-400 text-xs leading-none">↓</div>

<div class="px-3 py-1.5 bg-cyan-500/20 border border-cyan-400 rounded-lg text-xs text-white">
👁️ <span class="font-semibold">Observation</span> · 觀察結果
</div>

</div>
</div>

<div class="text-emerald-400 text-sm leading-none">↓</div>

<div class="px-3 py-1.5 bg-emerald-500/30 border border-emerald-400 rounded-lg text-xs text-white font-semibold">
✓ 完成目標
</div>

</div>

<div class="mt-2 text-center text-[11px] text-emerald-200/80 italic">
有工具 · 有記憶 · 多步推理
</div>

</div>

</div>

<div v-click="5" class="text-center mt-3 text-xs text-white/60">
一句話總結：<span class="text-white font-semibold">LLM 是「大腦」，Agent 是「大腦 + 手腳 + 記憶」</span>
</div>

</div>

<!--
講者備註：
- 開場：「我們先把 LLM 和 Agent 畫在同一張紙上」
- Click 1-3：左邊 LLM 一步一步組起來（Q→腦→A），強調「單向」
- Click 4：右邊 Agent 一次全出，看到循環箭頭的視覺衝擊
- 重點講 Thought → Action → Observation 是 ReAct pattern（Reasoning + Acting）
- 用一個具體例子：「問天氣 vs 幫我訂會議」
  - 問天氣 → LLM 可能給你過時答案
  - 幫我訂會議 → Agent 會查行事曆、發 invite、確認
- 最後一句「大腦 vs 大腦+手腳+記憶」是本張金句，停頓一下

口頭補充（原本在卡片底部的細節）：
- LLM 限制：只能用訓練時的知識 / 無法查即時資料 / 給答案後就結束
- Agent 優勢：可呼叫外部工具 API / 保留上下文與記憶 / 多步推理直到完成
-->

---
layout: default
class: bg-slate-950 text-white
transition: slide-left
---

<div class="h-full flex flex-col py-2 px-6">

<div class="text-center mb-4">
<div class="text-xs uppercase tracking-[0.3em] text-blue-400 mb-1">Anatomy of an Agent</div>
<h2 class="text-2xl font-light text-white !my-0">拆解一個 Agent 的四大組件</h2>
<div class="text-sm text-white/50 mt-1 italic">少了任何一個，都只是「聰明的 Chatbot」</div>
</div>

<div class="grid grid-cols-2 gap-4 flex-1 min-h-0">

<!-- ============ 01 · Brain ============ -->
<div v-click="1" class="relative bg-gradient-to-br from-purple-900/40 to-purple-950/40 border border-purple-500/30 rounded-xl p-4 shadow-lg">
<div class="absolute -top-2.5 -left-2.5 w-8 h-8 bg-purple-500 text-white rounded-full flex items-center justify-center text-xs font-bold shadow">01</div>

<div class="flex items-center gap-3 mb-2">
<div class="text-3xl">🧠</div>
<div>
<div class="text-[10px] uppercase tracking-wider text-purple-300">Brain</div>
<div class="text-lg font-semibold text-white leading-tight">大腦 · 推理中樞</div>
</div>
</div>

<div class="text-xs text-white/70 leading-relaxed mb-2">
負責「<span class="text-purple-300 font-semibold">思考</span>」與「<span class="text-purple-300 font-semibold">決策</span>」：分析任務、選擇工具、產生回應。
</div>

<div class="text-[11px] text-purple-200/60 bg-purple-500/10 rounded px-2 py-1">
<span class="font-semibold">例：</span> Gemini · GPT · Claude
</div>
</div>

<!-- ============ 02 · Memory ============ -->
<div v-click="2" class="relative bg-gradient-to-br from-blue-900/40 to-blue-950/40 border border-blue-500/30 rounded-xl p-4 shadow-lg">
<div class="absolute -top-2.5 -left-2.5 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center text-xs font-bold shadow">02</div>

<div class="flex items-center gap-3 mb-2"><div class="text-3xl">💾</div>
<div>
<div class="text-[10px] uppercase tracking-wider text-blue-300">Memory</div>
<div class="text-lg font-semibold text-white leading-tight">記憶 · 上下文管理</div>
</div>
</div>

<div class="text-xs text-white/70 leading-relaxed mb-2">
<span class="text-blue-300 font-semibold">短期</span>：本次對話上下文 · <span class="text-blue-300 font-semibold">長期</span>：跨對話知識與偏好。
</div>

<div class="text-[11px] text-blue-200/60 bg-blue-500/10 rounded px-2 py-1">
<span class="font-semibold">例：</span> Session 紀錄 · Vector DB · RAG
</div>
</div>

<!-- ============ 03 · Tools ============ -->
<div v-click="3" class="relative bg-gradient-to-br from-orange-900/40 to-amber-950/40 border border-orange-500/30 rounded-xl p-4 shadow-lg">
<div class="absolute -top-2.5 -left-2.5 w-8 h-8 bg-orange-500 text-white rounded-full flex items-center justify-center text-xs font-bold shadow">03</div>

<div class="flex items-center gap-3 mb-2">
<div class="text-3xl">🛠️</div>
<div>
<div class="text-[10px] uppercase tracking-wider text-orange-300">Tools</div>
<div class="text-lg font-semibold text-white leading-tight">工具 · 對外執行力</div>
</div>
</div>

<div class="text-xs text-white/70 leading-relaxed mb-2">
Agent 的「<span class="text-orange-300 font-semibold">手腳</span>」：呼叫 API、查資料庫、寄信、操作系統。
</div>

<div class="text-[11px] text-orange-200/60 bg-orange-500/10 rounded px-2 py-1">
<span class="font-semibold">例：</span> search_db · send_email · MCP tools
</div>
</div>

<!-- ============ 04 · Planning ============ -->
<div v-click="4" class="relative bg-gradient-to-br from-emerald-900/40 to-emerald-950/40 border border-emerald-500/30 rounded-xl p-4 shadow-lg">
<div class="absolute -top-2.5 -left-2.5 w-8 h-8 bg-emerald-500 text-white rounded-full flex items-center justify-center text-xs font-bold shadow">04</div>

<div class="flex items-center gap-3 mb-2">
<div class="text-3xl">🗺️</div>
<div>
<div class="text-[10px] uppercase tracking-wider text-emerald-300">Planning</div>
<div class="text-lg font-semibold text-white leading-tight">規劃 · 任務分解</div>
</div>
</div>

<div class="text-xs text-white/70 leading-relaxed mb-2">
把「<span class="text-emerald-300 font-semibold">大目標</span>」拆成「<span class="text-emerald-300 font-semibold">可執行的小步驟</span>」並決定順序。
</div>

<div class="text-[11px] text-emerald-200/60 bg-emerald-500/10 rounded px-2 py-1">
<span class="font-semibold">例：</span> ReAct · Plan-and-Execute · Chain-of-Thought
</div>
</div>

</div>

<div v-click="5" class="text-center mt-4 text-xs text-white/60">
這四塊組起來 = <span class="text-white font-semibold">一個能「自主完成任務」的 Agent</span>
</div>

</div>

<!--
講者備註：
- 用「拆機殼」的比喻：「我們把 Agent 拆開看它裡面有什麼」
- 依序 click：Brain（最重要，有它才有 IQ）→ Memory（連續對話關鍵）→ Tools（沒它就只會紙上談兵）→ Planning（長任務必備）
- 每塊可以花 15-20 秒講一個具體例子：
  - Brain：Gemini vs GPT 有什麼差（擇 LLM 的考量）
  - Memory：為什麼 ChatGPT 要「新對話」就會忘記你
  - Tools：這就是今天主角 MCP Toolbox 要處理的事
  - Planning：為什麼複雜任務要先列步驟
- 最後一句「四塊組起來 = Agent」做為本章內化總結
- 下一張：企業級 Agent 的 4 個要求（連到 Ch3 為什麼要用 ADK）
-->

---
layout: default
class: bg-slate-950 text-white
transition: slide-left
---

<div class="h-full flex flex-col py-2 px-6">

<div class="text-center mb-4">
<div class="text-xs uppercase tracking-[0.3em] text-amber-400 mb-1">Prototype → Production</div>
<h2 class="text-2xl font-light text-white !my-0">「能跑」跟「能上線」中間差四道門檻</h2>
<div class="text-sm text-white/50 mt-1 italic">Demo 10 分鐘 · 上線 6 個月</div>
</div>

<div class="grid grid-cols-2 gap-3 flex-1 min-h-0">

<!-- 01 · Observable -->
<div v-click="1" class="flex gap-3 items-start bg-slate-900/60 border-l-4 border-cyan-400 rounded-r-lg p-4 shadow">
<div class="text-3xl shrink-0">👁️</div>
<div class="flex-1 min-w-0">
<div class="flex items-baseline gap-2 mb-1">
<span class="text-base font-semibold text-white">可觀測</span>
<span class="text-[10px] uppercase tracking-wider text-cyan-300">Observable</span>
</div>
<div class="text-xs text-white/70 leading-relaxed mb-1.5">
每一次推理、每一次 tool 呼叫、每一個 token 都要看得到。
</div>
<div class="text-[11px] text-red-300/80">
✕ 沒有它：出事了你不知道 Agent 在想什麼
</div>
</div>
</div>

<!-- 02 · Governable -->
<div v-click="2" class="flex gap-3 items-start bg-slate-900/60 border-l-4 border-amber-400 rounded-r-lg p-4 shadow">
<div class="text-3xl shrink-0">🛡️</div>
<div class="flex-1 min-w-0">
<div class="flex items-baseline gap-2 mb-1">
<span class="text-base font-semibold text-white">可治理</span>
<span class="text-[10px] uppercase tracking-wider text-amber-300">Governable</span>
</div>
<div class="text-xs text-white/70 leading-relaxed mb-1.5">
權限、PII 過濾、審計日誌、Prompt Injection 防護。
</div>
<div class="text-[11px] text-red-300/80">
✕ 沒有它：資料外洩、法遵炸鍋、被當後門
</div>
</div>
</div>

<!-- 03 · Scalable -->
<div v-click="3" class="flex gap-3 items-start bg-slate-900/60 border-l-4 border-blue-400 rounded-r-lg p-4 shadow">
<div class="text-3xl shrink-0">🚀</div>
<div class="flex-1 min-w-0">
<div class="flex items-baseline gap-2 mb-1">
<span class="text-base font-semibold text-white">可擴展</span>
<span class="text-[10px] uppercase tracking-wider text-blue-300">Scalable</span>
</div>
<div class="text-xs text-white/70 leading-relaxed mb-1.5">
多人同時用、狀態持久化、長任務背景執行。
</div>
<div class="text-[11px] text-red-300/80">
✕ 沒有它：Demo OK，10 個人同時用就爆了
</div>
</div>
</div>

<!-- 04 · Evaluable -->
<div v-click="4" class="flex gap-3 items-start bg-slate-900/60 border-l-4 border-emerald-400 rounded-r-lg p-4 shadow">
<div class="text-3xl shrink-0">📊</div>
<div class="flex-1 min-w-0">
<div class="flex items-baseline gap-2 mb-1">
<span class="text-base font-semibold text-white">可評估</span>
<span class="text-[10px] uppercase tracking-wider text-emerald-300">Evaluable</span>
</div>
<div class="text-xs text-white/70 leading-relaxed mb-1.5">
回歸測試、品質指標、A/B 實驗、prompt 版本管理。
</div>
<div class="text-[11px] text-red-300/80">
✕ 沒有它：改了 prompt 不知道更好還更爛
</div>
</div>
</div>

</div>

<div v-click="5" class="text-center mt-4 text-xs text-white/60">
自己刻這四題要花 <span class="text-amber-300 font-semibold">80% 的力氣</span> 在 <span class="text-white font-semibold">「不是 AI」</span> 的事 · 所以需要框架 →
</div>

</div>

<!--
講者備註：
- 這張是 Ch2 收尾，也是 Ch3 的引子
- 主訴求：「能 Demo」和「敢上線」差很多
- 四個門檻依序 click：Observable → Governable → Scalable → Evaluable
- 每個門檻都有一個「沒有它會怎樣」的紅字警語，戳聽眾痛點
- 對工程背景同學：強調這四件事自己刻 = 做 MLOps + Platform
- 對主管背景同學：強調這四件事是「你敢把它丟到客戶面前」的前提
- 最後一句過場：「80% 力氣花在不是 AI 的事」→ 自然帶到 Ch3「所以我們用框架」
- 關鍵台詞可用：「這就是為什麼 Google 要做一個叫 ADK 的框架」
-->


