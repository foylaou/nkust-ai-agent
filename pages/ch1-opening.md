---
# ========================================
#  Chapter 1 · 開場與問題意識
# ========================================
layout: center
class: text-center text-white
transition: fade
background: https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1920&q=80
---

<div class="absolute inset-0 bg-gradient-to-br from-slate-950/95 via-slate-900/95 to-blue-950/95"></div>

<div class="relative z-10">

<div class="text-sm uppercase tracking-[0.3em] text-blue-300 mb-8 opacity-80">
  在我們開始之前 · Before we begin
</div>

<div class="text-3xl font-light text-white/90 mb-12">
  先問三個問題 👇
</div>

<div class="flex flex-col items-center gap-5 max-w-3xl mx-auto">

<div v-click class="flex items-start gap-4 text-left bg-blue-500/10 backdrop-blur border-l-4 border-blue-400 px-6 py-4 rounded-r-lg w-full shadow-lg">
  <div class="text-3xl font-bold text-blue-400">1</div>
  <div class="text-xl pt-1 text-white/90">你今天用 <span class="font-semibold text-blue-300">ChatGPT / Gemini</span> 做了什麼？</div>
</div>

<div v-click class="flex items-start gap-4 text-left bg-amber-500/10 backdrop-blur border-l-4 border-amber-400 px-6 py-4 rounded-r-lg w-full shadow-lg">
  <div class="text-3xl font-bold text-amber-400">2</div>
  <div class="text-xl pt-1 text-white/90">它幫你「<span class="font-semibold text-amber-300">做完</span>」了一件事，還是只告訴你「<span class="italic">怎麼做</span>」？</div>
</div>

<div v-click class="flex items-start gap-4 text-left bg-emerald-500/10 backdrop-blur border-l-4 border-emerald-400 px-6 py-4 rounded-r-lg w-full shadow-lg">
  <div class="text-3xl font-bold text-emerald-400">3</div>
  <div class="text-xl pt-1 text-white/90">如果它能直接 <span class="font-semibold text-emerald-300">查公司資料庫、開工單、寄信</span> 呢？</div>
</div>

</div>

<div v-click class="mt-12 text-white/50 text-sm italic">
  這就是 <span class="font-semibold not-italic text-white/80">AI Agent</span> 想解決的事
</div>

</div>

<!--
講者備註：
- 每個問題依序 click 出現，給同學 3-5 秒思考
- 問題 1 輕鬆：大家可能會說「幫我寫 email」、「查資料」、「寫程式」
- 問題 2 是關鍵：引導出「它只是『建議』，不是『執行』」的差距
- 問題 3 是引子：如果它能真的做事呢？ → 下一張展示對比
- 最後一句「這就是 AI Agent 想解決的事」是過場句
-->

---
layout: default
class: bg-slate-950 text-white
transition: slide-left
---

<div class="h-full flex flex-col">

<div class="text-center mb-6 mt-2">
  <div class="text-xs uppercase tracking-[0.3em] text-blue-400 mb-2">A Tale of Two Workflows</div>
  <h2 class="text-3xl font-light text-white">同一個需求，兩種世界</h2>
  <div class="text-base text-white/60 mt-2 italic">
    業務：「我想知道上個月 Top 10 客戶是誰」
  </div>
</div>

<div class="grid grid-cols-2 gap-6 flex-1 px-4">

<!-- 左：傳統做法 -->
<div class="flex flex-col bg-slate-900/60 border border-slate-700/50 rounded-xl p-5 shadow-xl">

  <div class="flex items-center gap-2 mb-4">
    <div class="text-2xl">🐢</div>
    <div>
      <div class="text-xs uppercase tracking-wider text-slate-400">Before</div>
      <div class="text-lg font-semibold text-slate-300">傳統做法</div>
    </div>
  </div>

  <div class="space-y-3 text-sm text-slate-300 flex-1">

  <div v-click="1" class="flex gap-3 items-start">
    <div class="w-6 h-6 rounded-full bg-slate-700 text-white flex items-center justify-center text-xs font-bold shrink-0">1</div>
    <div>業務寄 Email 給 IT 部門，附上需求描述</div>
  </div>

  <div v-click="2" class="flex gap-3 items-start">
    <div class="w-6 h-6 rounded-full bg-slate-700 text-white flex items-center justify-center text-xs font-bold shrink-0">2</div>
    <div>工程師排進 backlog，等待優先級</div>
  </div>

  <div v-click="3" class="flex gap-3 items-start">
    <div class="w-6 h-6 rounded-full bg-slate-700 text-white flex items-center justify-center text-xs font-bold shrink-0">3</div>
    <div>工程師撰寫 SQL，跑報表、匯出 Excel</div>
  </div>

  <div v-click="4" class="flex gap-3 items-start">
    <div class="w-6 h-6 rounded-full bg-slate-700 text-white flex items-center justify-center text-xs font-bold shrink-0">4</div>
    <div>寄回 Excel，業務發現「我想再看不同時段的分佈」→ 回到步驟 1</div>
  </div>

  </div>

  <div v-click="4" class="mt-4 pt-4 border-t border-slate-700/60 flex items-center justify-between">
    <div class="flex items-center gap-2">
      <carbon-time class="text-slate-400" />
      <span class="text-slate-400 text-sm">⏱ 1–3 天</span>
    </div>
    <div class="text-xs text-slate-500">人肉排程 · 資訊落差</div>
  </div>

</div>

<!-- 右：Agent 做法（一次整塊 reveal） -->
<div v-click="5" class="flex flex-col bg-gradient-to-br from-emerald-900/40 to-cyan-900/40 border border-emerald-500/30 rounded-xl p-5 shadow-2xl shadow-emerald-500/10">

  <div class="flex items-center gap-2 mb-4">
    <div class="text-2xl">⚡</div>
    <div>
      <div class="text-xs uppercase tracking-wider text-emerald-300">After</div>
      <div class="text-lg font-semibold text-emerald-200">Agent 做法</div>
    </div>
  </div>

  <div class="space-y-3 text-sm flex-1">

  <div class="flex gap-3 items-start">
    <div class="w-6 h-6 rounded-full bg-emerald-500 text-slate-900 flex items-center justify-center text-xs font-bold shrink-0">1</div>
    <div class="text-white/90">業務直接問 Agent：<span class="italic text-emerald-200">「上月 Top 10 客戶是誰？」</span></div>
  </div>

  <div class="flex gap-3 items-start">
    <div class="w-6 h-6 rounded-full bg-emerald-500 text-slate-900 flex items-center justify-center text-xs font-bold shrink-0">2</div>
    <div class="text-white/90">Agent 自動規劃 → 呼叫資料庫工具 → 執行查詢</div>
  </div>

  <div class="flex gap-3 items-start">
    <div class="w-6 h-6 rounded-full bg-emerald-500 text-slate-900 flex items-center justify-center text-xs font-bold shrink-0">3</div>
    <div class="text-white/90">回傳結果 + 自動產出圖表 + 附上解讀</div>
  </div>

  <div class="flex gap-3 items-start">
    <div class="w-6 h-6 rounded-full bg-emerald-500 text-slate-900 flex items-center justify-center text-xs font-bold shrink-0">4</div>
    <div class="text-white/90">想看不同時段？再問一句就好 —— 上下文自動保留</div>
  </div>

  </div>

  <div class="mt-4 pt-4 border-t border-emerald-500/30 flex items-center justify-between">
    <div class="flex items-center gap-2">
      <carbon-flash class="text-emerald-300" />
      <span class="text-emerald-300 text-sm font-semibold">⏱ 10 秒內</span>
    </div>
    <div class="text-xs text-emerald-300/70">自助分析 · 零等待</div>
  </div>

</div>

</div>

<div v-click="6" class="text-center mt-5 mb-2 text-sm text-white/60">
  差別不只是「快」，而是 <span class="text-white font-semibold">決策的節奏完全不同</span>
</div>

</div>

<!--
講者備註：
- 先秀左邊傳統做法，一步一步 click 展開，製造「痛感」
- 講到步驟 4「回到步驟 1」時可以笑著說：「大家是不是都有這種經驗？」
- 然後右邊 Agent 做法整塊 fade in，視覺反差
- 強調：這不是 Chatbot，是會「執行動作」的 Agent
- 最後一句是本章結論：重點不是快，是節奏改變了 → 「自助分析」成為可能
-->

---
layout: default
class: bg-slate-950 text-white
transition: slide-left
---

<div class="h-full flex flex-col justify-center px-8">

<div class="text-center mb-10">
  <div class="text-xs uppercase tracking-[0.3em] text-blue-400 mb-3">Takeaways</div>
  <h2 class="text-3xl font-light text-white">這場演講結束後，你會帶走三件事</h2>
  <div class="w-16 h-px bg-blue-400/40 mx-auto mt-4"></div>
</div>

<div class="grid grid-cols-3 gap-6 max-w-6xl mx-auto w-full">

<!-- Goal 1 · 理解 -->
<div v-click class="group relative bg-gradient-to-br from-blue-900/40 to-blue-950/40 border border-blue-500/30 rounded-xl p-6 shadow-xl hover:shadow-blue-500/20 transition">
  <div class="absolute -top-3 -left-3 w-10 h-10 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold shadow-lg">
    01
  </div>
  <div class="text-4xl mb-3">🧠</div>
  <div class="text-xs uppercase tracking-wider text-blue-300 mb-2">Understand</div>
  <div class="text-lg font-semibold text-white mb-3 leading-snug">
    看懂 LLM 和 Agent 的<br/>本質差異
  </div>
  <div class="text-sm text-white/60 leading-relaxed">
    不再把 ChatGPT 和 Agent 搞混，<br/>
    理解「會思考」和「會做事」的關鍵
  </div>
</div>

<!-- Goal 2 · 認識 -->
<div v-click class="group relative bg-gradient-to-br from-purple-900/40 to-purple-950/40 border border-purple-500/30 rounded-xl p-6 shadow-xl hover:shadow-purple-500/20 transition">
  <div class="absolute -top-3 -left-3 w-10 h-10 bg-purple-500 text-white rounded-full flex items-center justify-center font-bold shadow-lg">
    02
  </div>
  <div class="text-4xl mb-3">🛠️</div>
  <div class="text-xs uppercase tracking-wider text-purple-300 mb-2">Build</div>
  <div class="text-lg font-semibold text-white mb-3 leading-snug">
    掌握 ADK + MCP Toolbox<br/>的實戰工法
  </div>
  <div class="text-sm text-white/60 leading-relaxed">
    知道怎麼用 10 行程式，<br/>
    讓 Agent 真的查到你公司的資料
  </div>
</div>

<!-- Goal 3 · 評估 -->
<div v-click class="group relative bg-gradient-to-br from-emerald-900/40 to-emerald-950/40 border border-emerald-500/30 rounded-xl p-6 shadow-xl hover:shadow-emerald-500/20 transition">
  <div class="absolute -top-3 -left-3 w-10 h-10 bg-emerald-500 text-white rounded-full flex items-center justify-center font-bold shadow-lg">
    03
  </div>
  <div class="text-4xl mb-3">🚀</div>
  <div class="text-xs uppercase tracking-wider text-emerald-300 mb-2">Apply</div>
  <div class="text-lg font-semibold text-white mb-3 leading-snug">
    判斷你的專題 / 公司<br/>要不要導入 Agent
  </div>
  <div class="text-sm text-white/60 leading-relaxed">
    帶著一張「評估清單」回去，<br/>
    避開常見的坑與誤區
  </div>
</div>

</div>

<div v-click class="text-center mt-10 text-white/50 text-sm italic">
  接下來我們從 <span class="text-white/80 font-semibold not-italic">「什麼是 Agent」</span> 開始 →
</div>

</div>

<!--
講者備註：
- 這張是 Ch1 收尾，告訴同學接下來「為什麼要聽下去」
- 三張卡片依序 click 出現：理解 → 建構 → 應用（對應 Bloom 認知層次）
- 講到第 3 點時可以說：「如果你只記得一件事，希望是這個——回去能判斷你的工作要不要用 Agent」
- 最後一句過場，自然帶入 Ch2「什麼是 AI Agent」
-->

