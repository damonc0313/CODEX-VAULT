"""
Comprehensive tests for Cognitive Core.

Production-grade testing with:
- Unit tests
- Integration tests  
- Edge case coverage
- Mocking where appropriate
"""

import pytest
from typing import Dict, Any
from unittest.mock import Mock, patch

from codex_framework.core import CognitiveCore
from codex_framework.exceptions import ValidationError


class TestCognitiveCore:
    """Test suite for CognitiveCore."""
    
    def setup_method(self) -> None:
        """Setup test instance before each test."""
        self.core = CognitiveCore()
        
    def test_initialization(self) -> None:
        """Test cognitive core initializes correctly."""
        assert self.core is not None
        assert self.core.state['active'] is True
        assert self.core.state['version'] == '4.0'
        assert self.core.metacognition is not None
        
    def test_process_decision_basic(self) -> None:
        """Test basic decision processing."""
        result = self.core.process_decision(
            proposition="Test proposition",
            context={'test': True}
        )
        
        assert 'decision' in result
        assert 'confidence' in result
        assert 'ethical_status' in result
        assert isinstance(result['confidence'], float)
        
    def test_process_decision_with_empty_context(self) -> None:
        """Test decision processing with empty context."""
        result = self.core.process_decision(
            proposition="Test",
            context={}
        )

        assert result is not None
        # Should handle gracefully
        assert 'decision' in result

    def test_dialectical_confidence_bounded_by_evidence_weight(self) -> None:
        """Weak evidence should not produce near-certain synthesis confidence."""
        engine = self.core.dialectics
        thesis = engine.generate_argument_for("Sparse proposition", {})
        antithesis = engine.generate_argument_against("Sparse proposition", {})
        synthesis = engine.reconcile(thesis, antithesis)

        assert synthesis.confidence < 0.3
        
    def test_process_decision_high_quality(self) -> None:
        """Test decision with high-quality context."""
        context = {
            'evidence': ['fact1', 'fact2', 'fact3'],
            'confidence': 0.9,
            'ethical_clear': True
        }
        
        result = self.core.process_decision(
            "High quality proposition",
            context
        )
        
        assert result['confidence'] > 0.0
        
    def test_validate_artifact_success(self) -> None:
        """Test artifact validation with good code."""
        good_code = '''
from typing import Dict

def test_func(x: int) -> Dict[str, int]:
    """Test function."""
    return {"result": x}
'''

        result = self.core.validate_artifact(good_code)

        assert 'rigor_passed' in result
        assert 'ethical_passed' in result

    def test_validate_artifact_without_coverage_data(self) -> None:
        """Rigor should pass when coverage data is unavailable."""
        good_code = '''
from typing import Dict

def test_func(x: int) -> Dict[str, int]:
    """Test function."""
    return {"result": x}
'''

        result = self.core.validate_artifact(good_code)

        assert result['rigor_passed'] is True
        assert any(
            'coverage' in recommendation.lower()
            for recommendation in result['recommendations']
        )

    def test_validate_artifact_syntax_error(self) -> None:
        """Test artifact validation with syntax error."""
        bad_code = "def broken( invalid python"
        
        result = self.core.validate_artifact(bad_code)
        
        # Should handle gracefully, not crash
        assert result is not None
        assert result['rigor_passed'] is False
        
    def test_set_mode(self) -> None:
        """Test mode setting."""
        modes = ['analysis', 'architecture', 'build', 'teaching']
        
        for mode in modes:
            self.core.set_mode(mode)
            assert self.core.state['mode'] == mode
            
    def test_get_status(self) -> None:
        """Test status retrieval."""
        status = self.core.get_status()
        
        assert 'state' in status
        assert 'metacognitive_metrics' in status
        assert 'dialectical_balance' in status
        
    def test_decision_coherence_validation(self) -> None:
        """Test that coherence is validated."""
        context = {'key1': 'value1', 'key2': 'value2'}
        
        result = self.core.process_decision("Test", context)
        
        assert 'coherent' in result
        assert isinstance(result['coherent'], bool)
        
    def test_ethical_validation_integration(self) -> None:
        """Test ethical validation is integrated."""
        result = self.core.process_decision(
            "Ethical test",
            {'ethical': True}
        )
        
        assert 'ethical_status' in result
        assert isinstance(result['ethical_status'], bool)
        
    def test_reasoning_transparency(self) -> None:
        """Test reasoning is transparently recorded."""
        result = self.core.process_decision(
            "Transparent test",
            {'transparency': True}
        )
        
        assert 'reasoning' in result
        assert 'decision' in result['reasoning']
        assert 'rationale' in result['reasoning']


class TestCognitiveCoreIntegration:
    """Integration tests for cognitive core with subsystems."""
    
    def setup_method(self) -> None:
        """Setup for integration tests."""
        self.core = CognitiveCore()
        
    def test_full_decision_pipeline(self) -> None:
        """Test complete decision pipeline."""
        # Complex context
        context = {
            'goal': 'Test goal',
            'constraints': ['c1', 'c2'],
            'evidence': ['e1', 'e2', 'e3'],
            'priority': 'high'
        }
        
        result = self.core.process_decision(
            "Complex decision test",
            context
        )
        
        # Verify all subsystems engaged
        assert result['confidence'] >= 0.0
        assert result['ethical_status'] in [True, False]
        assert result['coherent'] in [True, False]
        assert result['reasoning'] is not None
        
    def test_metacognitive_integration(self) -> None:
        """Test metacognition integrates correctly."""
        # Make several decisions
        for i in range(3):
            self.core.process_decision(f"Decision {i}", {})
            
        # Check metacognitive state updated
        status = self.core.get_status()
        assert len(self.core.metacognition.decision_trace) == 3
        
    def test_mode_transitions(self) -> None:
        """Test mode transitions work correctly."""
        modes = ['idle', 'analysis', 'architecture', 'build', 'teaching', 'idle']
        
        for mode in modes:
            self.core.set_mode(mode)
            status = self.core.get_status()
            assert status['state']['mode'] == mode


@pytest.fixture
def cognitive_core() -> CognitiveCore:
    """Fixture providing cognitive core instance."""
    return CognitiveCore()


def test_cognitive_core_fixture(cognitive_core: CognitiveCore) -> None:
    """Test using fixture."""
    assert cognitive_core is not None
    assert cognitive_core.state['active'] is True
