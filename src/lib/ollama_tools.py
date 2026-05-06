import os


def ollama_web_search(query: str) -> str:
    """
    搜尋網路上的最新資訊，回傳相關網頁的標題、網址與摘要。

    透過呼叫自定義的 Ollama Web Search API，取得與查詢條件相關的網頁結果，
    並將結果格式化為文字字串回傳給 Agent。

    Args:
        query (str): 搜尋的關鍵字或句子。

    Returns:
        str: 格式化後的搜尋結果字串。如果失敗或找不到，則回傳對應提示。
    """
    import requests
    api_key = os.getenv("OLLAMA_WEB_SEARCH_API_KEY", "")
    try:
        # 發送 POST 請求進行網頁搜尋，並設定最大結果數與超時限制
        resp = requests.post(
            "https://ollama.com/api/web_search",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"query": query, "max_results": 5},
            timeout=15
        )
        resp.raise_for_status()

        # 取得 API 回傳的結果列表
        results = resp.json().get("results", [])
        if not results:
            return "未找到相關結果"

        # 整理並格式化搜尋結果
        lines = []
        for r in results:
            lines.append(f"標題: {r.get('title', '')}\nURL: {r.get('url', '')}\n摘要: {r.get('content', '')}\n")
        return "\n".join(lines)
    except Exception as search_err:
        return f"搜尋失敗: {search_err}"
