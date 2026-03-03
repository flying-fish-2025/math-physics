from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4


@dataclass
class SessionState:
    session_id: str
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    objects: dict[str, Any] = field(default_factory=dict)
    traces: list[dict[str, Any]] = field(default_factory=list)


class SessionManager:
    """In-memory stateful storage for MCP object-level workflows."""

    def __init__(self) -> None:
        self._sessions: dict[str, SessionState] = {}

    def create_session(self) -> SessionState:
        session_id = str(uuid4())
        state = SessionState(session_id=session_id)
        self._sessions[session_id] = state
        return state

    def get_or_create(self, session_id: str | None = None) -> SessionState:
        if session_id and session_id in self._sessions:
            return self._sessions[session_id]
        return self.create_session()

    def put_object(self, session_id: str, name: str, value: Any) -> None:
        self._sessions[session_id].objects[name] = value

    def get_object(self, session_id: str, name: str) -> Any:
        if name not in self._sessions[session_id].objects:
            raise KeyError(f"Object '{name}' not found in session {session_id}")
        return self._sessions[session_id].objects[name]

    def list_objects(self, session_id: str) -> dict[str, str]:
        objects = self._sessions[session_id].objects
        return {k: type(v).__name__ for k, v in objects.items()}

    def trace(self, session_id: str, tool: str, args: dict[str, Any], result: Any) -> None:
        self._sessions[session_id].traces.append(
            {
                "ts": datetime.utcnow().isoformat(),
                "tool": tool,
                "args": args,
                "result": str(result),
            }
        )

    def get_traces(self, session_id: str) -> list[dict[str, Any]]:
        return self._sessions[session_id].traces

    def export_session(self, session_id: str) -> dict[str, Any]:
        state = self._sessions[session_id]
        return {
            "session_id": state.session_id,
            "created_at": state.created_at,
            "objects": state.objects,
            "traces": state.traces,
        }

