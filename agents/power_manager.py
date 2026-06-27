"""
CAMAS Agent Power Management Controller
Implements sleep-state scheduling to reduce idle energy.

States: ACTIVE → SLEEP → ACTIVE (on wakeup)
"""

import time
import logging
import threading
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

logger = logging.getLogger(__name__)


class AgentState(Enum):
    ACTIVE = "ACTIVE"
    SLEEP  = "SLEEP"


@dataclass
class SleepStats:
    agent_name: str
    total_active_sec: float = 0.0
    total_sleep_sec: float  = 0.0
    num_wakeups: int        = 0
    num_sleep_events: int   = 0
    state_history: list[dict] = field(default_factory=list)


class PowerManagedAgent:
    """
    Wraps an agent with automatic sleep-state management.

    After `idle_threshold_seconds` of inactivity the agent transitions
    to SLEEP state.  When a new task arrives it wakes up (ACTIVE).
    """

    def __init__(
        self,
        agent_name: str,
        idle_threshold_seconds: float = 30.0,
        db_conn: sqlite3.Connection | None = None,
        run_id: str = "default",
    ):
        self.agent_name = agent_name
        self.idle_threshold = idle_threshold_seconds
        self.db_conn = db_conn
        self.run_id = run_id

        self._state = AgentState.ACTIVE
        self._last_active = time.monotonic()
        self._state_start = time.monotonic()
        self._lock = threading.Lock()
        self._stats = SleepStats(agent_name=agent_name)
        self._pending_logs: list[tuple] = []

        # Background thread to auto-sleep on idle
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop, daemon=True
        )
        self._monitor_thread.start()
        logger.info(f"[{agent_name}] PowerManager started (threshold={idle_threshold_seconds}s)")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def state(self) -> AgentState:
        return self._state

    def notify_task_start(self) -> None:
        """Call when a task is assigned to this agent."""
        with self._lock:
            self._last_active = time.monotonic()
            if self._state == AgentState.SLEEP:
                self._wakeup()

    def notify_task_end(self) -> None:
        """Call when a task completes."""
        with self._lock:
            self._last_active = time.monotonic()

    def get_stats(self) -> SleepStats:
        with self._lock:
            # Flush current state duration
            elapsed = time.monotonic() - self._state_start
            if self._state == AgentState.ACTIVE:
                self._stats.total_active_sec += elapsed
            else:
                self._stats.total_sleep_sec += elapsed
            self._state_start = time.monotonic()
        return self._stats

    def shutdown(self) -> SleepStats:
        """Graceful shutdown; returns final stats."""
        return self.get_stats()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _monitor_loop(self) -> None:
        while True:
            time.sleep(max(1.0, self.idle_threshold / 6))
            with self._lock:
                if self._state == AgentState.ACTIVE:
                    idle = time.monotonic() - self._last_active
                    if idle >= self.idle_threshold:
                        self._sleep()

    def _sleep(self) -> None:
        """Transition to SLEEP state (must hold _lock)."""
        elapsed = time.monotonic() - self._state_start
        self._stats.total_active_sec += elapsed
        self._state = AgentState.SLEEP
        self._state_start = time.monotonic()
        self._stats.num_sleep_events += 1
        event = {
            "state": "SLEEP",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "duration_before_sec": round(elapsed, 3),
        }
        self._stats.state_history.append(event)
        self._log_to_db("SLEEP", round(elapsed, 3))
        logger.debug(f"[{self.agent_name}] → SLEEP (was active {elapsed:.1f}s)")

    def _wakeup(self) -> None:
        """Transition to ACTIVE state (must hold _lock)."""
        elapsed = time.monotonic() - self._state_start
        self._stats.total_sleep_sec += elapsed
        self._state = AgentState.ACTIVE
        self._state_start = time.monotonic()
        self._last_active = time.monotonic()
        self._stats.num_wakeups += 1
        event = {
            "state": "WAKEUP",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sleep_duration_sec": round(elapsed, 3),
        }
        self._stats.state_history.append(event)
        self._log_to_db("WAKEUP", round(elapsed, 3))
        logger.debug(f"[{self.agent_name}] → WAKEUP (slept {elapsed:.1f}s)")

    def _log_to_db(self, state: str, duration_sec: float) -> None:
        if self.db_conn is None:
            return
        # Queue the event; main thread flushes via flush_pending_db_logs()
        self._pending_logs.append((
            self.agent_name, self.run_id, state, duration_sec,
            datetime.now(timezone.utc).isoformat(),
        ))

    def flush_pending_db_logs(self) -> None:
        """Write queued sleep events from the main thread (avoids cross-thread SQLite error)."""
        while self._pending_logs:
            row = self._pending_logs.pop(0)
            try:
                self.db_conn.execute(
                    "INSERT INTO sleep_logs (agent_name, run_id, state, duration_sec, timestamp) "
                    "VALUES (?, ?, ?, ?, ?)", row,
                )
                self.db_conn.commit()
            except Exception as exc:
                logger.warning(f"Failed to flush sleep log: {exc}")
