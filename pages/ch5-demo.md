---
# ========================================
#  Chapter 5 · Demo：打造你的第一個企業級 Agent
# ========================================
layout: section
class: bg-slate-950 text-white
---

<div class="text-xs uppercase tracking-[0.3em] text-blue-400 mb-3">Chapter 05</div>

# Live Demo

<div class="text-white/60 mt-2">從程式碼到生產力的瞬間</div>

<!--
講者備註：
- 聽了這麼多理論，現在我們來看真的。
- 我們會分三個層次來 Demo：
  1. 最小可行性：Local Tool。
  2. 企業級連接：MCP Toolbox 整合。
  3. 複雜流程：Multi-Agent 協同。
-->

---
layout: default
class: bg-slate-950 text-white
transition: slide-left
---

<div class="h-full flex flex-col py-4 px-8">

<div class="text-center mb-6">

<div class="text-xs uppercase tracking-[0.4em] text-blue-400 mb-2">The Mission</div>

<h2 class="text-2xl font-light text-white !my-0">Demo 目標：企業行政小幫手</h2>

<div class="text-sm text-white/50 mt-2 italic">從「問答」進化到「執行任務」</div>

</div>

<div class="grid grid-cols-3 gap-6 flex-1 items-stretch">

<!-- Step 1 -->
<div v-click="1" class="bg-slate-900/60 border border-slate-700 rounded-xl p-5 relative overflow-hidden">

<div class="absolute top-0 right-0 p-2 text-[10px] bg-blue-500/20 text-blue-300">Phase 01</div>

<div class="text-2xl mb-3">💻</div>

<div class="text-sm font-bold text-white mb-2">Local Python Tools</div>

<div class="text-[11px] text-white/60 leading-relaxed">
讀取本地檔案、執行自定義 Python 邏輯。
</div>

<div class="mt-4 flex items-center gap-1.5 text-[9px] text-emerald-400 font-mono">
<span>✓</span> 快速原型開發
</div>

</div>

<!-- Step 2 -->
<div v-click="2" class="bg-slate-900/60 border border-slate-700 rounded-xl p-5 relative overflow-hidden">

<div class="absolute top-0 right-0 p-2 text-[10px] bg-orange-500/20 text-orange-300">Phase 02</div>

<div class="text-2xl mb-3">🦾</div>

<div class="text-sm font-bold text-white mb-2">MCP Toolbox 整合</div>

<div class="text-[11px] text-white/60 leading-relaxed">
接上企業 Slack、Google Calendar、Jira。
</div>

<div class="mt-4 flex items-center gap-1.5 text-[9px] text-emerald-400 font-mono">
<span>✓</span> 跨系統資料讀寫
</div>

</div>

<!-- Step 3 -->
<div v-click="3" class="bg-slate-900/60 border border-slate-700 rounded-xl p-5 relative overflow-hidden">

<div class="absolute top-0 right-0 p-2 text-[10px] bg-purple-500/20 text-purple-300">Phase 03</div>

<div class="text-2xl mb-3">🧬</div>

<div class="text-sm font-bold text-white mb-2">Multi-Agent Orchestration</div>

<div class="text-[11px] text-white/60 leading-relaxed">
多個 Agent 分工：一個查資料、一個寫報告、一個發送。
</div>

<div class="mt-4 flex items-center gap-1.5 text-[9px] text-emerald-400 font-mono">
<span>✓</span> 處理複雜業務邏輯
</div>

</div>

</div>

<div v-click="4" class="mt-8 p-4 bg-blue-500/10 border-l-4 border-blue-400 rounded flex items-center justify-between">

<div class="text-xs text-white/80">
<span class="font-bold text-blue-300">場景模擬：</span> 「幫我查一下明天下午兩點的會議室有沒有空，如果有的話幫我約起來，並在 Slack 通知主管。」
</div>

<div class="text-[10px] font-mono bg-blue-500/20 px-2 py-1 rounded text-blue-300 italic animate-pulse">
Ready to Run...
</div>

</div>

</div>

---
layout: default
class: bg-slate-950 text-white
transition: slide-left
---

<div class="h-full flex flex-col py-4 px-8">

<div class="text-center mb-4">

<div class="text-xs uppercase tracking-[0.4em] text-blue-400 mb-2">Phase 01 · Code to Action</div>

<h2 class="text-2xl font-light text-white !my-0">定義工具，就是定義功能</h2>

<div class="text-sm text-white/50 mt-1 italic">無需 JSON Schema · Python Function 轉化為工具</div>

</div>

<div class="grid grid-cols-2 gap-6 flex-1 min-h-0">

<div class="min-h-0 flex flex-col justify-center">

````md magic-move {lines: true}
```python
# 1. 定義一個簡單的查詢 function
def get_room_status(time: str):
    """查詢會議室佔用狀況"""
    # 模擬資料庫查詢
    return f"{time} 會議室目前為空閒狀態"

# 2. 封裝進 Agent
agent = Agent(
    model="gemini-2.0-flash",
    tools=[get_room_status]
)
```

```python
# 3. 升級：加入 MCP 工具
from google.adk.mcp import McpTool

slack_tool = McpTool(
    url="https://toolbox.internal/slack"
)

agent = Agent(
    model="gemini-2.0-flash",
    tools=[get_room_status, slack_tool]
)
```
````

</div>

<div v-click="1" class="bg-slate-900 border border-slate-700 rounded-xl p-4 flex flex-col font-mono text-[10px] overflow-hidden">

<div class="text-blue-400 border-b border-slate-800 pb-2 mb-2 flex justify-between items-center">
  <span>AGENT TRACE</span>
  <span class="opacity-50 text-[8px]">ADK MONITOR v1.0</span>
</div>

<div class="space-y-3">

<div class="flex gap-2 items-start">
  <span class="text-white/40 shrink-0">09:00:01</span>
  <span class="text-purple-400 shrink-0">[USER]</span>
  <span class="text-white/80">"幫我查明天 14:00 的會議室"</span>
</div>

<div v-click="2" class="flex gap-2 bg-blue-500/10 p-1.5 rounded border-l-2 border-blue-400 items-start">
  <span class="text-white/40 shrink-0">09:00:02</span>
  <span class="text-blue-400 shrink-0">[THOUGHT]</span>
  <span class="text-blue-200">用戶詢問會議室狀況，應呼叫 get_room_status。</span>
</div>

<div v-click="3" class="flex gap-2 items-start">
  <span class="text-white/40 shrink-0">09:00:03</span>
  <span class="text-orange-400 shrink-0">[CALL]</span>
  <span class="text-white/80">get_room_status(time="明天 14:00")</span>
</div>

<div v-click="4" class="flex gap-2 items-start">
  <span class="text-white/40 shrink-0">09:00:04</span>
  <span class="text-emerald-400 shrink-0">[RESULT]</span>
  <span class="text-white/60">"明天 14:00 會議室目前為空閒狀態"</span>
</div>

<div v-click="5" class="flex gap-2 items-start">
  <span class="text-white/40 shrink-0">09:00:05</span>
  <span class="text-purple-400 shrink-0">[AGENT]</span>
  <span class="text-white/80">"查好了！明天下午兩點會議室是有空的喔。"</span>
</div>

</div>

<div class="mt-auto pt-2 border-t border-slate-800 text-blue-400/50 italic text-[8px]">
  -- Process Finished --
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

<div class="text-center mb-6">

<div class="text-xs uppercase tracking-[0.4em] text-orange-400 mb-2">Phase 02 · MCP Power</div>

<h2 class="text-2xl font-light text-white !my-0">實戰：連接真實世界</h2>

<div class="text-sm text-white/50 mt-1 italic">從 Mock Data 到生產環境的 API 呼叫</div>

</div>

<div class="grid grid-cols-2 gap-8 flex-1">

<!-- Left: MCP Toolbox UI Snapshot -->
<div class="bg-slate-900 border border-slate-700 rounded-2xl overflow-hidden shadow-2xl flex flex-col">

<div class="bg-slate-800 px-4 py-2 border-b border-slate-700 flex justify-between items-center">
  <span class="text-[10px] text-white/80 font-bold uppercase tracking-widest">MCP Toolbox Explorer</span>
  <span class="text-[10px] bg-emerald-500/20 text-emerald-400 px-2 rounded">Active</span>
</div>

<div class="p-4 space-y-4">

<!-- Server 1 -->
<div class="flex items-center justify-between p-3 bg-slate-800/50 rounded-lg border border-orange-500/30">
  <div class="flex items-center gap-3">
    <div class="w-8 h-8 bg-orange-500/20 rounded-full flex items-center justify-center text-lg">💬</div>
    <div>
      <div class="text-xs font-bold text-white">Slack Connector</div>
      <div class="text-[9px] text-white/40">mcp-server-slack</div>
    </div>
  </div>
  <div class="text-[10px] text-orange-300 font-mono">12 tools</div>
</div>

<!-- Server 2 -->
<div class="flex items-center justify-between p-3 bg-slate-800/50 rounded-lg border border-slate-700">
  <div class="flex items-center gap-3">
    <div class="w-8 h-8 bg-blue-500/20 rounded-full flex items-center justify-center text-lg">📅</div>
    <div>
      <div class="text-xs font-bold text-white">G-Calendar</div>
      <div class="text-[9px] text-white/40">mcp-server-calendar</div>
    </div>
  </div>
  <div class="text-[10px] text-blue-300 font-mono">8 tools</div>
</div>

<!-- Secret Highlight -->
<div v-click="1" class="mt-4 p-3 bg-red-500/5 border border-red-500/20 rounded-lg">
  <div class="text-[9px] font-bold text-red-400 uppercase mb-1">Secret Manager Integration</div>
  <div class="flex items-center gap-2">
    <div class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></div>
    <div class="text-[10px] text-white/60 font-mono tracking-tighter">SLACK_BOT_TOKEN: [ ENCRYPTED ]</div>
  </div>
</div>

</div>

</div>

<!-- Right: Why MCP Toolbox? -->
<div class="space-y-6 flex flex-col justify-center">

<div v-click="2" class="flex gap-4 p-4 bg-orange-500/5 border-l-2 border-orange-400 rounded-r">
  <div class="text-2xl shrink-0">⚡</div>
  <div>
    <div class="text-sm font-bold text-white mb-1">零部署成本</div>
    <div class="text-xs text-white/70">無需在開發機安裝各種 SDK 或 Docker，ADK 通過 URL 直接調用。</div>
  </div>
</div>

<div v-click="3" class="flex gap-4 p-4 bg-blue-500/5 border-l-2 border-blue-400 rounded-r">
  <div class="text-2xl shrink-0">🔒</div>
  <div>
    <div class="text-sm font-bold text-white mb-1">權限顆粒度控制</div>
    <div class="text-xs text-white/70">可以限制 Agent 只能使用 `send_message` 工具，而不能 `delete_history`。</div>
  </div>
</div>

<div v-click="4" class="flex gap-4 p-4 bg-emerald-500/5 border-l-2 border-emerald-400 rounded-r">
  <div class="text-2xl shrink-0">📋</div>
  <div>
    <div class="text-sm font-bold text-white mb-1">即時可見性</div>
    <div class="text-xs text-white/70">在 Toolbox 面板上即時觀看 Agent 正在呼叫哪個工具、傳入什麼參數。</div>
  </div>
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

<div class="text-center mb-6">

<div class="text-xs uppercase tracking-[0.4em] text-purple-400 mb-2">Phase 03 · Advanced Multi-Agent</div>

<h2 class="text-2xl font-light text-white !my-0">群策群力：多 Agent 流程</h2>

<div class="text-sm text-white/50 mt-1 italic">當一個大腦應付不來時，我們需要一個「團隊」</div>

</div>

<div class="flex-1 flex flex-col items-center justify-center relative">

<!-- Flow Visualization -->
<div class="flex items-center gap-4 w-full max-w-3xl">

<!-- Agent 1 -->
<div v-click="1" class="flex-1 bg-slate-900 border border-blue-500/50 rounded-xl p-4 text-center z-10">
  <div class="text-2xl mb-2">🕵️</div>
  <div class="text-xs font-bold text-white mb-1">Searcher</div>
  <div class="text-[9px] text-blue-300 font-mono">負責查詢會議室</div>
</div>

<!-- Arrow -->
<div v-click="2" class="text-white/20 text-xl font-bold animate-pulse">➔</div>

<!-- Agent 2 -->
<div v-click="2" class="flex-1 bg-slate-900 border border-purple-500/50 rounded-xl p-4 text-center z-10">
  <div class="text-2xl mb-2">📅</div>
  <div class="text-xs font-bold text-white mb-1">Booker</div>
  <div class="text-[9px] text-purple-300 font-mono">負責發起日曆預約</div>
</div>

<!-- Arrow -->
<div v-click="3" class="text-white/20 text-xl font-bold animate-pulse">➔</div>

<!-- Agent 3 -->
<div v-click="3" class="flex-1 bg-slate-900 border border-emerald-500/50 rounded-xl p-4 text-center z-10">
  <div class="text-2xl mb-2">📢</div>
  <div class="text-xs font-bold text-white mb-1">Notifier</div>
  <div class="text-[9px] text-emerald-300 font-mono">負責發送 Slack 通知</div>
</div>

</div>

<!-- State Container -->
<div v-click="4" class="mt-10 w-full max-w-md bg-slate-800/50 border border-slate-700 rounded-lg p-3">

<div class="flex justify-between items-center mb-2">
  <span class="text-[9px] uppercase tracking-widest text-white/40 font-bold">Shared Session State</span>
  <span class="text-[8px] font-mono text-emerald-400 bg-emerald-500/10 px-1 rounded">Persistent</span>
</div>

<div class="space-y-1 font-mono text-[9px] text-white/60">
  <div class="flex justify-between"><span>room_id:</span> <span class="text-blue-300">"Meeting-Room-A"</span></div>
  <div class="flex justify-between"><span>status:</span> <span class="text-blue-300">"Available"</span></div>
  <div v-click="2" class="flex justify-between border-t border-slate-700 pt-1"><span>event_url:</span> <span class="text-purple-300">"https://g-cal/evt/..."</span></div>
  <div v-click="3" class="flex justify-between border-t border-slate-700 pt-1"><span>slack_ts:</span> <span class="text-emerald-300">"172345.002"</span></div>
</div>

</div>

<div v-click="5" class="absolute -bottom-2 text-xs text-white/40 italic">
ADK 的 <span class="text-white">SequentialAgent</span> 自動幫你傳遞這些狀態
</div>

</div>

</div>

---
layout: center
class: bg-slate-950 text-white text-center
transition: fade
---

<div class="text-xs uppercase tracking-[0.3em] text-blue-400 mb-4">Chapter 5 · Recap</div>

<h2 class="text-3xl font-light text-white mb-8">Demo 重點總結</h2>

<div class="max-w-3xl mx-auto space-y-4 text-left">

<div v-click class="flex items-start gap-4 p-4 bg-blue-500/10 border-l-4 border-blue-400 rounded-r">

<div class="text-3xl">🚀</div>

<div>
<div class="text-lg font-semibold text-blue-200 mb-1">定義即功能</div>
<div class="text-sm text-white/70">Python function 不需要任何複雜修飾，就能成為 Agent 的技能。</div>
</div>

</div>

<div v-click class="flex items-start gap-4 p-4 bg-orange-500/10 border-l-4 border-orange-400 rounded-r">

<div class="text-3xl">🔌</div>

<div>
<div class="text-lg font-semibold text-orange-200 mb-1">隨插即用的 MCP 生態</div>
<div class="text-sm text-white/70">透過 MCP Toolbox，開發者可以用同一個介面操作 Slack、Calendar 與地端資料庫。</div>
</div>

</div>

<div v-click class="flex items-start gap-4 p-4 bg-purple-500/10 border-l-4 border-purple-400 rounded-r">

<div class="text-3xl">🤝</div>

<div>
<div class="text-lg font-semibold text-purple-200 mb-1">團隊協作的力量</div>
<div class="text-sm text-white/70">透過 Multi-Agent 組合，將單一 Agent 無法完成的長流程拆解並自動執行。</div>
</div>

</div>

</div>

<div v-click class="mt-10 text-white/50 text-sm italic">
有了大腦與手腳，我們該如何將它交付？下一章 → <span class="text-white/80 font-semibold not-italic">Deploy & Scale：邁向生產環境</span>
</div>

<!--
講者備註：
- Demo 結束，我們展示了從 simple code 到 complex orchestration。
- 接下來要討論的是最後一哩路：如何部署、如何治理。
-->
