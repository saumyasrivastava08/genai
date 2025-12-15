"""
Unit tests for reports module
"""

import pytest
from datetime import datetime
from metrics.tracker import RequestMetrics
from reports.generator import ReportGenerator


class TestReportGenerator:
    """Test cases for ReportGenerator"""
    
    def test_generate_summary_report_empty(self):
        """Test generating summary report with no data"""
        generator = ReportGenerator()
        report = generator.generate_summary_report([])
        
        assert "error" in report
        assert "generated_at" in report
    
    def test_generate_summary_report_with_data(self):
        """Test generating summary report with metrics data"""
        generator = ReportGenerator()
        
        # Create sample metrics
        metrics = [
            RequestMetrics(
                latency_seconds=1.5,
                input_tokens=100,
                output_tokens=50,
                total_tokens=150,
                estimated_cost_usd=0.001,
                finish_reason="stop",
                timestamp=datetime.now().isoformat(),
                model="gpt-4o-mini"
            ),
            RequestMetrics(
                latency_seconds=2.0,
                input_tokens=200,
                output_tokens=100,
                total_tokens=300,
                estimated_cost_usd=0.002,
                finish_reason="stop",
                timestamp=datetime.now().isoformat(),
                model="gpt-4o-mini"
            )
        ]
        
        report = generator.generate_summary_report(metrics)
        
        assert "summary" in report
        assert report["summary"]["total_requests"] == 2
        assert report["summary"]["total_tokens"] == 450
        assert report["summary"]["total_cost_usd"] == 0.003
        assert "model_breakdown" in report
        assert "gpt-4o-mini" in report["model_breakdown"]
    
    def test_generate_csv_report_empty(self):
        """Test generating CSV report with no data"""
        generator = ReportGenerator()
        csv = generator.generate_csv_report([])
        
        assert csv == "No data available"
    
    def test_generate_csv_report_with_data(self):
        """Test generating CSV report with metrics data"""
        generator = ReportGenerator()
        
        metrics = [
            RequestMetrics(
                latency_seconds=1.5,
                input_tokens=100,
                output_tokens=50,
                total_tokens=150,
                estimated_cost_usd=0.001,
                finish_reason="stop",
                timestamp="2025-12-15T10:00:00",
                model="gpt-4o-mini"
            )
        ]
        
        csv = generator.generate_csv_report(metrics)
        
        assert "timestamp" in csv
        assert "model" in csv
        assert "input_tokens" in csv
        assert "gpt-4o-mini" in csv
        assert "1.5" in csv
    
    def test_model_breakdown_multiple_models(self):
        """Test report generation with multiple models"""
        generator = ReportGenerator()
        
        metrics = [
            RequestMetrics(
                latency_seconds=1.0,
                input_tokens=100,
                output_tokens=50,
                total_tokens=150,
                estimated_cost_usd=0.001,
                finish_reason="stop",
                timestamp=datetime.now().isoformat(),
                model="gpt-4o"
            ),
            RequestMetrics(
                latency_seconds=1.5,
                input_tokens=200,
                output_tokens=100,
                total_tokens=300,
                estimated_cost_usd=0.002,
                finish_reason="stop",
                timestamp=datetime.now().isoformat(),
                model="gpt-4o-mini"
            )
        ]
        
        report = generator.generate_summary_report(metrics)
        
        assert "gpt-4o" in report["model_breakdown"]
        assert "gpt-4o-mini" in report["model_breakdown"]
        assert report["model_breakdown"]["gpt-4o"]["requests"] == 1
        assert report["model_breakdown"]["gpt-4o-mini"]["requests"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
