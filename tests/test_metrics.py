"""
Unit tests for metrics module
"""

import pytest
from metrics.tracker import MetricsTracker, RequestMetrics


class TestMetricsTracker:
    """Test cases for MetricsTracker"""
    
    def test_calculate_cost_gpt4o(self):
        """Test cost calculation for GPT-4o"""
        cost = MetricsTracker.calculate_cost("gpt-4o", 1000, 500)
        expected = (1000/1000 * 0.0025) + (500/1000 * 0.01)
        assert cost == round(expected, 6)
    
    def test_calculate_cost_gpt4o_mini(self):
        """Test cost calculation for GPT-4o-mini"""
        cost = MetricsTracker.calculate_cost("gpt-4o-mini", 1000, 500)
        expected = (1000/1000 * 0.00015) + (500/1000 * 0.0006)
        assert cost == round(expected, 6)
    
    def test_calculate_cost_unknown_model(self):
        """Test cost calculation for unknown model"""
        cost = MetricsTracker.calculate_cost("unknown-model", 1000, 500)
        assert cost == 0.0
    
    def test_metrics_tracker_start(self):
        """Test starting the metrics tracker"""
        tracker = MetricsTracker()
        tracker.start()
        assert tracker.start_time is not None
    
    def test_create_metrics(self):
        """Test creating metrics object"""
        tracker = MetricsTracker()
        tracker.start()
        
        metrics = tracker.create_metrics(
            model="gpt-4o-mini",
            input_tokens=100,
            output_tokens=50,
            total_tokens=150,
            finish_reason="stop"
        )
        
        assert isinstance(metrics, RequestMetrics)
        assert metrics.input_tokens == 100
        assert metrics.output_tokens == 50
        assert metrics.total_tokens == 150
        assert metrics.model == "gpt-4o-mini"
        assert metrics.finish_reason == "stop"
        assert metrics.latency_seconds >= 0
    
    def test_get_metrics_dict(self):
        """Test converting metrics to dictionary"""
        tracker = MetricsTracker()
        tracker.start()
        
        metrics = tracker.create_metrics(
            model="gpt-4o-mini",
            input_tokens=100,
            output_tokens=50,
            total_tokens=150,
            finish_reason="stop"
        )
        
        metrics_dict = tracker.get_metrics_dict(metrics)
        
        assert "latency_seconds" in metrics_dict
        assert "tokens" in metrics_dict
        assert metrics_dict["tokens"]["input"] == 100
        assert metrics_dict["tokens"]["output"] == 50
        assert metrics_dict["tokens"]["total"] == 150
    
    def test_summary_statistics(self):
        """Test summary statistics generation"""
        tracker = MetricsTracker()
        
        # Create multiple metrics
        for i in range(3):
            tracker.start()
            tracker.create_metrics(
                model="gpt-4o-mini",
                input_tokens=100,
                output_tokens=50,
                total_tokens=150,
                finish_reason="stop"
            )
        
        summary = tracker.get_summary_statistics()
        
        assert summary["total_requests"] == 3
        assert summary["total_tokens"] == 450
        assert "average_latency_seconds" in summary
        assert "total_cost_usd" in summary


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
