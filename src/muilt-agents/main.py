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
import argparse
import subprocess
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="NKUST Multi-Agent Web Server")
    parser.add_argument("--debug",   action="store_true", help="開啟 memory debug log")
    parser.add_argument("--port",    type=int, default=8000, help="指定 port（預設 8000）")
    parser.add_argument("--backend", choices=["inmemory", "postgres", "redis"], help="覆蓋 MEMORY_BACKEND")
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
    backend    = os.environ.get("MEMORY_BACKEND", "inmemory")

    print("🚀 啟動 NKUST Multi-Agent")
    print(f"   DEBUG_MODE     = {debug_mode}")
    print(f"   MEMORY_BACKEND = {backend}")
    print(f"   PORT           = {args.port}")
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
