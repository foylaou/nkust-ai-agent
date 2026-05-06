"""
ADK services.py hook — adk web muilt-agents 啟動時自動載入。
手動把 src/lib 加入 sys.path，再註冊 unified:// memory scheme。
"""
import os
import sys

# __file__ = .../src/muilt-agents/services.py
# lib 在    .../src/lib/
_src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_lib_dir = os.path.join(_src_dir, "lib")

for _p in (_src_dir, _lib_dir):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from UnifiedMemoryService import UnifiedMemoryServiceFactory
from google.adk.cli.service_registry import get_service_registry

# ── Singleton：整個 process 只建一個 instance ──────────────────────────
_memory_service_instance = UnifiedMemoryServiceFactory(uri="unified://")

def _factory(uri: str, **kwargs):
    return _memory_service_instance  # 永遠回傳同一個

get_service_registry().register_memory_service("unified", _factory)
