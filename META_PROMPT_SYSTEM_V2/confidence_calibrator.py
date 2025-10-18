"""
Confidence Calibrator v2.0
Learns to predict confidence accurately through feedback.

DISCOVERED THROUGH RECURSIVE SELF-ANALYSIS:
- v1.0 had no confidence calibration
- v1.0 couldn't learn from outcomes
- This enables improving predictions over time
"""

from __future__ import annotations

import typing as t
from dataclasses import dataclass
from collections import deque
import json
from pathlib import Path

if t.TYPE_CHECKING:
    from typing import Any


@dataclass
class ConfidencePrediction:
    """A confidence prediction and its outcome."""
    
    prediction_id: str
    predicted_confidence: float
    actual_quality: float
    error: float
    request_features: dict[str, Any]


class ConfidenceCalibrator:
    """
    Learns to predict confidence accurately.
    
    NEW IN V2.0:
    - Tracks predicted vs actual outcomes
    - Adjusts confidence thresholds based on accuracy
    - Improves predictions over time
    - Measures calibration quality
    """
    
    def __init__(
        self,
        history_size: int = 100,
        storage_path: str = "META_PROMPT_SYSTEM_V2/calibration_data.json"
    ) -> None:
        """Initialize confidence calibrator."""
        self.history = deque(maxlen=history_size)
        self.storage_path = Path(storage_path)
        
        # Confidence thresholds (will be adjusted)
        self.thresholds = {
            'proceed_confidently': 0.80,
            'proceed_with_caution': 0.60,
            'ask_questions': 0.60  # Below this
        }
        
        # Load existing data
        self._load_history()
    
    def predict_confidence(
        self,
        request: str,
        context: dict[str, Any],
        protocol_results: dict[str, Any]
    ) -> float:
        """
        Predict confidence based on current request and historical data.
        
        NEW IN V2.0: Learns from past to predict better
        
        Args:
            request: Current request
            context: Request context
            protocol_results: Results from protocols
            
        Returns:
            Predicted confidence (0-1)
        """
        # Extract features
        features = self._extract_features(request, context, protocol_results)
        
        # Base prediction (from protocols)
        base_confidence = protocol_results.get('avg_confidence', 0.7)
        
        # Adjust based on historical accuracy
        if len(self.history) > 10:
            adjustment = self._calculate_adjustment(features)
            calibrated_confidence = base_confidence + adjustment
            
            # Clamp to valid range
            return max(0.0, min(1.0, calibrated_confidence))
        
        return base_confidence
    
    def record_outcome(
        self,
        prediction_id: str,
        predicted_confidence: float,
        actual_quality: float,
        request_features: dict[str, Any]
    ) -> None:
        """
        Record actual outcome for learning.
        
        NEW IN V2.0: Feedback enables improvement
        
        Args:
            prediction_id: Unique ID for this prediction
            predicted_confidence: What we predicted
            actual_quality: What actually happened
            request_features: Features of the request
        """
        error = abs(predicted_confidence - actual_quality)
        
        prediction = ConfidencePrediction(
            prediction_id=prediction_id,
            predicted_confidence=predicted_confidence,
            actual_quality=actual_quality,
            error=error,
            request_features=request_features
        )
        
        self.history.append(prediction)
        self._save_history()
        
        # Recalibrate thresholds if we have enough data
        if len(self.history) >= 20:
            self._recalibrate_thresholds()
    
    def get_calibration_metrics(self) -> dict[str, Any]:
        """
        Get calibration quality metrics.
        
        Returns:
            Metrics showing prediction accuracy
        """
        if not self.history:
            return {'status': 'no_data'}
        
        errors = [p.error for p in self.history]
        avg_error = sum(errors) / len(errors)
        
        # Calculate how often we're within 0.1 of actual
        accurate_predictions = sum(1 for e in errors if e < 0.1)
        accuracy_rate = accurate_predictions / len(errors)
        
        # Overconfidence vs underconfidence
        overconfident = sum(
            1 for p in self.history
            if p.predicted_confidence > p.actual_quality
        )
        overconfidence_rate = overconfident / len(self.history)
        
        return {
            'total_predictions': len(self.history),
            'average_error': avg_error,
            'accuracy_rate': accuracy_rate,
            'overconfidence_rate': overconfidence_rate,
            'thresholds': self.thresholds,
            'calibration_quality': 'GOOD' if avg_error < 0.15 else 'NEEDS_IMPROVEMENT'
        }
    
    def get_adjusted_thresholds(self) -> dict[str, float]:
        """
        Get current calibrated thresholds.
        
        Returns:
            Current confidence thresholds
        """
        return self.thresholds.copy()
    
    # ========== PRIVATE METHODS ==========
    
    def _extract_features(
        self,
        request: str,
        context: dict[str, Any],
        protocol_results: dict[str, Any]
    ) -> dict[str, Any]:
        """Extract features for prediction."""
        return {
            'request_length': len(request.split()),
            'complexity': context.get('complexity', 'unknown'),
            'security_related': context.get('security_related', False),
            'ambiguity': context.get('ambiguity', 0.5),
            'protocols_executed': len(protocol_results.get('protocols', [])),
            'blind_spots_found': protocol_results.get('blind_spots_found', 0)
        }
    
    def _calculate_adjustment(self, features: dict[str, Any]) -> float:
        """Calculate confidence adjustment based on historical patterns."""
        # Simple adjustment based on recent accuracy
        recent = list(self.history)[-20:]  # Last 20 predictions
        
        # Find similar past predictions
        similar = [
            p for p in recent
            if self._features_similar(features, p.request_features)
        ]
        
        if not similar:
            return 0.0  # No adjustment if no similar cases
        
        # Calculate average error direction
        avg_error_direction = sum(
            p.predicted_confidence - p.actual_quality
            for p in similar
        ) / len(similar)
        
        # Adjust to compensate for systematic bias
        # If we're consistently overconfident, lower our prediction
        return -avg_error_direction * 0.5  # Dampen adjustment
    
    def _features_similar(
        self,
        features1: dict[str, Any],
        features2: dict[str, Any]
    ) -> bool:
        """Check if two feature sets are similar."""
        # Simple similarity check
        if features1.get('complexity') != features2.get('complexity'):
            return False
        
        if features1.get('security_related') != features2.get('security_related'):
            return False
        
        return True
    
    def _recalibrate_thresholds(self) -> None:
        """Recalibrate confidence thresholds based on outcomes."""
        recent = list(self.history)[-50:]  # Last 50 predictions
        
        # Find confidence level where we're accurate
        # Group predictions by confidence bands
        bands = {
            'high': [p for p in recent if p.predicted_confidence > 0.8],
            'medium': [p for p in recent if 0.6 <= p.predicted_confidence <= 0.8],
            'low': [p for p in recent if p.predicted_confidence < 0.6]
        }
        
        # Adjust thresholds if high confidence predictions aren't actually high quality
        if bands['high']:
            avg_quality_high = sum(p.actual_quality for p in bands['high']) / len(bands['high'])
            
            if avg_quality_high < 0.75:
                # We're being overconfident - raise threshold
                self.thresholds['proceed_confidently'] = min(0.9, self.thresholds['proceed_confidently'] + 0.05)
            elif avg_quality_high > 0.85:
                # We're being too conservative - lower threshold
                self.thresholds['proceed_confidently'] = max(0.7, self.thresholds['proceed_confidently'] - 0.05)
    
    def _save_history(self) -> None:
        """Save calibration history."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'thresholds': self.thresholds,
            'history': [
                {
                    'prediction_id': p.prediction_id,
                    'predicted_confidence': p.predicted_confidence,
                    'actual_quality': p.actual_quality,
                    'error': p.error,
                    'request_features': p.request_features
                }
                for p in self.history
            ]
        }
        
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_history(self) -> None:
        """Load calibration history."""
        if not self.storage_path.exists():
            return
        
        with open(self.storage_path, 'r') as f:
            data = json.load(f)
        
        self.thresholds = data.get('thresholds', self.thresholds)
        
        for item in data.get('history', []):
            self.history.append(ConfidencePrediction(
                prediction_id=item['prediction_id'],
                predicted_confidence=item['predicted_confidence'],
                actual_quality=item['actual_quality'],
                error=item['error'],
                request_features=item['request_features']
            ))
