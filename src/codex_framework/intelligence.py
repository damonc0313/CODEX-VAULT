from __future__ import annotations

from typing import Dict


class IntelligenceIndexMonitor:
    def compute_cii(self, metrics: Dict[str, float]) -> float:
        required = [
            "adaptability",
            "clarity",
            "ethical_stability",
            "innovation_rate",
            "reasoning_depth",
        ]
        values = [metrics.get(key, 0.0) for key in required]
        return sum(values) / len(values)
