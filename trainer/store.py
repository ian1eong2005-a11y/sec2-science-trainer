"""Process-wide live store. Held in st.cache_resource so every browser session shares it.
Nothing is persisted: a redeploy or restart clears it (teacher's requirement: live, not stored)."""
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .config import CATEGORIES, ONLINE_SECONDS, RECENT_AVOID
from .engine import CatState

Key = Tuple[str, str]


@dataclass
class Attempt:
    ts: float
    category: str
    template_id: str
    chapter: int
    level: int
    chosen: str
    key: str
    correct: bool
    retry: bool
    hints_used: int


@dataclass
class StudentRecord:
    name: str
    cls: str
    login_at: float
    last_active: float
    states: Dict[str, CatState] = field(default_factory=lambda: {c: CatState() for c in CATEGORIES})
    attempts: List[Attempt] = field(default_factory=list)
    recent: Dict[str, deque] = field(default_factory=lambda: {c: deque(maxlen=RECENT_AVOID) for c in CATEGORIES})
    current: Dict[str, object] = field(default_factory=dict)   # category -> Question being answered
    last_chapter: Optional[int] = None

    @property
    def key(self) -> Key:
        return make_key(self.name, self.cls)

    def online(self, now: Optional[float] = None) -> bool:
        return (now or time.time()) - self.last_active <= ONLINE_SECONDS


def make_key(name: str, cls: str) -> Key:
    return (" ".join(name.split()).casefold(), cls)


class LiveStore:
    def __init__(self):
        self._lock = threading.RLock()
        self.students: Dict[Key, StudentRecord] = {}
        self.created_at = time.time()

    # -- students -----------------------------------------------------------
    def login(self, name: str, cls: str) -> StudentRecord:
        name = " ".join(name.split())
        key = make_key(name, cls)
        with self._lock:
            rec = self.students.get(key)
            now = time.time()
            if rec is None:
                rec = StudentRecord(name=name, cls=cls, login_at=now, last_active=now)
                self.students[key] = rec
            else:
                rec.last_active = now
            return rec

    def get(self, key: Key) -> Optional[StudentRecord]:
        with self._lock:
            return self.students.get(key)

    def touch(self, key: Key) -> None:
        with self._lock:
            rec = self.students.get(key)
            if rec:
                rec.last_active = time.time()

    def log_attempt(self, key: Key, attempt: Attempt) -> None:
        with self._lock:
            rec = self.students[key]
            rec.attempts.append(attempt)
            rec.last_active = attempt.ts
            rec.last_chapter = attempt.chapter

    def reset_student(self, key: Key) -> None:
        with self._lock:
            self.students.pop(key, None)

    def clear(self) -> None:
        with self._lock:
            self.students.clear()

    # -- dashboard ----------------------------------------------------------
    def rows(self) -> List[dict]:
        now = time.time()
        with self._lock:
            out = []
            for rec in self.students.values():
                calc, expl = rec.states["calc"], rec.states["explain"]
                first = [a for a in rec.attempts if not a.retry]
                online = rec.online(now)
                out.append({
                    "Name": rec.name,
                    "Class": rec.cls,
                    "Online": "● online" if online else "○ away",
                    "Logged in": time.strftime("%H:%M", time.localtime(rec.login_at)),
                    "Last active": time.strftime("%H:%M:%S", time.localtime(rec.last_active)),
                    "Calc level": calc.level,
                    "Calc streak": f"{calc.correct_streak} right / {calc.wrong_streak} wrong",
                    "Calc best": calc.best_level,
                    "Explain level": expl.level,
                    "Explain streak": f"{expl.correct_streak} right / {expl.wrong_streak} wrong",
                    "Attempted": len(first),
                    "Accuracy %": round(100 * sum(a.correct for a in first) / len(first)) if first else None,
                    "Hints used": sum(a.hints_used for a in rec.attempts),
                    "Last chapter": rec.last_chapter,
                    "_key": rec.key,
                    "_online": online,
                })
            out.sort(key=lambda r: (not r["_online"], r["Class"], r["Name"]))
            return out


_STORE: Optional[LiveStore] = None


def get_store() -> LiveStore:
    """One store per process (Streamlit Cloud runs one process per app, so all sessions share it)."""
    global _STORE
    if _STORE is None:
        _STORE = LiveStore()
    return _STORE
