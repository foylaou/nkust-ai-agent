---
# ========================================
#  Chapter 6 · Deploy & Scale：邁向生產環境
# ========================================
layout: section
class: bg-slate-950 text-white
---

<div class="text-xs uppercase tracking-[0.3em] text-blue-400 mb-3">Chapter 06</div>

# Deploy & Scale

<div class="text-white/60 mt-2">從 Demo 到企業級服務的最後一哩路</div>

<!--
講者備註：
- 這一章我們會解決 ADK 的最後兩個門檻：Deployable 與 Governable。
-->

---
layout: default
class: bg-slate-950 text-white
transition: slide-left
---

<div class="h-full flex flex-col py-4 px-8">

<div class="text-center mb-6">

<div class="text-xs uppercase tracking-[0.4em] text-blue-400 mb-2">Deployment Paths</div>

<h2 class="text-2xl font-light text-white !my-0">兩條路：部署你的 Agent</h2>

<div class="text-sm text-white/50 mt-2 italic">根據你的控制需求選擇合適的家</div>

</div>

<div class="grid grid-cols-2 gap-8 flex-1">

<!-- Path A: Cloud Run -->
<div v-click="1" class="bg-slate-900/60 border border-blue-500/30 rounded-2xl p-6 flex flex-col relative overflow-hidden">

<div class="absolute -top-4 -right-4 w-24 h-24 bg-blue-500/10 rounded-full blur-2xl"></div>

<div class="flex items-center gap-3 mb-4">
  <div class="text-3xl">☁️</div>
  <div>
    <div class="text-sm font-bold text-white">Google Cloud Run</div>
    <div class="text-[10px] text-blue-300 uppercase font-mono">Serverless Container</div>
  </div>
</div>

<div class="space-y-3 mb-6">
  <div class="flex items-start gap-2">
    <div class="text-emerald-400 text-xs mt-0.5">✓</div>
    <div class="text-xs text-white/70">完全的環境控制權 (Runtime/Dependencies)</div>
  </div>
  <div class="flex items-start gap-2">
    <div class="text-emerald-400 text-xs mt-0.5">✓</div>
    <div class="text-xs text-white/70">標準的 CI/CD 流程整合</div>
  </div>
  <div class="flex items-start gap-2">
    <div class="text-emerald-400 text-xs mt-0.5">✓</div>
    <div class="text-xs text-white/70">適合已有雲端架構的團隊</div>
  </div>
</div>

<div class="mt-auto p-3 bg-blue-500/10 rounded border border-blue-400/20">
  <div class="text-[9px] font-mono text-blue-300">adk deploy cloud_run --project=...</div>
</div>

</div>

<!-- Path B: Agent Engine -->
<div v-click="2" class="bg-slate-900/60 border border-purple-500/30 rounded-2xl p-6 flex flex-col relative overflow-hidden">

<div class="absolute -top-4 -right-4 w-24 h-24 bg-purple-500/10 rounded-full blur-2xl"></div>

<div class="flex items-center gap-3 mb-4">
  <div class="text-3xl">🚀</div>
  <div>
    <div class="text-sm font-bold text-white">Vertex AI Agent Engine</div>
    <div class="text-[10px] text-purple-300 uppercase font-mono">Managed Agent Service</div>
  </div>
</div>

<div class="space-y-3 mb-6">
  <div class="flex items-start gap-2">
    <div class="text-emerald-400 text-xs mt-0.5">✓</div>
    <div class="text-xs text-white/70">Google 託管，無需管理基礎設施</div>
  </div>
  <div class="flex items-start gap-2">
    <div class="text-emerald-400 text-xs mt-0.5">✓</div>
    <div class="text-xs text-white/70">原生整合 Vertex AI 的治理與監控</div>
  </div>
  <div class="flex items-start gap-2">
    <div class="text-emerald-400 text-xs mt-0.5">✓</div>
    <div class="text-xs text-white/70">最快從 Code 轉為 API 端點</div>
  </div>
</div>

<div class="mt-auto p-3 bg-purple-500/10 rounded border border-purple-400/20">
  <div class="text-[9px] font-mono text-purple-300">adk deploy agent_engine --project=...</div>
</div>

</div>

</div>

<div v-click="3" class="text-center mt-6 text-xs text-white/40">
ADK 提供統一的 CLI 工具，讓你 <span class="text-white">無需重寫程式碼</span> 即可在不同環境切換。
</div>

</div>

---
layout: default
class: bg-slate-950 text-white
transition: slide-left
---

<div class="h-full flex flex-col py-3 px-8">

<div class="text-center mb-4">
<div class="text-xs uppercase tracking-[0.4em] text-emerald-400 mb-1">Governable Agent</div>
<h2 class="text-2xl font-light text-white !my-0">治理：如何防止 Agent 「脫軌」？</h2>
<div class="text-sm text-white/50 mt-1 italic">透過 Callbacks 實現企業級安全護欄</div>
</div>

<div class="grid grid-cols-5 gap-6 flex-1 items-center min-h-0">

<!-- Left: The Logic ( col-span-3 ) -->
<div class="col-span-3 space-y-2">

<div v-click="1" class="bg-slate-900 border border-slate-700 p-3 rounded-lg">
  <div class="text-emerald-400 text-xs font-bold mb-1">🛡️ Input Guardrail (事前過濾)</div>
  <div class="text-[10px] text-white/70 leading-tight mb-2">
    檢查請求是否包含敏感詞、PII 資料，或超出權限的指令。
  </div>
  <div class="text-[8px] font-mono text-emerald-300/60 bg-emerald-500/5 p-1.5 rounded">
    def mask_pii(cb, req, ctx): ...<br/>
    LlmAgent(..., before_model_callback=mask_pii)
  </div>
</div>

<div v-click="2" class="bg-slate-900 border border-slate-700 p-3 rounded-lg">
  <div class="text-orange-400 text-xs font-bold mb-1">⚖️ Tool Call Audit (事中稽核)</div>
  <div class="text-[10px] text-white/70 leading-tight mb-2">
    當 Agent 決定呼叫敏感工具時，攔截並記錄審計日誌。
  </div>
  <div class="text-[8px] font-mono text-orange-300/60 bg-orange-500/5 p-1.5 rounded">
    def verify_permission(tool, args, ctx): ...<br/>
    LlmAgent(..., before_tool_callback=verify_permission)
  </div>
</div>

<div v-click="3" class="bg-slate-900 border border-slate-700 p-3 rounded-lg">
  <div class="text-blue-400 text-xs font-bold mb-1">🔍 Output Sanitizer (事後清洗)</div>
  <div class="text-[10px] text-white/70 leading-tight mb-2">
    確保回覆內容不包含機密資訊，或進行最終格式修正。
  </div>
  <div class="text-[8px] font-mono text-blue-300/60 bg-blue-500/5 p-1.5 rounded">
    def filter_output(cb, resp, ctx): ...<br/>
    LlmAgent(..., after_model_callback=filter_output)
  </div>
</div>

</div>

<!-- Right: Visual ( col-span-2 ) -->
<div class="col-span-2 flex flex-col gap-3">

<div class="relative py-8 px-4 bg-slate-800/50 rounded-2xl border border-slate-700 flex flex-col items-center justify-center gap-4">

  <div class="w-12 h-12 bg-blue-500/20 rounded-full flex items-center justify-center text-2xl">🤖</div>

  <div v-click="1" class="absolute top-2 left-2 bg-emerald-500/20 border border-emerald-500/50 text-[7px] px-1.5 py-0.5 rounded text-emerald-300">Input Filter</div>
  <div v-click="2" class="absolute top-1/2 -right-2 bg-orange-500/20 border border-orange-500/50 text-[7px] px-1.5 py-0.5 rounded text-orange-300">Tool Audit</div>
  <div v-click="3" class="absolute bottom-2 left-1/2 -translate-x-1/2 bg-blue-500/20 border border-blue-400/50 text-[7px] px-1.5 py-0.5 rounded text-blue-300">Output Sanitize</div>

  <div class="text-center">
    <div class="text-[10px] text-white/60">ADK Callbacks Pipeline</div>
    <div class="text-[9px] text-emerald-400 font-bold tracking-widest">SECURE</div>
  </div>

</div>

<div class="p-3 bg-slate-900 border border-slate-700 rounded-xl">
  <div class="text-[9px] text-white/40 uppercase mb-1">Pro Tip</div>
  <div class="text-[10px] text-white/70 leading-snug">
    Callbacks 是硬性代碼攔截。無論 Prompt 如何被繞過，Callback 始終有效。
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

<div class="text-center mb-4">

<div class="text-xs uppercase tracking-[0.4em] text-blue-400 mb-2">Observable Agent</div>

<h2 class="text-2xl font-light text-white !my-0">可觀測性：不再是「黑盒子」</h2>

<div class="text-sm text-white/50 mt-1 italic">內建 Trace 與 Google Cloud Observability 整合</div>

</div>

<div class="flex-1 flex flex-col gap-6">

<!-- Trace UI Simulation -->
<div v-click="1" class="bg-slate-900 border border-slate-700 rounded-2xl overflow-hidden shadow-2xl">

<div class="bg-slate-800 px-4 py-2 border-b border-slate-700 flex justify-between items-center">
  <div class="flex gap-2">
    <div class="w-2.5 h-2.5 rounded-full bg-red-500/40"></div>
    <div class="w-2.5 h-2.5 rounded-full bg-amber-500/40"></div>
    <div class="w-2.5 h-2.5 rounded-full bg-emerald-500/40"></div>
  </div>
  <span class="text-[10px] font-mono text-white/40">TRACE-ID: 8f2a1b9c...</span>
</div>

<div class="p-4 font-mono text-[10px] space-y-2">

<div class="flex gap-4 p-1 hover:bg-slate-800/50 rounded">
  <span class="text-blue-400 w-16">0ms</span>
  <span class="text-white font-bold">Runner.run_async()</span>
  <span class="text-white/40">-- Start</span>
</div>

<div class="flex gap-4 p-1 hover:bg-slate-800/50 rounded pl-6 border-l border-slate-800">
  <span class="text-blue-400 w-16">45ms</span>
  <span class="text-purple-400">Model.generate_content()</span>
  <span class="text-white/40 italic">"Thinking: Need to fetch user profile..."</span>
</div>

<div class="flex gap-4 p-1 hover:bg-slate-800/50 rounded pl-6 border-l border-slate-800">
  <span class="text-blue-400 w-16">1200ms</span>
  <span class="text-orange-400">Tool.call("get_user_info")</span>
  <span class="text-emerald-400">SUCCESS</span>
</div>

<div class="flex gap-4 p-1 hover:bg-slate-800/50 rounded pl-6 border-l border-slate-800">
  <span class="text-blue-400 w-16">1500ms</span>
  <span class="text-purple-400">Model.generate_content()</span>
  <span class="text-white/40">"Final response formulation"</span>
</div>

<div class="flex gap-4 p-1 hover:bg-slate-800/50 rounded">
  <span class="text-blue-400 w-16">1850ms</span>
  <span class="text-white font-bold">Runner.finished</span>
  <span class="text-white/40">-- Done</span>
</div>

</div>

</div>

<div class="grid grid-cols-3 gap-6">

<div v-click="2" class="p-4 bg-blue-500/10 border border-blue-400/20 rounded-xl">
  <div class="text-xs font-bold text-blue-200 mb-1">🔍 Cloud Trace</div>
  <div class="text-[10px] text-white/60">追蹤跨服務的分散式調用。</div>
</div>

<div v-click="3" class="p-4 bg-purple-500/10 border border-purple-400/20 rounded-xl">
  <div class="text-xs font-bold text-purple-200 mb-1">📊 Log Explorer</div>
  <div class="text-[10px] text-white/60">對話、工具與 Token 自動記錄。</div>
</div>

<div v-click="4" class="p-4 bg-emerald-500/10 border border-emerald-400/20 rounded-xl">
  <div class="text-xs font-bold text-emerald-200 mb-1">⏱️ Latency</div>
  <div class="text-[10px] text-white/60">精確分析每個步驟的延遲。</div>
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

<div class="text-xs uppercase tracking-[0.4em] text-blue-400 mb-2">Enterprise Checklist</div>

<h2 class="text-2xl font-light text-white !my-0">邁向 Production：最後檢核表</h2>

<div class="text-sm text-white/50 mt-2 italic">發布給客戶前，請確保這四件事</div>

</div>

<div class="grid grid-cols-2 gap-10 flex-1">

<div class="space-y-8">

<div v-click="1" class="flex gap-4">
  <div class="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center text-xl shrink-0">🔐</div>
  <div>
    <div class="text-sm font-bold text-white mb-1">金鑰安全 (Secrets)</div>
    <div class="text-xs text-white/60 leading-relaxed">
      請使用 <span class="text-blue-300">Secret Manager</span>，不要將 API Key 寫在 .env。
    </div>
  </div>
</div>

<div v-click="2" class="flex gap-4">
  <div class="w-10 h-10 bg-purple-500/20 rounded-lg flex items-center justify-center text-xl shrink-0">🤝</div>
  <div>
    <div class="text-sm font-bold text-white mb-1">身分驗證 (Auth)</div>
    <div class="text-xs text-white/60 leading-relaxed">
      整合 IAP 或 OAuth。確保 <span class="text-purple-300">User A</span> 只能存取自己的資料。
    </div>
  </div>
</div>

</div>

<div class="space-y-8">

<div v-click="3" class="flex gap-4">
  <div class="w-10 h-10 bg-orange-500/20 rounded-lg flex items-center justify-center text-xl shrink-0">📈</div>
  <div>
    <div class="text-sm font-bold text-white mb-1">配額管理 (Quotas)</div>
    <div class="text-xs text-white/60 leading-relaxed">
      設定 LLM 的 <span class="text-orange-300">Rate Limits</span>，防止惡意消耗。
    </div>
  </div>
</div>

<div v-click="4" class="flex gap-4">
  <div class="w-10 h-10 bg-emerald-500/20 rounded-lg flex items-center justify-center text-xl shrink-0">📝</div>
  <div>
    <div class="text-sm font-bold text-white mb-1">審計日誌 (Audit)</div>
    <div class="text-xs text-white/60 leading-relaxed">
      所有工具變動操作都必須寫入不可篡改的 <span class="text-emerald-300">Audit Log</span>。
    </div>
  </div>
</div>

</div>

</div>

<div v-click="5" class="mt-8 p-4 bg-slate-900 border border-slate-700 rounded-xl text-center">
  <div class="text-sm text-white/90">
    <span class="text-blue-400 font-bold">結論：</span> ADK 是為了讓你「睡得著覺」而設計。
  </div>
</div>

</div>

---
layout: center
class: bg-slate-950 text-white text-center
transition: fade
---

<div class="text-xs uppercase tracking-[0.3em] text-blue-400 mb-4">Chapter 6 · Recap</div>

<h2 class="text-3xl font-light text-white mb-8">Ch6 三大收穫</h2>

<div class="max-w-3xl mx-auto space-y-4 text-left">

<div v-click class="flex items-start gap-4 p-4 bg-blue-500/10 border-l-4 border-blue-400 rounded-r">
<div class="text-3xl">🚀</div>
<div>
<div class="text-lg font-semibold text-blue-200 mb-1">部署毫不費力</div>
<div class="text-sm text-white/70">一鍵推向 Cloud Run 或 Agent Engine。</div>
</div>
</div>

<div v-click class="flex items-start gap-4 p-4 bg-emerald-500/10 border-l-4 border-emerald-400 rounded-r">
<div class="text-3xl">🛡️</div>
<div>
<div class="text-lg font-semibold text-emerald-200 mb-1">治理始於 Callbacks</div>
<div class="text-sm text-white/70">硬性的代碼攔截比軟性的提示詞更能保障安全。</div>
</div>
</div>

<div v-click class="flex items-start gap-4 p-4 bg-purple-500/10 border-l-4 border-purple-400 rounded-r">
<div class="text-3xl">📊</div>
<div>
<div class="text-lg font-semibold text-purple-200 mb-1">觀測驅動優化</div>
<div class="text-sm text-white/70">內建 Trace 與日誌讓 Agent 的運作透明化。</div>
</div>
</div>

</div>

<div v-click class="mt-10 text-white/50 text-sm italic">
大功告成！最後一個章節 → <span class="text-white/80 font-semibold not-italic">Conclusion：AI Agent 的未來與你的下一步</span>
</div>
