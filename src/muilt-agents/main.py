#!/usr/bin/env python3
"""
NKUST Multi-Agent 啟動入口
放置位置: src/muilt-agents/main.py
用法:
    python main.py          # 一般啟動
    python main.py --debug  # 開啟 memory debug log
    python main.py --port 8080
    python main.py --backend postgres

原始 adk web muilt-agents --memory_service_uri="unified://"
"""

import os
import sys
import stat
import platform
import argparse
import subprocess
from pathlib import Path

# MCP Toolbox 版本（學員自行下載的對應版本）
TOOLBOX_VERSION = "1.4.0"
# GitHub Release 頁面（含各平台下載連結與 checksum）
TOOLBOX_RELEASE_URL = f"https://github.com/googleapis/mcp-toolbox/releases/tag/v{TOOLBOX_VERSION}"


def _detect_platform():
    """回傳 (os_name, arch, bin_name) 對應 genai-toolbox 的下載路徑。"""
    system = platform.system().lower()           # darwin / linux / windows
    machine = platform.machine().lower()         # arm64 / x86_64 / aarch64 / amd64 ...

    os_map = {"darwin": "darwin", "linux": "linux", "windows": "windows"}
    os_name = os_map.get(system, system)

    if machine in ("x86_64", "amd64"):
        arch = "amd64"
    elif machine in ("arm64", "aarch64"):
        arch = "arm64"
    else:
        arch = machine

    bin_name = "toolbox.exe" if os_name == "windows" else "toolbox"
    return os_name, arch, bin_name


def _download_hint(os_name, arch, bin_path):
    """印出該平台的下載指引。"""
    url = f"https://storage.googleapis.com/genai-toolbox/v{TOOLBOX_VERSION}/{os_name}/{arch}/{'toolbox.exe' if os_name == 'windows' else 'toolbox'}"
    dest_dir = bin_path.parent
    print("=" * 70)
    print("⚠️  找不到 MCP Toolbox 執行檔，mcp_tool_agent 將無法使用。")
    print(f"    偵測平台：{os_name}/{arch}")
    print(f"    請自行下載 v{TOOLBOX_VERSION} 並放到：{dest_dir}")
    print()
    if os_name == "windows":
        print("    PowerShell：")
        print(f'      Invoke-WebRequest -Uri "{url}" -OutFile "{bin_path}"')
    else:
        print("    終端機：")
        print(f'      curl -L -o "{bin_path}" "{url}"')
        print(f'      chmod +x "{bin_path}"')
    print()
    print(f"    其他平台 / checksum 請見：{TOOLBOX_RELEASE_URL}")
    print("=" * 70)


def setup_toolbox():
    """啟動前配置 MCP Toolbox：定位執行檔、設權限、設定環境變數。

    執行檔由學員自行下載（跨平台），缺檔時只印出指引並繼續，
    其餘 agent 不受影響。
    """
    os_name, arch, bin_name = _detect_platform()

    # main.py 在 src/muilt-agents/，toolbox 在 src/lib/mcp_tool_box/
    toolbox_dir = Path(__file__).resolve().parent.parent / "lib" / "mcp_tool_box"
    bin_path = toolbox_dir / bin_name
    config_path = toolbox_dir / "tools.yaml"
    db_path = toolbox_dir / "toolbox.db"

    # 環境變數讓 mcp_tool_agent 找得到執行檔、設定與資料庫
    os.environ.setdefault("TOOLBOX_BIN", str(bin_path))
    os.environ.setdefault("TOOLBOX_CONFIG", str(config_path))
    os.environ.setdefault("SQLITE_DATABASE", str(db_path))

    if not bin_path.exists():
        _download_hint(os_name, arch, bin_path)
        return False

    # 非 Windows：補上執行權限
    if os_name != "windows":
        try:
            mode = os.stat(bin_path).st_mode
            os.chmod(bin_path, mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        except OSError as e:
            print(f"⚠️  無法設定 toolbox 執行權限：{e}")

    # macOS：移除 Gatekeeper quarantine 屬性（best-effort）
    if os_name == "darwin":
        subprocess.run(
            ["xattr", "-d", "com.apple.quarantine", str(bin_path)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
        )

    print(f"✅ MCP Toolbox v{TOOLBOX_VERSION} 就緒：{bin_path}")
    if not config_path.exists():
        print(f"⚠️  缺少設定檔：{config_path}")
    if not db_path.exists():
        print(f"⚠️  缺少 SQLite 資料庫：{db_path}")
    return True


def main():
    parser = argparse.ArgumentParser(description="NKUST Multi-Agent Web Server")
    parser.add_argument("--debug", action="store_true", help="開啟 memory debug log")
    parser.add_argument("--port", type=int, default=8000, help="指定 port（預設 8000）")
    parser.add_argument("--backend", choices=["sqlite", "inmemory", "postgres", "redis"], help="覆蓋 MEMORY_BACKEND")
    args = parser.parse_args()

    # main.py 在 src/muilt-agents/，執行目錄切到 src/
    src_dir = Path(__file__).parent.parent
    os.chdir(src_dir)

    # 設定環境變數
    if args.debug:
        os.environ["DEBUG_MODE"] = "1"
    if args.backend:
        os.environ["MEMORY_BACKEND"] = args.backend

    debug_mode = os.environ.get("DEBUG_MODE", "0")
    backend = os.environ.get("MEMORY_BACKEND", "sqlite")

    print("🚀 啟動 NKUST Multi-Agent")
    print(f"   DEBUG_MODE     = {debug_mode}")
    print(f"   MEMORY_BACKEND = {backend}")
    print(f"   PORT           = {args.port}")
    print()

    # 配置 MCP Toolbox（跨平台；學員自行下載執行檔）
    setup_toolbox()
    print()

    cmd = [
        sys.executable, "-m", "google.adk.cli",
        "web", "muilt-agents",
        "--memory_service_uri", "unified://",
        "--port", str(args.port),
    ]

    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 已停止")
    except subprocess.CalledProcessError as e:
        print(f"❌ 啟動失敗: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
