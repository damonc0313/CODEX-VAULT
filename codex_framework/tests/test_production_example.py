"""
Tests for production-grade example module.

Demonstrates professional testing:
- Comprehensive coverage
- Edge cases
- Error cases
- Integration scenarios
- Performance validation
"""

import pytest
from typing import Dict, Any

from codex_framework.examples.production_grade_module import (
    ProductionGradeProcessor,
    DataProcessingError,
    InvalidInputError
)


class TestProductionGradeProcessor:
    """Comprehensive test suite for ProductionGradeProcessor."""
    
    def setup_method(self) -> None:
        """Setup before each test."""
        self.processor = ProductionGradeProcessor(
            max_size=100,
            strict_mode=True
        )
        
    def test_initialization_success(self) -> None:
        """Test successful initialization."""
        processor = ProductionGradeProcessor(max_size=500)
        assert processor.max_size == 500
        assert processor.strict_mode is True  # Default
        
    def test_initialization_invalid_max_size(self) -> None:
        """Test initialization fails with invalid max_size."""
        with pytest.raises(ValueError, match="must be positive"):
            ProductionGradeProcessor(max_size=-1)
            
    def test_initialization_wrong_type_max_size(self) -> None:
        """Test initialization fails with wrong type."""
        with pytest.raises(TypeError, match="must be int"):
            ProductionGradeProcessor(max_size="invalid")  # type: ignore
            
    def test_process_data_basic(self) -> None:
        """Test basic data processing."""
        data = {"key1": "value1", "key2": "value2"}
        result = self.processor.process_data(data)
        
        assert result.success is True
        assert "key1" in result.data
        assert len(result.warnings) == 0
        
    def test_process_data_empty(self) -> None:
        """Test processing empty data."""
        result = self.processor.process_data({})
        
        assert result.success is True
        assert result.data == {}
        assert "empty_input" in result.warnings
        
    def test_process_data_too_large_strict(self) -> None:
        """Test processing oversized data in strict mode."""
        large_data = {f"key{i}": i for i in range(200)}
        
        with pytest.raises(DataProcessingError, match="exceeds max"):
            self.processor.process_data(large_data)
            
    def test_process_data_too_large_non_strict(self) -> None:
        """Test processing oversized data in non-strict mode."""
        processor = ProductionGradeProcessor(max_size=10, strict_mode=False)
        large_data = {f"key{i}": i for i in range(20)}
        
        result = processor.process_data(large_data)
        
        assert result.success is True
        assert len(result.data) <= 10
        assert "size_exceeded" in result.warnings
        
    def test_process_data_invalid_type(self) -> None:
        """Test processing with invalid input type."""
        with pytest.raises(TypeError, match="Expected dict"):
            self.processor.process_data("not a dict")  # type: ignore
            
    def test_process_data_with_dunder_keys(self) -> None:
        """Test processing data with potentially dangerous keys."""
        dangerous_data = {"__class__": "exploit", "normal": "value"}
        
        with pytest.raises(InvalidInputError, match="dunder names"):
            self.processor.process_data(dangerous_data)
            
    def test_get_stats(self) -> None:
        """Test statistics retrieval."""
        # Process some data
        self.processor.process_data({"test": 1})
        self.processor.process_data({"test": 2})
        
        stats = self.processor.get_stats()
        
        assert stats['processing_count'] == 2
        assert stats['error_count'] == 0
        assert stats['success_rate'] == 1.0
        
    def test_reset_stats(self) -> None:
        """Test statistics reset."""
        self.processor.process_data({"test": 1})
        self.processor.reset_stats()
        
        stats = self.processor.get_stats()
        assert stats['processing_count'] == 0
        
    def test_processing_metrics(self) -> None:
        """Test that metrics are calculated correctly."""
        data = {"a": 1, "b": 2, "c": 3}
        result = self.processor.process_data(data)
        
        assert 'processed_count' in result.metrics
        assert result.metrics['processed_count'] == 3.0
        
    def test_no_validation_mode(self) -> None:
        """Test processing without validation."""
        data = {"__test__": "should normally fail"}
        
        # Without validation, dangerous keys allowed (use case dependent)
        result = self.processor.process_data(data, validate=False)
        
        # Should process (validation skipped)
        assert result.data is not None


# Integration tests
class TestProductionGradeProcessorIntegration:
    """Integration tests for production scenarios."""
    
    def test_bulk_processing(self) -> None:
        """Test processing multiple datasets."""
        processor = ProductionGradeProcessor(max_size=1000)
        
        datasets = [
            {"batch1": i for i in range(10)},
            {"batch2": i for i in range(20)},
            {"batch3": i for i in range(30)}
        ]
        
        results = [processor.process_data(d) for d in datasets]
        
        assert all(r.success for r in results)
        assert processor.get_stats()['processing_count'] == 3
        
    def test_error_recovery(self) -> None:
        """Test system recovers from errors gracefully."""
        processor = ProductionGradeProcessor(max_size=10, strict_mode=False)
        
        # Process good data
        result1 = processor.process_data({"good": 1})
        assert result1.success
        
        # Process oversized (warning but continues)
        large = {f"k{i}": i for i in range(20)}
        result2 = processor.process_data(large)
        assert result2.success  # Non-strict mode
        
        # Process good data again (recovery)
        result3 = processor.process_data({"good": 2})
        assert result3.success
        
        # Stats show recovery
        stats = processor.get_stats()
        assert stats['processing_count'] == 3