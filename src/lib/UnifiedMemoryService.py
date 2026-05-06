"""
UnifiedMemoryService
支援三種後端，透過 .env MEMORY_BACKEND 控制：
  - inmemory  : ADK 內建 InMemoryMemoryService
  - postgres  : 自訂 PostgresMemoryService (需要 pgvector / pg_trgm)
  - redis     : 自訂 RedisMemoryService    (需要 RediSearch module)
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# ADK imports
# ---------------------------------------------------------------------------
from google.adk.memory import InMemoryMemoryService
from google.adk.memory.base_memory_service import BaseMemoryService
from google.adk.sessions import Session
from google.genai import types as genai_types

# SearchMemoryResponse / MemoryEntry — ADK 的回傳型別
from google.adk.memory.base_memory_service import (
    SearchMemoryResponse,
    MemoryEntry,
)

# ===========================================================================
# 0. CJK-compatible InMemory (修正 ADK 原生不支援中文 keyword matching)
# ===========================================================================

class CJKInMemoryMemoryService(InMemoryMemoryService):
    """
    繼承 ADK InMemoryMemoryService，override search_memory。
    原版用 \\w+ regex 拆詞，遇到全中文 query 會拆出空 set 導致搜不到。
    改為：英文用詞級比對，中文用字元級子字串比對。
    """

    async def search_memory(
        self,
        *,
        app_name: str,
        user_id: str,
        query: str,
    ) -> SearchMemoryResponse:
        import re, threading

        def _extract_cjk_chars(text: str) -> set[str]:
            """拆出所有 CJK 字元（單字）。"""
            return set(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', text))

        def _extract_ascii_words(text: str) -> set[str]:
            """拆出英文單詞（小寫）。"""
            return set(re.findall(r'[a-zA-Z0-9]+', text.lower()))

        query_cjk   = _extract_cjk_chars(query)
        query_ascii = _extract_ascii_words(query)

        # 取得內部 _session_events（parent class 的私有屬性）
        with self._lock:
            session_event_lists = dict(
                self._session_events.get(f"{app_name}/{user_id}", {})
            )

        memories: list[MemoryEntry] = []
        for session_events in session_event_lists.values():
            for event in session_events:
                if not event.content or not event.content.parts:
                    continue
                event_text = " ".join(
                    p.text for p in event.content.parts if p.text
                )
                if not event_text:
                    continue

                event_cjk   = _extract_cjk_chars(event_text)
                event_ascii = _extract_ascii_words(event_text)

                cjk_match   = bool(query_cjk   and query_cjk   & event_cjk)
                ascii_match = bool(query_ascii  and query_ascii & event_ascii)

                if cjk_match or ascii_match:
                    from google.adk.memory import _utils
                    memories.append(
                        MemoryEntry(
                            content=event.content,
                            author=event.author,
                            timestamp=_utils.format_timestamp(event.timestamp),
                        )
                    )

        return SearchMemoryResponse(memories=memories)

# ===========================================================================
# 1. PostgreSQL Memory Service
# ===========================================================================

class PostgresMemoryService(BaseMemoryService):
    """
    自訂 MemoryService，後端為 PostgreSQL。
    需要的擴充：
      - pg_trgm  (模糊全文搜尋，基本版)
      - pgvector (向量語意搜尋，進階版，選用)

    建表 DDL 會在 __init__ 檢查並自動建立。
    """

    _CREATE_EXTENSION_TRGM = "CREATE EXTENSION IF NOT EXISTS pg_trgm;"
    _CREATE_EXTENSION_VECTOR = "CREATE EXTENSION IF NOT EXISTS vector;"

    _CREATE_TABLE = """
                    CREATE TABLE IF NOT EXISTS adk_memories (
                                                                id          BIGSERIAL PRIMARY KEY,
                                                                app_name    TEXT        NOT NULL,
                                                                user_id     TEXT        NOT NULL,
                                                                session_id  TEXT        NOT NULL,
                                                                author      TEXT,
                                                                content     JSONB       NOT NULL,
                                                                created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
                        );
                    CREATE INDEX IF NOT EXISTS idx_adk_memories_lookup
                        ON adk_memories (app_name, user_id);
                    CREATE INDEX IF NOT EXISTS idx_adk_memories_content_trgm
                        ON adk_memories USING gin ((content::text) gin_trgm_ops); \
                    """

    def __init__(self) -> None:
        try:
            import psycopg2
            import psycopg2.extras
        except ImportError as e:
            raise RuntimeError(
                "psycopg2 未安裝。請執行: pip install psycopg2-binary"
            ) from e

        self._psycopg2 = psycopg2
        self._extras = psycopg2.extras

        dsn = os.environ.get("POSTGRES_DSN")
        if not dsn:
            # 從各別變數組合 DSN
            host = os.environ.get("POSTGRES_HOST", "localhost")
            port = os.environ.get("POSTGRES_PORT", "5432")
            dbname = os.environ.get("POSTGRES_DB", "adk_memory")
            user = os.environ.get("POSTGRES_USER", "postgres")
            password = os.environ.get("POSTGRES_PASSWORD", "")
            dsn = f"host={host} port={port} dbname={dbname} user={user} password={password}"

        self._dsn = dsn
        self._check_connection_and_setup()

    # ------------------------------------------------------------------
    # 初始化：檢查連線 & 擴充 & 建表
    # ------------------------------------------------------------------

    def _check_connection_and_setup(self) -> None:
        logger.info("[PostgresMemoryService] 檢查 PostgreSQL 連線...")
        try:
            conn = self._psycopg2.connect(self._dsn)
        except Exception as e:
            raise RuntimeError(
                f"[PostgresMemoryService] 無法連線到 PostgreSQL: {e}\n"
                f"請確認 DSN 或環境變數 POSTGRES_HOST/PORT/DB/USER/PASSWORD"
            ) from e

        with conn:
            with conn.cursor() as cur:
                # 安裝 pg_trgm（必要）
                try:
                    cur.execute(self._CREATE_EXTENSION_TRGM)
                    logger.info("[PostgresMemoryService] ✅ pg_trgm 擴充已就緒")
                except Exception as e:
                    logger.warning(f"[PostgresMemoryService] ⚠️  pg_trgm 安裝失敗: {e}")

                # 安裝 pgvector（選用）
                try:
                    cur.execute(self._CREATE_EXTENSION_VECTOR)
                    logger.info("[PostgresMemoryService] ✅ pgvector 擴充已就緒")
                except Exception:
                    logger.info("[PostgresMemoryService] ℹ️  pgvector 未安裝，使用純文字搜尋")

                # 建表 & Index
                cur.execute(self._CREATE_TABLE)
                logger.info("[PostgresMemoryService] ✅ adk_memories 表格已就緒")

        conn.close()
        logger.info("[PostgresMemoryService] ✅ 初始化完成")

    def _get_conn(self):
        return self._psycopg2.connect(self._dsn)

    # ------------------------------------------------------------------
    # BaseMemoryService 介面實作
    # ------------------------------------------------------------------

    async def add_session_to_memory(self, session: Session) -> None:
        """將 Session 中所有 events 的內容存入 PostgreSQL。"""
        conn = self._get_conn()
        try:
            with conn:
                with conn.cursor() as cur:
                    for event in session.events or []:
                        if event.content is None:
                            continue
                        content_json = json.dumps(
                            type(event.content).to_dict(event.content)
                            if hasattr(type(event.content), "to_dict")
                            else {"parts": [{"text": p.text} for p in (event.content.parts or []) if p.text]}
                        )
                        cur.execute(
                            """
                            INSERT INTO adk_memories
                                (app_name, user_id, session_id, author, content, created_at)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            """,
                            (
                                session.app_name,
                                session.user_id,
                                session.id,
                                event.author,
                                content_json,
                                datetime.now(timezone.utc),
                            ),
                        )
        finally:
            conn.close()

    async def search_memory(
            self,
            *,
            app_name: str,
            user_id: str,
            query: str,
    ) -> SearchMemoryResponse:
        """使用 pg_trgm 相似度搜尋，回傳最相關的記憶片段。"""
        conn = self._get_conn()
        try:
            with conn.cursor(cursor_factory=self._extras.DictCursor) as cur:
                cur.execute(
                    """
                    SELECT author, content, created_at
                    FROM   adk_memories
                    WHERE  app_name = %s
                      AND  user_id  = %s
                      AND  content::text %% %s
                    ORDER BY similarity(content::text, %s) DESC
                        LIMIT  10
                    """,
                    (app_name, user_id, query, query),
                )
                rows = cur.fetchall()
        finally:
            conn.close()

        memories: list[MemoryEntry] = []
        for row in rows:
            content_dict = row["content"]
            parts = [
                genai_types.Part(text=p["text"])
                for p in content_dict.get("parts", [])
                if p.get("text")
            ]
            memories.append(
                MemoryEntry(
                    content=genai_types.Content(parts=parts),
                    author=row["author"],
                    timestamp=row["created_at"].isoformat() if row["created_at"] else None,
                )
            )
        return SearchMemoryResponse(memories=memories)


# ===========================================================================
# 2. Redis Memory Service
# ===========================================================================

class RedisMemoryService(BaseMemoryService):
    """
    自訂 MemoryService，後端為 Redis。
    需要：
      - Redis Stack 或 Redis + RediSearch module
      - redis-py >= 4.x  (pip install redis)

    Key 結構：
      adk:mem:{app_name}:{user_id}:{session_id}:{event_idx}
    Index：
      FT.CREATE adk_mem_idx ON JSON ...（自動建立）
    """

    _INDEX_NAME = "adk_mem_idx"
    _KEY_PREFIX = "adk:mem:"

    def __init__(self) -> None:
        try:
            import redis
            from redis.commands.search.field import TextField, TagField
            from redis.commands.search.indexDefinition import IndexDefinition, IndexType
        except ImportError as e:
            raise RuntimeError(
                "redis 未安裝。請執行: pip install redis"
            ) from e

        self._redis_mod = redis
        self._TextField = TextField
        self._TagField = TagField
        self._IndexDefinition = IndexDefinition
        self._IndexType = IndexType

        host = os.environ.get("REDIS_HOST", "localhost")
        port = int(os.environ.get("REDIS_PORT", "6379"))
        password = os.environ.get("REDIS_PASSWORD") or None
        db = int(os.environ.get("REDIS_DB", "0"))

        self._client = redis.Redis(
            host=host, port=port, password=password, db=db,
            decode_responses=True,
        )
        self._check_connection_and_setup()

    # ------------------------------------------------------------------
    # 初始化：ping + 檢查 RediSearch module + 建 Index
    # ------------------------------------------------------------------

    def _check_connection_and_setup(self) -> None:
        logger.info("[RedisMemoryService] 檢查 Redis 連線...")

        # 1. Ping
        try:
            self._client.ping()
            logger.info("[RedisMemoryService] ✅ Redis 連線成功")
        except Exception as e:
            raise RuntimeError(
                f"[RedisMemoryService] 無法連線到 Redis: {e}\n"
                f"請確認環境變數 REDIS_HOST/PORT/PASSWORD/DB"
            ) from e

        # 2. 檢查 RediSearch module
        try:
            modules = self._client.module_list()
            module_names = [m.get("name", b"").decode() if isinstance(m.get("name"), bytes) else m.get("name", "") for m in modules]
            if "search" not in [n.lower() for n in module_names]:
                raise RuntimeError(
                    "[RedisMemoryService] ❌ RediSearch module 未載入。\n"
                    "請使用 Redis Stack 或安裝 RediSearch module。\n"
                    "Docker: docker run -p 6379:6379 redis/redis-stack-server"
                )
            logger.info("[RedisMemoryService] ✅ RediSearch module 已就緒")
        except self._redis_mod.exceptions.ResponseError:
            logger.warning("[RedisMemoryService] ⚠️  無法取得 module 列表，跳過 RediSearch 檢查")

        # 3. 建立 Search Index（若不存在）
        self._ensure_index()

    def _ensure_index(self) -> None:
        try:
            self._client.ft(self._INDEX_NAME).info()
            logger.info(f"[RedisMemoryService] ✅ Index '{self._INDEX_NAME}' 已存在")
        except Exception:
            # Index 不存在，建立
            try:
                self._client.ft(self._INDEX_NAME).create_index(
                    fields=[
                        self._TagField("$.app_name", as_name="app_name"),
                        self._TagField("$.user_id",  as_name="user_id"),
                        self._TextField("$.text",    as_name="text"),
                    ],
                    definition=self._IndexDefinition(
                        prefix=[self._KEY_PREFIX],
                        index_type=self._IndexType.JSON,
                    ),
                )
                logger.info(f"[RedisMemoryService] ✅ Index '{self._INDEX_NAME}' 建立完成")
            except Exception as e:
                logger.warning(f"[RedisMemoryService] ⚠️  Index 建立失敗: {e}，將使用 key scan fallback")

    # ------------------------------------------------------------------
    # BaseMemoryService 介面實作
    # ------------------------------------------------------------------

    async def add_session_to_memory(self, session: Session) -> None:
        pipe = self._client.pipeline()
        for idx, event in enumerate(session.events or []):
            if event.content is None:
                continue
            text = " ".join(
                p.text for p in (event.content.parts or []) if p.text
            )
            if not text.strip():
                continue
            key = f"{self._KEY_PREFIX}{session.app_name}:{session.user_id}:{session.id}:{idx}"
            pipe.json().set(key, "$", {
                "app_name":  session.app_name,
                "user_id":   session.user_id,
                "session_id": session.id,
                "author":    event.author or "",
                "text":      text,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
        pipe.execute()

    async def search_memory(
            self,
            *,
            app_name: str,
            user_id: str,
            query: str,
    ) -> SearchMemoryResponse:
        from redis.commands.search.query import Query as RediSearchQuery

        # 安全跳脫特殊字元
        safe_query = query.replace("-", " ").replace("@", "").strip()
        rs_query = (
            f"@app_name:{{{app_name}}} "
            f"@user_id:{{{user_id}}} "
            f"@text:({safe_query})"
        )

        try:
            results = self._client.ft(self._INDEX_NAME).search(
                RediSearchQuery(rs_query).paging(0, 10)
            )
            docs = results.docs
        except Exception as e:
            logger.warning(f"[RedisMemoryService] 搜尋失敗: {e}，回傳空結果")
            return SearchMemoryResponse(memories=[])

        memories: list[MemoryEntry] = []
        for doc in docs:
            data = json.loads(doc.json) if isinstance(doc.json, str) else doc.json
            memories.append(
                MemoryEntry(
                    content=genai_types.Content(
                        parts=[genai_types.Part(text=data.get("text", ""))]
                    ),
                    author=data.get("author"),
                    timestamp=data.get("timestamp"),
                )
            )
        return SearchMemoryResponse(memories=memories)


# ===========================================================================
# 3. UnifiedMemoryService — Factory / Facade
# ===========================================================================

class UnifiedMemoryService:
    """
    根據環境變數 MEMORY_BACKEND 選擇後端：
      inmemory  → ADK InMemoryMemoryService  (預設)
      postgres  → PostgresMemoryService
      redis     → RedisMemoryService

    用法：
        service = UnifiedMemoryService()
        runner  = Runner(..., memory_service=service.backend)
    """

    SUPPORTED_BACKENDS = ("inmemory", "postgres", "redis")

    def __init__(self) -> None:
        backend_name = os.environ.get("MEMORY_BACKEND", "inmemory").lower().strip()

        if backend_name not in self.SUPPORTED_BACKENDS:
            raise ValueError(
                f"MEMORY_BACKEND='{backend_name}' 不支援。"
                f"請選擇: {self.SUPPORTED_BACKENDS}"
            )

        logger.info(f"[UnifiedMemoryService] 使用後端: {backend_name}")

        if backend_name == "inmemory":
            self._backend: BaseMemoryService = CJKInMemoryMemoryService()
            logger.info("[UnifiedMemoryService] ✅ CJKInMemoryMemoryService 已就緒（支援中文，重啟後資料消失）")

        elif backend_name == "postgres":
            self._backend = PostgresMemoryService()

        elif backend_name == "redis":
            self._backend = RedisMemoryService()

        self._backend_name = backend_name

    @property
    def backend(self) -> BaseMemoryService:
        """取得實際的 MemoryService 實例，傳入 ADK Runner 使用。"""
        return self._backend

    @property
    def backend_name(self) -> str:
        return self._backend_name

    # 代理常用方法，讓 UnifiedMemoryService 自己也可以直接當 service 用
    async def add_session_to_memory(self, session: Session) -> None:
        await self._backend.add_session_to_memory(session)

    async def search_memory(self, *, app_name: str, user_id: str, query: str) -> SearchMemoryResponse:
        return await self._backend.search_memory(
            app_name=app_name, user_id=user_id, query=query
        )


# ===========================================================================
# 4. Factory class for services.yaml — ADK 要求 __init__(uri, **kwargs)
# ===========================================================================

class UnifiedMemoryServiceFactory(BaseMemoryService):
    """
    給 services.yaml 用的 wrapper。
    ADK 會呼叫 UnifiedMemoryServiceFactory(uri="unified://", ...)
    實際後端由 .env MEMORY_BACKEND 決定。
    """

    def __init__(self, uri: str = "", **kwargs) -> None:
        unified = UnifiedMemoryService()
        self._backend: BaseMemoryService = unified.backend
        logger.info(f"[UnifiedMemoryServiceFactory] 後端: {unified.backend_name}")

    async def add_session_to_memory(self, session: Session) -> None:
        await self._backend.add_session_to_memory(session)

    async def search_memory(self, *, app_name: str, user_id: str, query: str) -> SearchMemoryResponse:
        return await self._backend.search_memory(
            app_name=app_name, user_id=user_id, query=query
        )