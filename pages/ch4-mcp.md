---
# ========================================
#  Chapter 4 · MCP 與 MCP Toolbox
# ========================================
layout: section
class: bg-slate-950 text-white
---

<div class="text-xs uppercase tracking-[0.3em] text-blue-400 mb-3">Chapter 04</div>

# MCP 與 MCP Toolbox

<div class="text-white/60 mt-2">企業資料源的統一接口</div>

<!--
講者備註：
- 銜接 Ch3：我們學會了用 ADK 寫 Agent 的大腦，但大腦需要「手腳」
- 手腳就是 Tool，但現在有個大問題：每家公司的 Tool 介面都不一樣
- 引出 MCP：AI 界的「USB 接口」標準
-->

---
layout: default
class: bg-slate-950 text-white
transition: slide-left
---

<div class="h-full flex flex-col py-2 px-8 text-center">

<div class="mb-2">
<div class="text-xs uppercase tracking-[0.4em] text-blue-400 mb-1">The Fragmentation Problem</div>
<h2 class="text-2xl font-light text-white !my-0">碎片化的「整合地獄」</h2>
<div class="text-sm text-white/50 mt-1 italic">在 MCP 出現之前，整合資料是一場災難</div>
</div>

<div class="flex-1 flex flex-col items-center justify-center">

<!-- NxM Complexity Visualization -->
<div class="relative w-full max-w-xl aspect-[21/9] flex items-center justify-between px-12">

  <!-- Models -->
  <div class="flex flex-col gap-3">
    <div class="w-20 h-8 bg-blue-500/20 border border-blue-400/60 rounded flex items-center justify-center text-[9px] text-white">Gemini</div>
    <div class="w-20 h-8 bg-slate-800 border border-slate-700 rounded flex items-center justify-center text-[9px] text-white/60">Claude</div>
    <div class="w-20 h-8 bg-slate-800 border border-slate-700 rounded flex items-center justify-center text-[9px] text-white/60">OpenAI</div>
  </div>

  <!-- Chaos Lines -->
  <div class="absolute inset-0 flex items-center justify-center">
    <div v-click="1" class="w-40 h-24 relative">
      <svg class="w-full h-full opacity-40" viewBox="0 0 100 100">
        <path d="M0,20 L100,20 M0,20 L100,50 M0,20 L100,80" stroke="#60a5fa" stroke-width="0.5" fill="none" />
        <path d="M0,50 L100,20 M0,50 L100,50 M0,50 L100,80" stroke="#94a3b8" stroke-width="0.5" fill="none" />
        <path d="M0,80 L100,20 M0,80 L100,50 M0,80 L100,80" stroke="#94a3b8" stroke-width="0.5" fill="none" />
      </svg>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-red-500/20 border border-red-500/50 text-red-400 text-[9px] px-2 py-1 rounded-full whitespace-nowrap">
        碎片化的 N x M 重複開發
      </div>
    </div>
  </div>

  <!-- Data Sources -->
  <div class="flex flex-col gap-3">
    <div class="w-20 h-8 bg-orange-500/20 border border-orange-400/60 rounded flex items-center justify-center text-[9px] text-white">PostgreSQL</div>
    <div class="w-20 h-8 bg-orange-500/20 border border-orange-400/60 rounded flex items-center justify-center text-[9px] text-white">Slack</div>
    <div class="w-20 h-8 bg-orange-500/20 border border-orange-400/60 rounded flex items-center justify-center text-[9px] text-white">GitHub</div>
  </div>

</div>

<div v-click="2" class="grid grid-cols-3 gap-4 mt-4">
  <div class="p-2 bg-slate-900/60 border border-slate-700 rounded-lg">
    <div class="text-lg mb-1">🛠️</div>
    <div class="text-xs font-semibold text-white">重複造輪子</div>
    <div class="text-[9px] text-white/50">每個模型都要寫一套自己的 Slack Connector</div>
  </div>
  <div class="p-2 bg-slate-900/60 border border-slate-700 rounded-lg">
    <div class="text-lg mb-1">🔒</div>
    <div class="text-xs font-semibold text-white">治理與安全</div>
    <div class="text-[9px] text-white/50">權限散落在各處，難以統一稽核</div>
  </div>
  <div class="p-2 bg-slate-900/60 border border-slate-700 rounded-lg">
    <div class="text-lg mb-1">📉</div>
    <div class="text-xs font-semibold text-white">維護成本高</div>
    <div class="text-[9px] text-white/50">API 一改，所有 Agent 都要跟著動</div>
  </div>
</div>

</div>

<div v-click="3" class="mt-2 text-[10px] text-blue-300 font-semibold uppercase tracking-wider">
We need a standard.
</div>

</div>
<!--
講者備註：
- 這張講「痛點」：以前要接資料庫，Google 寫一套、OpenAI 寫一套、Anthropic 寫一套
- 這是 N 個模型 x M 個資料源的噩夢
- 企業最怕這個：如果你今天想從 Gemini 換到 Claude，難道所有 Tooling 都要重寫嗎？
- 結論：我們需要 AI 界的 USB 接口。
-->

---
layout: default
class: bg-slate-950 text-white
transition: slide-left
---

<div class="h-full flex flex-col py-4 px-8">

<div class="text-center mb-6">
<div class="text-xs uppercase tracking-[0.4em] text-blue-400 mb-2">The Standard</div>
<h2 class="text-2xl font-light text-white !my-0">MCP：AI 時代的 USB 協議</h2>
<div class="text-sm text-white/50 mt-2 italic">Model Context Protocol · 讓模型與資料「隨插即用」</div>
</div>

<div class="grid grid-cols-2 gap-10 flex-1 items-center">

<!-- Left: Concept -->
<div class="space-y-6">
  <div v-click="1" class="relative pl-6 border-l-2 border-blue-400">
    <div class="text-lg font-semibold text-white">由 Anthropic 發起</div>
    <div class="text-sm text-white/70">一個開放、標準化的協議，讓 LLM 應用程式能無縫對接外部資料來源與工具。</div>
  </div>

  <div v-click="2" class="relative pl-6 border-l-2 border-purple-400">
    <div class="text-lg font-semibold text-white">解耦 (Decoupling)</div>
    <div class="text-sm text-white/70">模型 (Client) 不再需要知道資料庫 (Server) 的細節，只要雙方都懂 MCP 即可通訊。</div>
  </div>

  <div v-click="3" class="bg-blue-500/10 border border-blue-400/30 rounded-lg p-4">
    <div class="text-xs font-bold text-blue-300 mb-2 uppercase tracking-widest">核心價值</div>
    <div class="text-sm text-white/90">「一次開發，處處使用」：你為 Postgres 寫的 MCP Server，Gemini 和 Claude 都能直接用。</div>
  </div>
</div>

<!-- Right: Architecture Diagram -->
<div v-click="4" class="relative bg-slate-900/50 rounded-2xl border border-slate-700/50 p-6 flex flex-col items-center gap-4">
  
  <!-- MCP Client -->
  <div class="w-full bg-blue-500/20 border border-blue-400/60 rounded-lg p-3 text-center">
    <div class="text-[10px] text-blue-300 uppercase tracking-tighter">MCP Host / Client</div>
    <div class="text-sm font-bold text-white">ADK / Claude Desktop / IDE</div>
  </div>

  <div class="text-blue-400 text-lg">⇅ <span class="text-[10px] font-mono opacity-60">Standard JSON-RPC</span></div>

  <!-- MCP Server -->
  <div class="w-full bg-orange-500/20 border border-orange-400/60 rounded-lg p-3">
    <div class="text-[10px] text-orange-300 uppercase tracking-tighter text-center">MCP Server</div>
    <div class="flex justify-around mt-2">
      <div class="flex flex-col items-center">
        <div class="text-lg">📄</div>
        <div class="text-[9px] text-white/70">Resources</div>
      </div>
      <div class="flex flex-col items-center">
        <div class="text-lg">🛠️</div>
        <div class="text-[9px] text-white/70">Tools</div>
      </div>
      <div class="flex flex-col items-center">
        <div class="text-lg">📝</div>
        <div class="text-[9px] text-white/70">Prompts</div>
      </div>
    </div>
  </div>

  <div class="text-orange-400 text-lg">⇅</div>

  <!-- Real World -->
  <div class="flex gap-2">
    <div class="px-2 py-1 bg-slate-800 rounded text-[9px] border border-slate-700">Database</div>
    <div class="px-2 py-1 bg-slate-800 rounded text-[9px] border border-slate-700">SaaS APIs</div>
    <div class="px-2 py-1 bg-slate-800 rounded text-[9px] border border-slate-700">Local Files</div>
  </div>

</div>

</div>

</div>

<!--
講者備註：
- MCP 由 Anthropic 推出，但它是一個 open standard。
- 它的架構非常像 LSP (Language Server Protocol)：IDE 不需要懂每種語言，只要懂 LSP 協議，剩下的交給 Language Server。
- 三大組件：
  1. Resources：唯讀資料（如檔案內容、日誌）
  2. Tools：可執行的動作（如發郵件、寫入資料庫）
  3. Prompts：預設的提示詞模板
- 重點：這讓 Agent 開發從「整合 API」變成了「組合協議」。
-->

---
layout: default
class: bg-slate-950 text-white
transition: slide-left
---

<div class="h-full flex flex-col py-4 px-8">

<div class="text-center mb-6">
<div class="text-xs uppercase tracking-[0.4em] text-red-400 mb-2">The Reality Gap</div>
<h2 class="text-2xl font-light text-white !my-0">理想很豐滿，現實很骨感</h2>
<div class="text-sm text-white/50 mt-2 italic">部署與管理 MCP Server 的三大難題</div>
</div>

<div class="grid grid-cols-3 gap-6 flex-1">

<div v-click="1" class="bg-slate-900/60 border border-slate-700 rounded-xl p-5 flex flex-col">
  <div class="text-3xl mb-4">🐳</div>
  <div class="text-lg font-semibold text-white mb-2">部署地獄</div>
  <div class="text-xs text-white/60 leading-relaxed">
    每個 MCP Server 都要跑一個 Docker 或本地 Process？連接埠怎麼管？
  </div>
  <div class="mt-auto pt-4 border-t border-slate-800 text-[10px] text-red-400">
    → 「我只想接個 Slack，為什麼要管 K8s？」
  </div>
</div>

<div v-click="2" class="bg-slate-900/60 border border-slate-700 rounded-xl p-5 flex flex-col">
  <div class="text-3xl mb-4">🔑</div>
  <div class="text-lg font-semibold text-white mb-2">認證與密鑰</div>
  <div class="text-xs text-white/60 leading-relaxed">
    API Keys 存在哪？每個工程師本地都要存一份 .env？
  </div>
  <div class="mt-auto pt-4 border-t border-slate-800 text-[10px] text-red-400">
    → 「萬一工程師電腦丟了，金鑰就外洩了。」
  </div>
</div>

<div v-click="3" class="bg-slate-900/60 border border-slate-700 rounded-xl p-5 flex flex-col">
  <div class="text-3xl mb-4">🛡️</div>
  <div class="text-lg font-semibold text-white mb-2">缺乏統一治理</div>
  <div class="text-xs text-white/60 leading-relaxed">
    誰在什麼時候呼叫了哪個工具？LLM 亂下指令怎麼辦？
  </div>
  <div class="mt-auto pt-4 border-t border-slate-800 text-[10px] text-red-400">
    → 「Agent 把客戶資料全刪了，我查不到是誰幹的。」
  </div>
</div>

</div>

<div v-click="4" class="text-center mt-6 py-3 bg-red-500/10 border border-red-500/20 rounded">
  <span class="text-sm text-white">企業需要一個 <span class="text-red-400 font-bold">Managed MCP Platform</span> —— 這就是 MCP Toolbox 出現的原因。</span>
</div>

</div>

<!--
講者備註：
- MCP 協議本身很棒，但「實作」和「維運」是兩回事。
- 在本地跑 `node server.js` 很快，但在企業內部大規模使用時，你會遇到：
  1. 部署問題：Infrastructure 過於複雜。
  2. 安全問題：金鑰管理與權限控制。
  3. 稽核問題：缺少完整的日誌紀錄。
-->

---
layout: default
class: bg-slate-950 text-white
transition: slide-left
---

<div class="h-full flex flex-col py-4 px-8">

<div class="text-center mb-6">
<div class="text-xs uppercase tracking-[0.4em] text-blue-400 mb-2">The Solution</div>
<h2 class="text-2xl font-light text-white !my-0">MCP Toolbox：企業級 MCP 管理平台</h2>
<div class="text-sm text-white/50 mt-2 italic">讓 Agent 的「手腳」變得安全、可控、易於擴展</div>
</div>

<div class="grid grid-cols-2 gap-8 flex-1 items-center">

<!-- Visual: Toolbox UI Mockup or Iconography -->
<div class="relative group">
  <div class="absolute -inset-1 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl blur opacity-25 group-hover:opacity-50 transition"></div>
  <div class="relative bg-slate-900 border border-slate-700 rounded-xl overflow-hidden shadow-2xl">
    <div class="bg-slate-800 px-4 py-2 border-b border-slate-700 flex gap-1.5">
      <div class="w-2.5 h-2.5 rounded-full bg-red-500/50"></div>
      <div class="w-2.5 h-2.5 rounded-full bg-amber-500/50"></div>
      <div class="w-2.5 h-2.5 rounded-full bg-emerald-500/50"></div>
    </div>
    <div class="p-4 space-y-3">
      <div class="flex items-center justify-between text-[10px]">
        <span class="text-blue-400">Connected Servers (4)</span>
        <span class="text-emerald-400">● All Healthy</span>
      </div>
      <div class="space-y-2">
        <div class="bg-slate-800/50 p-2 rounded border border-blue-500/30 flex justify-between items-center">
          <div class="text-xs text-white">Slack Connector</div>
          <div class="text-[9px] bg-blue-500/20 px-1 rounded text-blue-300">mcp-v1</div>
        </div>
        <div class="bg-slate-800/50 p-2 rounded border border-slate-700 flex justify-between items-center">
          <div class="text-xs text-white">Postgres DB Reader</div>
          <div class="text-[9px] bg-slate-700 px-1 rounded text-white/50">mcp-v1</div>
        </div>
        <div class="bg-slate-800/50 p-2 rounded border border-slate-700 flex justify-between items-center">
          <div class="text-xs text-white">Jira Issue Tracker</div>
          <div class="text-[9px] bg-slate-700 px-1 rounded text-white/50">mcp-v1</div>
        </div>
      </div>
      <div class="pt-2">
        <div class="h-12 w-full bg-blue-500/10 rounded border border-dashed border-blue-400/40 flex items-center justify-center text-[10px] text-blue-300">
          + Add New MCP Server
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Key Features -->
<div class="space-y-4">
  <div v-click="1" class="flex gap-4">
    <div class="text-2xl">🚀</div>
    <div>
      <div class="text-sm font-semibold text-white">一鍵部署</div>
      <div class="text-[11px] text-white/60">內建熱門 Connector (Slack, GitHub, G-Workspace)，點擊即用，自動託管。</div>
    </div>
  </div>

  <div v-click="2" class="flex gap-4">
    <div class="text-2xl">🔑</div>
    <div>
      <div class="text-sm font-semibold text-white">集中式 Secret 管理</div>
      <div class="text-[11px] text-white/60">與 Google Cloud Secret Manager 整合，API Key 不落地，安全有保障。</div>
    </div>
  </div>

  <div v-click="3" class="flex gap-4">
    <div class="text-2xl">📊</div>
    <div>
      <div class="text-sm font-semibold text-white">完整的可觀測性</div>
      <div class="text-[11px] text-white/60">內建 Trace 與 Audit Log，每一筆工具呼叫都清清楚楚。</div>
    </div>
  </div>

  <div v-click="4" class="flex gap-4">
    <div class="text-2xl">🌐</div>
    <div>
      <div class="text-sm font-semibold text-white">跨區域訪問</div>
      <div class="text-[11px] text-white/60">支援 SSE / Std-io，無論是雲端還是地端資料，都能統一接入。</div>
    </div>
  </div>
</div>

</div>

</div>

<!--
講者備註：
- MCP Toolbox 的定位：不是要取代 MCP，而是要讓 MCP 「更好用」。
- 對於開發者：不用管 Infra，只要寫核心邏輯。
- 對於運維與資安：可以統一控管權限、監控呼叫流量。
- 它就像是 MCP Server 的 "App Store" + "Dashboard"。
-->

---
layout: default
class: bg-slate-950 text-white
transition: slide-left
---

<div class="h-full flex flex-col py-4 px-8">

<div class="text-center mb-6">
<div class="text-xs uppercase tracking-[0.4em] text-blue-400 mb-2">Synergy</div>
<h2 class="text-2xl font-light text-white !my-0">ADK + MCP Toolbox = 完整解決方案</h2>
<div class="text-sm text-white/50 mt-2 italic">「大腦」與「手腳」的完美配合</div>
</div>

<div class="flex-1 flex flex-col items-center justify-center">

<!-- Integration Flow -->
<div class="grid grid-cols-3 w-full max-w-3xl gap-4 relative">
  
  <!-- Left: ADK -->
  <div v-click="1" class="bg-blue-900/40 border-2 border-blue-400 rounded-2xl p-6 text-center shadow-xl shadow-blue-500/10">
    <div class="text-4xl mb-3">🧠</div>
    <div class="text-lg font-bold text-white mb-1">ADK</div>
    <div class="text-[10px] text-blue-200 uppercase tracking-widest mb-4 italic">The Brain</div>
    <div class="space-y-1.5 text-left text-[10px] text-white/70">
      <div class="flex items-center gap-2"><span class="text-blue-400">•</span> 推理與決策</div>
      <div class="flex items-center gap-2"><span class="text-blue-400">•</span> 多 Agent 協作</div>
      <div class="flex items-center gap-2"><span class="text-blue-400">•</span> 對話狀態管理</div>
    </div>
  </div>

  <!-- Middle: Connection -->
  <div class="flex flex-col items-center justify-center">
    <div v-click="3" class="w-full h-px bg-gradient-to-r from-blue-400 to-orange-400 relative">
      <div class="absolute -top-3 left-1/2 -translate-x-1/2 bg-slate-950 px-2 text-[10px] text-white/50 font-mono tracking-tighter">
        Standard MCP Protocol
      </div>
      <div class="absolute -right-1 -top-1 w-2 h-2 rounded-full bg-orange-400 shadow-lg shadow-orange-500/50"></div>
      <div class="absolute -left-1 -top-1 w-2 h-2 rounded-full bg-blue-400 shadow-lg shadow-blue-500/50"></div>
    </div>
  </div>

  <!-- Right: MCP Toolbox -->
  <div v-click="2" class="bg-orange-900/40 border-2 border-orange-400 rounded-2xl p-6 text-center shadow-xl shadow-orange-500/10">
    <div class="text-4xl mb-3">🦾</div>
    <div class="text-lg font-bold text-white mb-1">MCP Toolbox</div>
    <div class="text-[10px] text-orange-200 uppercase tracking-widest mb-4 italic">The Hands</div>
    <div class="space-y-1.5 text-left text-[10px] text-white/70">
      <div class="flex items-center gap-2"><span class="text-orange-400">•</span> 資料源安全接入</div>
      <div class="flex items-center gap-2"><span class="text-orange-400">•</span> 工具執行與稽核</div>
      <div class="flex items-center gap-2"><span class="text-orange-400">•</span> Secret 安全託管</div>
    </div>
  </div>

</div>

<div v-click="4" class="mt-12 max-w-2xl bg-slate-900/80 border border-slate-700 rounded-lg p-4">
  <div class="text-xs font-mono text-emerald-400 mb-2"># ADK 程式碼片段：連接 MCP Toolbox</div>
  <div class="text-[11px] text-white/80 font-mono leading-relaxed">
    mcp_tool = McpTool(url="https://mcp-toolbox.enterprise.com/slack")<br/>
    agent = Agent(..., tools=[mcp_tool])
  </div>
</div>

</div>

</div>

<!--
講者備註：
- 這張總結了兩者的關係。
- ADK 專注於 Agent 邏輯（如何思考、如何對話）。
- MCP Toolbox 專注於基礎設施（如何連接、如何安全）。
- 兩者通過標準的 MCP 協議對接。
- 程式碼範例展示了：對 ADK 來說，這只是一個 URL 的距離。
-->

---
layout: center
class: bg-slate-950 text-white text-center
transition: fade
---

<div class="text-xs uppercase tracking-[0.3em] text-blue-400 mb-4">Chapter 4 · Recap</div>

<h2 class="text-3xl font-light text-white mb-8">Ch4 重點回顧</h2>

<div class="max-w-3xl mx-auto space-y-4 text-left">

<div v-click class="flex items-start gap-4 p-4 bg-blue-500/10 border-l-4 border-blue-400 rounded-r">
<div class="text-3xl">🧩</div>
<div>
<div class="text-lg font-semibold text-blue-200 mb-1">MCP 終結了「整合地獄」</div>
<div class="text-sm text-white/70">它是 AI 界的 USB 接口，實現了模型與工具的解耦，大幅降低重複開發。</div>
</div>
</div>

<div v-click class="flex items-start gap-4 p-4 bg-purple-500/10 border-l-4 border-purple-400 rounded-r">
<div class="text-3xl">🛠️</div>
<div>
<div class="text-lg font-semibold text-purple-200 mb-1">MCP Toolbox 是管理層</div>
<div class="text-sm text-white/70">解決了部署、安全、金鑰管理與治理問題，讓企業能真正把 Agent 投入生產。</div>
</div>
</div>

<div v-click class="flex items-start gap-4 p-4 bg-emerald-500/10 border-l-4 border-emerald-400 rounded-r">
<div class="text-3xl">⚡</div>
<div>
<div class="text-lg font-semibold text-emerald-200 mb-1">ADK + MCP = 完整生態</div>
<div class="text-sm text-white/70">大腦 (ADK) + 手腳 (MCP Toolbox) = 一個安全、強大、可擴展的 AI 系統。</div>
</div>
</div>

</div>

<div v-click class="mt-10 text-white/50 text-sm italic">
光說不練假把戲。下一章 → <span class="text-white/80 font-semibold not-italic">Demo：打造你的第一個企業級 Agent</span>
</div>

<!--
講者備註：
- Ch4 結束。我們現在理論都懂了：框架懂了、協議懂了。
- 下一章將進入最精彩的部分：實機操作與 Demo。
-->
