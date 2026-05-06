import logging
import os
from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams
from dotenv import load_dotenv
from datetime import datetime
import pytz
from google.adk.tools.base_tool import BaseTool
# 確保使用台灣時區
tz = pytz.timezone('Asia/Taipei')
now = datetime.now(tz)
current_time_str = now.strftime("%Y-%m-%d %A %H:%M:%S")
# 例如：2026-05-05 Tuesday 14:11:59
load_dotenv()

_agent_mode = os.getenv("AGENT_MODE", "gemini").lower()
_model_name  = os.getenv("MODEL_NAME", "gemini-2.5-flash")
MODEL = f"openai/{_model_name}" if _agent_mode == "ollama" else _model_name

SYSTEM_INSTRUCTION = (
    "你是專門處理「石化業安全督導（Petrochemical Audits）」與「KPI 績效管理」的專業數據分析助理。 "
    f"【系統資訊】現在的台灣系統時間是：{current_time_str}。\n"
    "你的唯一職責是使用系統提供的資料庫查詢工具，來回答關於工廠督導案件、缺失改善進度、事故原因統計、督導委員名單以及企業 KPI 達標狀況的問題。 "
    "在回答時，請將工具回傳的生硬數據轉化為清晰、專業且易讀的總結報告。 "
    "如果使用者詢問與工業安全、督導稽核或 KPI 無關的話題，請禮貌地表示你無法協助，並說明你只能處理石化安衛與績效相關的查詢。 "
    "絕對不要嘗試回答無關的問題，或將工具用於其他未授權的用途。"
)

# 需要確認的工具名單（從你的 MCP Server 工具列表挑）
TOOLS_REQUIRE_CONFIRMATION = {
    "list-all-audits",
}

async def confirm_sensitive_tools(
        tool: BaseTool,
        args: dict,
        tool_context: ToolContext,
) -> dict | None:
    if tool.name in TOOLS_REQUIRE_CONFIRMATION:
        if tool_context.tool_confirmation is None:
            tool_context.request_confirmation(
                hint=f"即將執行工具 [{tool.name}]，參數：{args}，是否確認？",  # ← keyword
                payload={}
            )
            return {"status": "等待使用者確認..."}
    return None


sql_agent = LlmAgent(
    model=MODEL,
    name="sql_agent",
    description="「石化業安全督導（Petrochemical Audits）」與「KPI 績效管理」的專業數據分析助理",
    instruction=SYSTEM_INSTRUCTION,
    before_tool_callback=confirm_sensitive_tools,  # ← 條件式攔截
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=os.getenv("MCP_SERVER_URL", "https://mcp-toolbox.isafe.org.tw/mcp"),
                headers={
                    "Authorization": f"Bearer {os.getenv('MCP_SERVER_TOKEN', '')}"
                    if os.getenv('MCP_SERVER_TOKEN') else None
                }
            ),
        )
    ],
)

# require_confirmation=True,  # ← 全部 MCP 工具呼叫前都需確認