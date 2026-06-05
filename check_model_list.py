#!/usr/bin/env python3
"""
check_model_list.py — 測試 LiteLLM 目前有哪些模型可選

依 .env 內設定的各家 API Key，列出可用模型，協助你決定 MODEL_NAME 要填什麼。

用法：
    python check_model_list.py                 # 用你的 key 實際查各供應商可用模型（推薦）
    python check_model_list.py --keys          # 只檢查偵測到哪些供應商金鑰
    python check_model_list.py --provider anthropic   # 列出某供應商「目錄上」所有已知模型
    python check_model_list.py --all           # 列出所有供應商與其已知模型數量
    python check_model_list.py --ollama        # 查詢本地 Ollama 已安裝模型
    python check_model_list.py --test gpt-4o-mini            # 實際打一次 API 驗證模型可用
    python check_model_list.py --test anthropic/claude-sonnet-4-5
"""

import argparse
import os
import sys

from dotenv import load_dotenv

load_dotenv()

# 常見供應商 → 對應的環境變數（用來偵測你設了哪些金鑰）
PROVIDER_ENV = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "gemini": "GEMINI_API_KEY",
    "vertex_ai": "GOOGLE_APPLICATION_CREDENTIALS",
    "groq": "GROQ_API_KEY",
    "mistral": "MISTRAL_API_KEY",
    "cohere": "COHERE_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "xai": "XAI_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "together_ai": "TOGETHERAI_API_KEY",
    "fireworks_ai": "FIREWORKS_API_KEY",
}

# Gemini 也常用 GOOGLE_API_KEY
EXTRA_ENV_ALIASES = {
    "gemini": ["GEMINI_API_KEY", "GOOGLE_API_KEY"],
}


def _detected_providers():
    """回傳偵測到金鑰的供應商清單。"""
    found = []
    for provider, env_name in PROVIDER_ENV.items():
        names = EXTRA_ENV_ALIASES.get(provider, [env_name])
        if any(os.getenv(n) for n in names):
            found.append(provider)
    return found


def cmd_keys():
    found = _detected_providers()
    print("🔑 偵測到的供應商金鑰：")
    if not found:
        print("   （無）請在 .env 設定，例如 ANTHROPIC_API_KEY / OPENAI_API_KEY / GROQ_API_KEY …")
        return
    for p in found:
        print(f"   ✅ {p}")


def _endpoint_models(base, key):
    """GET {base}/models（OpenAI 相容端點），回傳 model id 列表。"""
    import requests

    url = base.rstrip("/") + "/models"
    headers = {"Authorization": f"Bearer {key}"} if key else {}
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json().get("data", [])
    return [m.get("id") for m in data if m.get("id")]


def cmd_endpoint():
    """列出 LITELLM_BASE_URL 指向的自架 / OpenAI 相容端點上的模型。"""
    base = os.getenv("LITELLM_BASE_URL") or os.getenv("OPENAI_BASE_URL")
    key = os.getenv("LITELLM_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not base:
        print("❌ 未設定 LITELLM_BASE_URL（或 OPENAI_BASE_URL）。")
        print("   範例： LITELLM_BASE_URL=https://llm.isafe.org.tw/v1")
        return
    print(f"🌐 查詢自架端點：{base}\n")
    try:
        ids = _endpoint_models(base, key)
    except Exception as e:
        print(f"❌ 查詢失敗：{e}")
        return
    if not ids:
        print("⚠️ 端點沒有回傳任何模型。")
        return
    print(f"✅ 端點可用模型（{len(ids)}）：\n")
    for mid in ids:
        # litellm 接 OpenAI 相容端點需加 openai/ 前綴
        print(f"   {mid:<24} →  MODEL_NAME=openai/{mid}")
    print(
        "\nℹ️ .env 設定範例：\n"
        "   AGENT_MODE=litellm\n"
        f"   MODEL_NAME=openai/{ids[0]}\n"
        f"   LITELLM_BASE_URL={base}\n"
        "   LITELLM_API_KEY=sk-..."
    )


def cmd_valid():
    """用實際金鑰打各供應商 /models 端點，列出真正可用的模型。"""
    import litellm

    # 若設了自架端點，優先直接查它（最貼近實際要用的情境）
    if os.getenv("LITELLM_BASE_URL") or os.getenv("OPENAI_BASE_URL"):
        cmd_endpoint()
        return

    found = _detected_providers()
    print("🔑 偵測到金鑰的供應商：", ", ".join(found) if found else "（無）")
    print("🌐 正在以你的金鑰查詢各供應商可用模型（check_provider_endpoint=True）…\n")

    try:
        models = litellm.get_valid_models(check_provider_endpoint=True)
    except Exception as e:
        print(f"❌ 查詢失敗：{e}")
        print("   可改用： python check_model_list.py --all  （列出目錄上的已知模型）")
        return

    if not models:
        print("⚠️ 沒有取得任何模型。請確認 .env 內金鑰是否正確、或網路是否可連到供應商。")
        return

    # 依供應商前綴分組顯示
    grouped = {}
    for m in sorted(models):
        prefix = m.split("/", 1)[0] if "/" in m else "openai"
        grouped.setdefault(prefix, []).append(m)

    total = 0
    for provider in sorted(grouped):
        items = grouped[provider]
        total += len(items)
        print(f"── {provider}（{len(items)}）" + "─" * 40)
        for m in items:
            print(f"   {m}")
        print()
    print(f"✅ 共 {total} 個可用模型。把要用的字串填到 .env 的 MODEL_NAME 即可。")


def cmd_provider(provider):
    """列出某供應商在 litellm 目錄上的所有已知模型（不需金鑰，但不保證你有權限）。"""
    import litellm

    catalog = litellm.models_by_provider
    if provider not in catalog:
        print(f"❌ 未知供應商：{provider}")
        print("   可用供應商：", ", ".join(sorted(catalog.keys())))
        return
    models = sorted(catalog[provider])
    print(f"📚 {provider} 目錄上的已知模型（{len(models)}）：\n")
    for m in models:
        print(f"   {m}")
    print(f"\nℹ️ 這是 litellm 內建目錄，能否實際使用仍取決於你的金鑰與權限。")


def cmd_all():
    """列出所有供應商及其已知模型數量。"""
    import litellm

    catalog = litellm.models_by_provider
    print(f"📚 litellm 已知供應商（{len(catalog)}），各自模型數量：\n")
    for provider in sorted(catalog):
        print(f"   {provider:<20} {len(catalog[provider])}")
    print("\nℹ️ 用 --provider <名稱> 看某家完整清單，或不帶參數用你的金鑰查實際可用模型。")


def cmd_ollama():
    """查詢本地 Ollama 已安裝模型。"""
    import requests

    base = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
    try:
        resp = requests.get(f"{base}/api/tags", timeout=5)
        resp.raise_for_status()
        models = resp.json().get("models", [])
    except Exception as e:
        print(f"❌ 無法連線到 Ollama（{base}）：{e}")
        print("   請先啟動 Ollama 服務，或用 OLLAMA_URL 指定位址。")
        return

    if not models:
        print("⚠️ Ollama 沒有已安裝的模型，請先 `ollama pull <model>`。")
        return
    print(f"🦙 本地 Ollama 已安裝模型（{base}）：\n")
    for m in models:
        name = m.get("name", "?")
        size_gb = round(m.get("size", 0) / 1e9, 2)
        print(f"   ollama/{name:<30} ({size_gb} GB)")
    print("\nℹ️ litellm 用法：MODEL_NAME=ollama/<name>")


def cmd_test(model):
    """實際對指定模型送出一次最小請求，驗證是否可用。"""
    import litellm

    print(f"🧪 測試模型：{model}")
    api_key = os.getenv("LITELLM_API_KEY")
    api_base = os.getenv("LITELLM_BASE_URL")
    kwargs = {}
    if api_key:
        kwargs["api_key"] = api_key
    if api_base:
        kwargs["api_base"] = api_base

    try:
        resp = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": "請用一句繁體中文回覆：你好"}],
            max_tokens=64,
            **kwargs,
        )
        content = resp.choices[0].message.content
        print(f"✅ 可用！模型回覆：{content}")
    except Exception as e:
        print(f"❌ 不可用：{type(e).__name__}: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="測試 LiteLLM 有哪些模型可選",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--keys", action="store_true", help="只檢查偵測到哪些供應商金鑰")
    group.add_argument("--endpoint", action="store_true", help="列出 LITELLM_BASE_URL 自架端點上的模型")
    group.add_argument("--provider", metavar="NAME", help="列出某供應商目錄上所有已知模型")
    group.add_argument("--all", action="store_true", help="列出所有供應商與其模型數量")
    group.add_argument("--ollama", action="store_true", help="查詢本地 Ollama 已安裝模型")
    group.add_argument("--test", metavar="MODEL", help="實際打一次 API 驗證模型可用")
    args = parser.parse_args()

    if args.keys:
        cmd_keys()
    elif args.endpoint:
        cmd_endpoint()
    elif args.provider:
        cmd_provider(args.provider)
    elif args.all:
        cmd_all()
    elif args.ollama:
        cmd_ollama()
    elif args.test:
        cmd_test(args.test)
    else:
        cmd_valid()


if __name__ == "__main__":
    main()
