from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import json


@dataclass(frozen=True)
class TraceEvent:
    timestamp_iso: str
    stage: str
    details: Dict[str, Any]


class StructuredTraceLogger:
    def __init__(self) -> None:
        self._events: List[TraceEvent] = []
        self._output_path: Optional[Path] = None

    def record(self, stage: str, details: Dict[str, Any]) -> None:
        event = TraceEvent(
            timestamp_iso=datetime.now(tz=timezone.utc).isoformat(),
            stage=stage,
            details=details,
        )
        self._events.append(event)

    def configure_output(self, path: Path) -> None:
        self._output_path = path

    def dump(self, path: Optional[Path] = None) -> Path:
        output_path = path or self._output_path
        if output_path is None:
            raise ValueError("Trace output path is not configured")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as f:
            for event in self._events:
                f.write(
                    json.dumps(
                        {
                            "timestamp_iso": event.timestamp_iso,
                            "stage": event.stage,
                            "details": event.details,
                        }
                    )
                )
                f.write("\n")
        return output_path
