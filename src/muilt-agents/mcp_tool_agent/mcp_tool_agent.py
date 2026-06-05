"""
mcp_tool_agent — 透過「MCP Toolbox for Databases」操作 SQLite 資料庫的 Agent。

參考：
  - https://mcp-toolbox.dev/documentation/getting-started/mcp_quickstart/
  - https://adk.dev/integrations/mcp-toolbox-for-databases/

連線方式採 stdio：本 Agent 會直接啟動 src/lib/mcp_tool_box/toolbox 二進位檔，
搭配 tools.yaml 設定，無需另外手動啟動 HTTP server。
（若要改用 HTTP，可改成 google.adk.tools.toolbox_toolset.ToolboxToolset，
  並先以 `./toolbox --config tools.yaml --port 5000` 啟動 server。）
"""

import os
import platform
from pathlib import Path

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams
from mcp import StdioServerParameters

load_dotenv()

# ==========================================
# 模型設定（與專案其他 Agent 一致）
# ==========================================
_agent_mode = os.getenv("AGENT_MODE", "gemini").lower()
_model_name = os.getenv("MODEL_NAME", "gemini-2.5-flash")
if _agent_mode == "ollama":
    from google.adk.models.lite_llm import LiteLlm
    MODEL = LiteLlm(model=f"openai/{_model_name}")
elif _agent_mode == "litellm":
    from google.adk.models.lite_llm import LiteLlm
    _ll_kwargs = {}
    if os.getenv("LITELLM_BASE_URL"):
        _ll_kwargs["api_base"] = os.getenv("LITELLM_BASE_URL")
    if os.getenv("LITELLM_API_KEY"):
        _ll_kwargs["api_key"] = os.getenv("LITELLM_API_KEY")
    MODEL = LiteLlm(model=_model_name, **_ll_kwargs)
else:
    MODEL = _model_name

# ==========================================
# MCP Toolbox 路徑設定
# ==========================================
# 本檔位置：src/muilt-agents/mcp_tool_agent/mcp_tool_agent.py
# toolbox 目錄：src/lib/mcp_tool_box/
_TOOLBOX_DIR = (
    Path(__file__).resolve().parent.parent.parent / "lib" / "mcp_tool_box"
)
# 執行檔名稱跨平台：Windows 為 toolbox.exe，其餘為 toolbox
_BIN_NAME = "toolbox.exe" if platform.system().lower() == "windows" else "toolbox"
_TOOLBOX_BIN = os.getenv("TOOLBOX_BIN", str(_TOOLBOX_DIR / _BIN_NAME))
_TOOLS_FILE = os.getenv("TOOLBOX_CONFIG", str(_TOOLBOX_DIR / "tools.yaml"))
_SQLITE_DB = os.getenv("SQLITE_DATABASE", str(_TOOLBOX_DIR / "toolbox.db"))

# ==========================================
# System Instruction
# ==========================================
SYSTEM_INSTRUCTION = (
    "你是資料庫查詢助理（Database Assistant），透過 MCP Toolbox 提供的工具操作 SQLite 飯店資料庫。\n\n"
    "【可用工具】\n"
    "  - search-hotels-by-name：依名稱關鍵字搜尋飯店\n"
    "  - search-hotels-by-location：依城市搜尋飯店\n"
    "  - book-hotel：依 id 預約飯店\n"
    "  - cancel-hotel：依 id 取消預約\n"
    "  - list-tables：列出所有資料表\n\n"
    "【規則】\n"
    "  - 一律使用工具取得真實資料，禁止憑空捏造或以文字模擬工具呼叫\n"
    "  - 預約（book-hotel）或取消（cancel-hotel）前，先確認使用者指定的飯店 id\n"
    "  - 將工具回傳的 JSON 整理成清楚、易讀的繁體中文摘要再回覆\n"
    "  - 與飯店資料庫無關的問題，禮貌說明你只能協助資料庫查詢\n"
)

# ==========================================
# Agent
# ==========================================
mcp_tool_agent = LlmAgent(
    model=MODEL,
    name="mcp_tool_agent",
    description="透過 MCP Toolbox 操作 SQLite 資料庫（飯店查詢與預約）的資料庫助理。",
    instruction=SYSTEM_INSTRUCTION,
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=_TOOLBOX_BIN,
                    args=["--config", _TOOLS_FILE, "--stdio"],
                    env={**os.environ, "SQLITE_DATABASE": _SQLITE_DB},
                ),
                timeout=30,
            ),
            # 只載入 hotel-toolset 內定義的工具
            tool_filter=[
                "search-hotels-by-name",
                "search-hotels-by-location",
                "book-hotel",
                "cancel-hotel",
                "list-tables",
            ],
        )
    ],
)
