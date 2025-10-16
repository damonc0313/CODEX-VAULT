"""Telemetry event collection and monitoring system."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime
import logging
import json


@dataclass
class TelemetryEvent:
    """Telemetry event record."""
    
    goal_id: str
    agent_mode: str
    uncertainty: float
    ethical_status: str
    artifact_hash: str
    result: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


class TelemetrySystem:
    """
    Comprehensive telemetry collection system.
    
    Tracks all cognitive events, decisions, and outcomes
    for analysis and learning.
    """
    
    def __init__(self) -> None:
        """Initialize telemetry system."""
        self.logger = logging.getLogger(__name__)
        self.events: List[TelemetryEvent] = []
        self.event_log_path = "codex_framework/telemetry/events.jsonl"
        
    def record_event(
        self,
        goal_id: str,
        agent_mode: str,
        uncertainty: float,
        ethical_status: str,
        artifact_hash: str,
        result: str,
        **metadata: Any
    ) -> None:
        """
        Record a telemetry event.
        
        Args:
            goal_id: Unique goal identifier
            agent_mode: Active agent mode
            uncertainty: Uncertainty level
            ethical_status: Ethical validation status
            artifact_hash: Hash of artifact produced
            result: Outcome result
            **metadata: Additional metadata
        """
        event = TelemetryEvent(
            goal_id=goal_id,
            agent_mode=agent_mode,
            uncertainty=uncertainty,
            ethical_status=ethical_status,
            artifact_hash=artifact_hash,
            result=result,
            metadata=metadata
        )
        
        self.events.append(event)
        self._persist_event(event)
        
        self.logger.debug(f"Recorded event: {goal_id}/{agent_mode}")
        
    def get_events(
        self,
        mode: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[TelemetryEvent]:
        """
        Retrieve telemetry events.
        
        Args:
            mode: Filter by agent mode
            limit: Maximum events to return
            
        Returns:
            List of matching events
        """
        events = self.events
        
        if mode:
            events = [e for e in events if e.agent_mode == mode]
            
        if limit:
            events = events[-limit:]
            
        return events
        
    def get_event_summary(self) -> Dict[str, Any]:
        """
        Get summary of telemetry events.
        
        Returns:
            Summary statistics
        """
        if not self.events:
            return {'total_events': 0}
            
        total = len(self.events)
        
        # Count by mode
        mode_counts: Dict[str, int] = {}
        ethical_pass = 0
        avg_uncertainty = 0.0
        
        for event in self.events:
            mode_counts[event.agent_mode] = (
                mode_counts.get(event.agent_mode, 0) + 1
            )
            if event.ethical_status == 'passed':
                ethical_pass += 1
            avg_uncertainty += event.uncertainty
            
        avg_uncertainty = avg_uncertainty / total if total > 0 else 0
        
        return {
            'total_events': total,
            'mode_distribution': mode_counts,
            'ethical_pass_rate': ethical_pass / total if total > 0 else 0,
            'avg_uncertainty': avg_uncertainty,
            'latest_event': self.events[-1].timestamp if self.events else None
        }
        
    def _persist_event(self, event: TelemetryEvent) -> None:
        """Persist event to log file."""
        try:
            import os
            os.makedirs(
                os.path.dirname(self.event_log_path),
                exist_ok=True
            )
            
            with open(self.event_log_path, 'a') as f:
                event_dict = {
                    'goal_id': event.goal_id,
                    'agent_mode': event.agent_mode,
                    'uncertainty': event.uncertainty,
                    'ethical_status': event.ethical_status,
                    'artifact_hash': event.artifact_hash,
                    'result': event.result,
                    'timestamp': event.timestamp,
                    'metadata': event.metadata
                }
                f.write(json.dumps(event_dict) + '\n')
        except Exception as e:
            self.logger.warning(f"Failed to persist event: {e}")
