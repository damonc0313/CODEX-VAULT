from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List


@dataclass(frozen=True)
class TelemetryEvent:
    timestamp_iso: str
    payload: Dict[str, Any]


class Telemetry:
    def __init__(self) -> None:
        self._events: List[TelemetryEvent] = []

    def record(self, payload: Dict[str, Any]) -> None:
        event = TelemetryEvent(
            timestamp_iso=datetime.now(tz=timezone.utc).isoformat(), payload=payload
        )
        self._events.append(event)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "events": [
                {"timestamp_iso": e.timestamp_iso, "payload": e.payload} for e in self._events
            ]
        }
