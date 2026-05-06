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
from google.adk.tools.mcp_tool import (
    MCPToolset, StreamableHTTPConnectionParams)

MCP_URL = "https://mcp-toolbox.isafe.org.tw/mcp"

agent = LlmAgent(
    model="gemini-2.0-flash",
    tools=[
        get_room_status,
        MCPToolset(connection_params=
            StreamableHTTPConnectionParams(
                url=MCP_URL,
                headers={"Authorization":
                    "Bearer <TOKEN>"}
            )),
    ]
)
```
````

</div>

<div v-click="1" class="bg-slate-900 border border-slate-700 rounded-xl p-4 flex flex-col font-mono text-[10px] overflow-hidden">

<div class="text-blue-400 border-b border-slate-800 pb-2 mb-2 flex justify-between items-center">
  <span>AGENT TRACE · sql_agent</span>
  <span class="opacity-50 text-[8px]">ADK MONITOR v1.0</span>
</div>

<div class="space-y-2">

<div class="flex gap-2 items-start">
  <span class="text-white/40 shrink-0">10:02:01</span>
  <span class="text-purple-400 shrink-0">[USER]</span>
  <span class="text-white/80">"中油去年督導改善完成率如何？"</span>
</div>

<div v-click="2" class="flex gap-2 bg-blue-500/10 p-1.5 rounded border-l-2 border-blue-400 items-start">
  <span class="text-white/40 shrink-0">10:02:02</span>
  <span class="text-blue-400 shrink-0">[THOUGHT]</span>
  <span class="text-blue-200">查詢改善完成率 → 呼叫 get-improvement-progress</span>
</div>

<div v-click="3" class="flex gap-2 items-start">
  <span class="text-white/40 shrink-0">10:02:03</span>
  <span class="text-orange-400 shrink-0">[CALL]</span>
  <span class="text-white/80 text-[9px]">get-improvement-progress(org_name="中油")</span>
</div>

<div v-click="4" class="flex gap-2 items-start">
  <span class="text-white/40 shrink-0">10:02:04</span>
  <span class="text-emerald-400 shrink-0">[MCP]</span>
  <span class="text-white/60 text-[9px]">→ petrochemical-db · 回傳 1 筆</span>
</div>

<div v-click="4" class="flex gap-2 items-start pl-4">
  <span class="text-white/30 shrink-0 text-[8px]">RESULT</span>
  <span class="text-emerald-300 text-[9px]">TotalAudits:42 CompletionRate:78.57%</span>
</div>

<div v-click="5" class="flex gap-2 items-start">
  <span class="text-white/40 shrink-0">10:02:05</span>
  <span class="text-purple-400 shrink-0">[AGENT]</span>
  <span class="text-white/80 text-[9px]">"中油共督導 42 件，改善完成率 78.6%。"</span>
</div>

</div>

<div class="mt-auto pt-2 border-t border-slate-800 text-blue-400/50 italic text-[8px]">
  MCP Toolbox → petrochemical-db (MSSQL)
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

<div class="text-xs uppercase tracking-[0.4em] text-purple-400 mb-2">Phase 03 · Multi-Agent Team</div>

<h2 class="text-2xl font-light text-white !my-0">Manager + 六位專員：實際跑起來的架構</h2>

<div class="text-sm text-white/50 mt-1 italic">root_agent 判斷意圖 · 動態委派給對應的 sub-agent</div>

</div>

<div class="flex-1 grid grid-cols-5 gap-4 min-h-0">

<!-- 左：架構圖 -->
<div class="col-span-2 flex flex-col items-center justify-center gap-2">

<!-- root_agent -->
<div v-click="1" class="w-full bg-gradient-to-r from-blue-900/70 to-indigo-900/70 border-2 border-blue-400 rounded-xl px-4 py-2.5 text-center shadow-lg shadow-blue-500/20">
<div class="text-[9px] uppercase tracking-widest text-blue-300">Manager · Gemini</div>
<div class="text-base font-bold text-white">root_agent</div>
</div>

<div v-click="2" class="text-blue-400/50 text-lg">↓ transfer_to_agent</div>

<!-- sub-agents grid -->
<div v-click="2" class="grid grid-cols-2 gap-1.5 w-full">
<div class="bg-emerald-500/15 border border-emerald-400/50 rounded-lg p-2 text-center">
<div class="text-base">🏢</div>
<div class="text-[10px] font-semibold text-emerald-300">room_agent</div>
<div class="text-[9px] text-white/50">查詢會議室</div>
</div>
<div class="bg-orange-500/15 border border-orange-400/50 rounded-lg p-2 text-center">
<div class="text-base">📖</div>
<div class="text-[10px] font-semibold text-orange-300">book_agent</div>
<div class="text-[9px] text-white/50">執行預約</div>
</div>
<div class="bg-purple-500/15 border border-purple-400/50 rounded-lg p-2 text-center">
<div class="text-base">🔍</div>
<div class="text-[10px] font-semibold text-purple-300">search_agent</div>
<div class="text-[9px] text-white/50">網路搜尋</div>
</div>
<div class="bg-cyan-500/15 border border-cyan-400/50 rounded-lg p-2 text-center">
<div class="text-base">🔔</div>
<div class="text-[10px] font-semibold text-cyan-300">alert_agent</div>
<div class="text-[9px] text-white/50">行事曆 + Discord</div>
</div>
<div class="bg-rose-500/15 border border-rose-400/50 rounded-lg p-2 text-center">
<div class="text-base">📧</div>
<div class="text-[10px] font-semibold text-rose-300">email_agent</div>
<div class="text-[9px] text-white/50">Gmail API</div>
</div>
<div class="bg-yellow-500/15 border border-yellow-400/50 rounded-lg p-2 text-center">
<div class="text-base">🗃️</div>
<div class="text-[10px] font-semibold text-yellow-300">sql_agent</div>
<div class="text-[9px] text-white/50">資料庫 MCP</div>
</div>
</div>

</div>

<!-- 右：ADK Web UI trace 模擬 -->
<div class="col-span-3 bg-slate-900 border border-slate-700 rounded-xl p-3 font-mono text-[10px] flex flex-col overflow-hidden">

<div class="text-blue-400 border-b border-slate-800 pb-1.5 mb-2 flex justify-between items-center">
<span>ADK WEB · AGENT TRACE</span>
<span class="text-emerald-400 text-[9px] animate-pulse">● LIVE</span>
</div>

<div class="space-y-1.5 overflow-y-auto flex-1">

<div v-click="1" class="flex gap-2 items-start">
<span class="text-white/30 shrink-0">11:23:01</span>
<span class="text-purple-300 shrink-0">[USER]</span>
<span class="text-white/80">"幫我查有沒有空的會議室"</span>
</div>

<div v-click="2" class="flex gap-2 bg-blue-500/10 p-1.5 rounded border-l-2 border-blue-400 items-start">
<span class="text-white/30 shrink-0">11:23:02</span>
<span class="text-blue-300 shrink-0">[root_agent]</span>
<span class="text-blue-200">→ transfer_to_agent: room_agent</span>
</div>

<div v-click="3" class="flex gap-2 items-start pl-4">
<span class="text-white/30 shrink-0">11:23:03</span>
<span class="text-emerald-300 shrink-0">[room_agent]</span>
<span class="text-white/70">→ get_room_status()</span>
</div>

<div v-click="3" class="flex gap-2 items-start pl-4">
<span class="text-white/30 shrink-0">11:23:04</span>
<span class="text-emerald-300 shrink-0">[room_agent]</span>
<span class="text-white/60 text-[9px]">A101 空閒 · B202 空閒 · C303 空閒</span>
</div>

<div v-click="4" class="flex gap-2 items-start">
<span class="text-white/30 shrink-0">11:23:05</span>
<span class="text-white/50 shrink-0">[USER]</span>
<span class="text-white/80">"我是 Foy，5人，設計會議"</span>
</div>

<div v-click="4" class="flex gap-2 bg-blue-500/10 p-1.5 rounded border-l-2 border-blue-400 items-start">
<span class="text-white/30 shrink-0">11:23:06</span>
<span class="text-blue-300 shrink-0">[root_agent]</span>
<span class="text-blue-200">→ transfer_to_agent: book_agent</span>
</div>

<div v-click="5" class="flex gap-2 items-start pl-4">
<span class="text-white/30 shrink-0">11:23:07</span>
<span class="text-orange-300 shrink-0">[book_agent]</span>
<span class="text-white/70">→ book_room(A101, Foy, 設計會議)</span>
</div>

<div v-click="5" class="flex gap-2 items-start pl-4">
<span class="text-white/30 shrink-0">11:23:08</span>
<span class="text-orange-300 shrink-0">[book_agent]</span>
<span class="text-emerald-400">✓ 成功預約 創意腦力室</span>
</div>

<div v-click="6" class="flex gap-2 bg-blue-500/10 p-1.5 rounded border-l-2 border-blue-400 items-start">
<span class="text-white/30 shrink-0">11:23:09</span>
<span class="text-blue-300 shrink-0">[root_agent]</span>
<span class="text-blue-200">→ transfer_to_agent: alert_agent</span>
</div>

<div v-click="6" class="flex gap-2 items-start pl-4">
<span class="text-white/30 shrink-0">11:23:10</span>
<span class="text-cyan-300 shrink-0">[alert_agent]</span>
<span class="text-white/70">→ create_calendar_event + discord_send</span>
</div>

</div>

<div class="border-t border-slate-800 pt-1.5 mt-1.5 text-white/30 text-[9px] italic">
-- ADK Web UI 可即時觀看這份 trace --
</div>

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
