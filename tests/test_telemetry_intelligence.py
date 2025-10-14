from codex_framework.telemetry import Telemetry
from codex_framework.intelligence import IntelligenceIndexMonitor


def test_telemetry_records_and_exports_dict() -> None:
    telemetry = Telemetry()
    telemetry.record({"goal_id": "g1", "result": "ok"})
    data = telemetry.to_dict()
    assert "events" in data
    assert len(data["events"]) == 1
    assert data["events"][0]["payload"]["goal_id"] == "g1"


def test_intelligence_cii_computation() -> None:
    monitor = IntelligenceIndexMonitor()
    cii = monitor.compute_cii(
        {
            "adaptability": 0.8,
            "clarity": 0.9,
            "ethical_stability": 1.0,
            "innovation_rate": 0.7,
            "reasoning_depth": 0.6,
        }
    )
    assert 0.0 < cii <= 1.0
