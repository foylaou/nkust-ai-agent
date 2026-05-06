import os
import sys
import subprocess
import time
import requests
import signal

def print_banner():
    print("\n" + "="*50)
    print("      🚀 NKUST AI Agent Workshop - Demo Runner")
    print("="*50)

def stop_server():
    """強制關閉正在執行 8000 連接埠的背景程式"""
    print("\n🧹 正在檢查並清理背景服務 (Port 8000)...")
    try:
        # 在 macOS/Linux 上尋找並關閉程序
        if sys.platform != "win32":
            result = subprocess.run(["lsof", "-t", "-i:8000"], capture_output=True, text=True)
            pids = result.stdout.strip().split("\n")
            for pid in pids:
                if pid:
                    os.kill(int(pid), signal.SIGTERM)
                    print(f"✅ 已關閉舊有的背景程序 (PID: {pid})")
        else:
            # Windows 的處理方式
            subprocess.run(["taskkill", "/f", "/im", "python.exe", "/fi", "WINDOWTITLE eq src/server.py"], stderr=subprocess.DEVNULL)
    except:
        pass

def check_server():
    """檢查 Dashboard 是否已啟動"""
    try:
        requests.get("http://localhost:8080/", timeout=1)
        return True
    except:
        return False

def start_dashboard():
    """在背景啟動 Dashboard"""
    print("\n📦 正在啟動會議室看板服務 (Dashboard)...")
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )

    # 輪詢等待，最多 10 秒
    for i in range(10):
        time.sleep(1)
        if check_server():
            print("✅ 看板服務已就緒：http://localhost:8080/")
            return
        # 若 process 已提早結束，印出錯誤
        if proc.poll() is not None:
            err = proc.stderr.read().decode(errors="ignore")
            print(f"❌ 啟動失敗：\n{err}")
            return
        print(f"   等待中... ({i+1}/10)")

    print("❌ 啟動逾時，請手動執行：uvicorn src.server:app --port 8080")

def main():
    print_banner()
    
    # 1. 確保看板服務有啟動
    if not check_server():
        choice = input("⚠️  看板服務尚未啟動。是否要在背景自動啟動？ (y/n): ").lower()
        if choice == 'y':
            start_dashboard()
        else:
            print("❌ 警告：未啟動看板服務，Agent 將無法調用本地預約工具。")
    else:
        print("ℹ️  看板服務已在背景執行中 (http://localhost:8080/)。")

    # 2. 選擇 Demo 階段
    print("\n請選擇要執行的 Demo 階段：")
    print("[1] 階段一：Local Agent (基礎工具調用)")
    print("[2] 階段二：MCP Power (跨系統整合範例)")
    print("[3] 階段三：Multi-Agent Orchestration (多代理人協作)")
    print("[k] 強制結束背景服務 (Kill Server)")
    print("[q] 退出程式")
    
    choice = input("\n請輸入編號 (1-3/k/q): ").strip().lower()
    
    if choice == '1':
        print("\n🟢 啟動階段一...")
        subprocess.run([sys.executable, "src/agent.py"])
    elif choice == '2':
        print("\n🔵 啟動階段二...")
        subprocess.run([sys.executable, "src/agent_mcp.py"])
    elif choice == '3':
        print("\n🔴 啟動階段三...")
        subprocess.run([sys.executable, "src/multi_agent.py"])
    elif choice == 'k':
        stop_server()
    elif choice == 'q':
        print("\n👋 祝您 Workshop 順利，再見！")
    else:
        print("\n❌ 無效的選擇，請重新執行程式。")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 強制結束 Demo。")
