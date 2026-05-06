---
# ========================================
#  Chapter 7 · Conclusion：未來已來
# ========================================
layout: section
class: bg-slate-950 text-white
---

<div class="text-xs uppercase tracking-[0.3em] text-blue-400 mb-3">Chapter 07</div>

# Conclusion & Beyond

<div class="text-white/60 mt-2">從實驗室走向現實世界的 Agent</div>

<!--
講者備註：
- 讓我們把這一切串連起來。
- 最後，我們要談談最近社群最火紅的話題。
-->

---
layout: default
class: bg-slate-950 text-white
transition: slide-left
---

<div class="h-full flex flex-col py-4 px-8">

<div class="text-center mb-4">

<div class="text-xs uppercase tracking-[0.4em] text-blue-400 mb-2">The Big Picture</div>

<h2 class="text-2xl font-light text-white !my-0">串連一切：你的 Agent 藍圖</h2>

<div class="text-sm text-white/50 mt-1 italic">這就是我們今天建構的完整生態</div>

</div>

<div class="flex-1 flex flex-col items-center justify-center">

<div class="relative w-full max-w-4xl py-8 px-6 bg-slate-900/50 rounded-3xl border border-white/5 flex flex-col items-center gap-6 shadow-2xl">

<!-- Layer 1: Application -->
<div v-click="1" class="w-full flex justify-center">

<div class="w-1/3 p-2 bg-blue-500/20 border-2 border-blue-400 rounded-xl text-center shadow-lg shadow-blue-500/20">

<div class="text-[10px] font-bold text-white uppercase tracking-widest">Business App</div>

<div class="text-[8px] text-blue-200 opacity-60">Slack Bot / Web UI / CLI</div>

</div>

</div>

<!-- Layer 2: ADK (The Brain) -->
<div v-click="2" class="w-full p-3 bg-slate-800 border-2 border-slate-600 rounded-2xl flex items-center justify-around relative">

<div class="absolute -top-3 left-6 bg-slate-950 px-2 text-[8px] font-bold text-slate-400 tracking-tighter">FRAMEWORK (ADK)</div>

<div class="flex flex-col items-center">
<div class="text-lg">🤖</div>
<div class="text-[9px] font-bold text-white">Agents</div>
</div>

<div class="text-slate-600 font-bold">+</div>

<div class="flex flex-col items-center">
<div class="text-lg">⚙️</div>
<div class="text-[9px] font-bold text-white">Runners</div>
</div>

<div class="text-slate-600 font-bold">+</div>

<div class="flex flex-col items-center">
<div class="text-lg">🪝</div>
<div class="text-[9px] font-bold text-white">Callbacks</div>
</div>

</div>

<!-- Connector: MCP -->
<div v-click="3" class="w-full h-px bg-gradient-to-r from-transparent via-orange-400 to-transparent relative my-2">

<div class="absolute -top-3 left-1/2 -translate-x-1/2 bg-slate-950 px-3 py-0.5 rounded-full border border-orange-400/50 text-[8px] font-mono text-orange-400 font-bold">
Standard MCP Protocol
</div>

</div>

<!-- Layer 3: MCP Toolbox (The Hands) -->
<div v-click="4" class="w-full p-3 bg-orange-900/20 border-2 border-orange-400 rounded-2xl flex items-center justify-between">

<div class="flex flex-col items-start">
<div class="text-[8px] font-bold text-orange-300 uppercase tracking-widest mb-1">Connectors</div>
<div class="flex gap-1">
<div class="px-1.5 py-0.5 bg-slate-800 rounded text-[7px]">Slack</div>
<div class="px-1.5 py-0.5 bg-slate-800 rounded text-[7px]">G-Suite</div>
<div class="px-1.5 py-0.5 bg-slate-800 rounded text-[7px]">DB</div>
</div>
</div>

<div class="h-8 w-px bg-orange-400/30"></div>

<div class="flex flex-col items-end">
<div class="text-[8px] font-bold text-orange-300 uppercase tracking-widest mb-1">Platform</div>
<div class="text-[9px] text-white/80 font-mono">Managed MCP Toolbox</div>
</div>

</div>

</div>

</div>

<div v-click="5" class="text-center mt-4 text-[10px] text-white/40 italic">
「大腦」負責思考與調度 (ADK)，「手腳」負責執行與連接 (MCP)。
</div>

</div>

---
layout: default
class: bg-slate-950 text-white
transition: slide-left
---

<div class="h-full flex flex-col py-4 px-8">

<div class="text-center mb-8">

<div class="text-xs uppercase tracking-[0.4em] text-red-400 mb-2">Hot Topic · Open Source Power</div>

<h2 class="text-2xl font-light text-white !my-0">為什麼大家都在聊這隻「龍蝦」？</h2>

<div class="text-sm text-white/50 mt-2 italic">OpenClaw 🦞 · 開源 Agent 的狂歡</div>

</div>

<div class="grid grid-cols-2 gap-10 flex-1 items-center">

<!-- Left: The Lobster Icon & Stats -->
<div class="flex flex-col items-center">
<div class="text-9xl mb-6 drop-shadow-[0_0_35px_rgba(239,68,68,0.5)] animate-bounce">🦞</div>
<div class="bg-red-500/20 border border-red-500/50 px-4 py-2 rounded-full">
<span class="text-xs font-bold text-red-400 font-mono uppercase tracking-widest">OpenSource / Community-Driven</span>
</div>
</div>

<!-- Right: Content -->
<div class="space-y-6">

<div v-click="1" class="flex gap-4">
<div class="text-2xl shrink-0">🌍</div>
<div>
<div class="text-sm font-bold text-white mb-1">對抗閉源壟斷</div>
<div class="text-xs text-white/60 leading-relaxed">
OpenClaw 是社群對 Anthropic 商業版 Agent 的開源回應，強調「自由」與「透明」。
</div>
</div>
</div>

<div v-click="2" class="flex gap-4">
<div class="text-2xl shrink-0">🏗️</div>
<div>
<div class="text-sm font-bold text-white mb-1">極簡與高效</div>
<div class="text-xs text-white/60 leading-relaxed">
它證明了：不需要複雜的雲端架構，只靠標準協議與優秀的 Prompt，也能實現自主操作電腦。
</div>
</div>
</div>

<div v-click="3" class="flex gap-4">
<div class="text-2xl shrink-0">🔄</div>
<div>
<div class="text-sm font-bold text-white mb-1">與 MCP 的交點</div>
<div class="text-xs text-white/60 leading-relaxed">
不論是 Google ADK 還是 OpenClaw，最終都匯流向同一個終點：<span class="text-red-400 font-bold">標準化的工具協議</span>。
</div>
</div>
</div>

<div v-click="4" class="mt-4 p-3 bg-white/5 border border-white/10 rounded-lg italic text-[10px] text-white/40">
龍蝦精神：即使在深海（開源環境），也能揮舞雙螯（工具），開拓出一片天地。
</div>

</div>

</div>

</div>

---
layout: default
class: bg-slate-950 text-white
transition: slide-left
---

<div class="h-full flex flex-col py-4 px-8">

<div class="text-center mb-8">

<div class="text-xs uppercase tracking-[0.4em] text-blue-400 mb-2">Trends & Future</div>

<h2 class="text-2xl font-light text-white !my-0">Agentic Workflow：下一波浪潮</h2>

<div class="text-sm text-white/50 mt-2 italic">從「一問一答」到「自主循環」</div>

</div>

<div class="grid grid-cols-2 gap-10 flex-1">

<div class="space-y-6">

<div v-click="1" class="flex gap-4">
<div class="text-2xl shrink-0">⚡</div>
<div>
<div class="text-sm font-bold text-white mb-1">從 Chat 到 Workflow</div>
<div class="text-xs text-white/60 leading-relaxed">
未來的 AI 不再只是聊天視窗，而是背景執行的自動化流程 (Agentic Workflows)。
</div>
</div>
</div>

<div v-click="2" class="flex gap-4">
<div class="text-2xl shrink-0">🧠</div>
<div>
<div class="text-sm font-bold text-white mb-1">推理能力 (Reasoning) 的進化</div>
<div class="text-xs text-white/60 leading-relaxed">
像 Gemini 2.0 這樣的模型，將具備更強的自我修正 (Self-Correction) 與長程規劃能力。
</div>
</div>
</div>

<div v-click="3" class="flex gap-4">
<div class="text-2xl shrink-0">🌐</div>
<div>
<div class="text-sm font-bold text-white mb-1">工具生態的標準化</div>
<div class="text-xs text-white/60 leading-relaxed">
MCP 將成為像 HTTP 一樣的標準。未來的 SaaS 軟體出廠時就會自帶 MCP Server。
</div>
</div>
</div>

</div>

<div v-click="4" class="bg-slate-900 border border-blue-500/20 rounded-2xl p-6 flex flex-col items-center justify-center text-center">

<div class="text-4xl mb-4">🔮</div>

<div class="text-base font-bold text-white mb-2">「未來的軟體，都是由一群 Agent 組成的」</div>

<div class="text-xs text-white/50 leading-relaxed">
不再是寫死 (Hard-coded) 的邏輯，<br/>而是具備動態適應能力的數位員工團隊。
</div>

<div class="mt-6 w-full h-px bg-gradient-to-r from-transparent via-blue-400/50 to-transparent"></div>

<div class="mt-6 text-[10px] text-blue-300/80 font-mono tracking-widest uppercase">
The Era of Agents is Here.
</div>

</div>

</div>

</div>

---
layout: default
class: bg-slate-950 text-white
transition: slide-left
---

<div class="h-full flex flex-col py-4 px-8">

<div class="text-center mb-8">

<div class="text-xs uppercase tracking-[0.4em] text-emerald-400 mb-2">Next Steps</div>

<h2 class="text-2xl font-light text-white !my-0">你明天可以開始的行動</h2>

<div class="text-sm text-white/50 mt-2 italic">不要只停留在聽，動手做才是王道</div>

</div>

<div class="grid grid-cols-3 gap-6 flex-1">

<!-- Action 1 -->
<div v-click="1" class="flex flex-col p-5 bg-slate-900 border-t-4 border-blue-400 rounded-xl">
<div class="text-2xl mb-4">📂</div>
<div class="text-sm font-bold text-white mb-3">盤點資料源</div>
<div class="text-[10px] text-white/60 leading-relaxed">
找出公司內部最常被詢問、最碎片化的資料（如：Excel, Wiki, Slack）。這就是 Agent 的第一塊拼圖。
</div>
</div>

<!-- Action 2 -->
<div v-click="2" class="flex flex-col p-5 bg-slate-900 border-t-4 border-purple-400 rounded-xl">
<div class="text-2xl mb-4">🛠️</div>
<div class="text-sm font-bold text-white mb-3">試用 ADK</div>
<div class="text-[10px] text-white/60 leading-relaxed font-mono bg-black/40 p-2 rounded">
pip install google-adk
</div>
<div class="mt-3 text-[10px] text-white/60 leading-relaxed">
用 10 行程式碼寫一個 Local Agent。感受「Code-first」帶來的開發爽感。
</div>
</div>

<!-- Action 3 -->
<div v-click="3" class="flex flex-col p-5 bg-slate-900 border-t-4 border-orange-400 rounded-xl">
<div class="text-2xl mb-4">🧪</div>
<div class="text-sm font-bold text-white mb-3">建立 MCP Server</div>
<div class="text-[10px] text-white/60 leading-relaxed">
嘗試把你的現有 API 封裝成 MCP Server。讓它不僅能被你的 Agent 用，也能被 Claude 用。
</div>
</div>

</div>

<div v-click="4" class="mt-8 p-6 bg-emerald-500/10 border border-emerald-500/30 rounded-2xl flex items-center gap-6">
<div class="text-4xl">💡</div>
<div>
<div class="text-sm font-bold text-emerald-400 mb-1">記住：</div>
<div class="text-xs text-white/80 leading-relaxed">
Agent 的價值不在於「聰明」，而在於「有用」。<br/>解決一個微小的、重複的痛點，就是企業級 Agent 最好的起點。
</div>
</div>
</div>

</div>

---
layout: center
class: bg-slate-950 text-white text-center
---

<div class="text-xs uppercase tracking-[0.5em] text-blue-400 mb-6">Thank You!</div>

<h1 class="text-5xl font-light text-white mb-4">邁向 Production</h1>

<div class="text-xl text-white/50 italic mb-12">企業級 AI Agent 的開發實踐與挑戰</div>

<div class="flex flex-col items-center gap-4">

<div class="text-sm text-white/80">任何問題?讓我們一起討論!</div>

<div class="flex gap-4 mt-4">
<div class="px-4 py-2 bg-slate-900 border border-slate-700 rounded-full text-xs text-white/60">#GoogleADK</div>
<div class="px-4 py-2 bg-slate-900 border border-slate-700 rounded-full text-xs text-white/60">#MCP</div>
<div class="px-4 py-2 bg-slate-900 border border-slate-700 rounded-full text-xs text-white/60">#OpenClaw</div>
</div>

<a href="https://github.com/foylaou/nkust-ai-agent" target="_blank" class="mt-6 flex items-center gap-2 px-5 py-2.5 bg-slate-900 border border-slate-700 hover:border-blue-500/50 hover:bg-slate-800 rounded-lg text-xs text-white/60 hover:text-white/90 transition-all duration-200 group">
  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
  github.com/foylaou/nkust-ai-agent
</a>

</div>

<div class="mt-16 text-[10px] text-white/30 font-mono">
NKUST AI Agent Workshop · 2026.05.06
</div>