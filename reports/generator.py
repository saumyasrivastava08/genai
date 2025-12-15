"""
Report generation module for creating usage reports
"""

import json
from typing import List, Dict
from datetime import datetime
from pathlib import Path
from metrics.tracker import RequestMetrics


class ReportGenerator:
    """Generate various reports from metrics data"""
    
    def __init__(self, output_dir: str = "reports/output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_summary_report(self, metrics_history: List[RequestMetrics]) -> Dict:
        """
        Generate a summary report from metrics history
        
        Args:
            metrics_history: List of RequestMetrics objects
            
        Returns:
            Dictionary containing summary statistics
        """
        if not metrics_history:
            return {
                "error": "No metrics data available",
                "generated_at": datetime.now().isoformat()
            }
        
        total_requests = len(metrics_history)
        total_cost = sum(m.estimated_cost_usd for m in metrics_history)
        total_tokens = sum(m.total_tokens for m in metrics_history)
        total_input_tokens = sum(m.input_tokens for m in metrics_history)
        total_output_tokens = sum(m.output_tokens for m in metrics_history)
        avg_latency = sum(m.latency_seconds for m in metrics_history) / total_requests
        
        # Group by model
        model_stats = {}
        for metric in metrics_history:
            if metric.model not in model_stats:
                model_stats[metric.model] = {
                    "requests": 0,
                    "total_cost": 0,
                    "total_tokens": 0
                }
            model_stats[metric.model]["requests"] += 1
            model_stats[metric.model]["total_cost"] += metric.estimated_cost_usd
            model_stats[metric.model]["total_tokens"] += metric.total_tokens
        
        return {
            "summary": {
                "total_requests": total_requests,
                "total_cost_usd": round(total_cost, 6),
                "total_tokens": total_tokens,
                "total_input_tokens": total_input_tokens,
                "total_output_tokens": total_output_tokens,
                "average_latency_seconds": round(avg_latency, 3),
                "average_cost_per_request": round(total_cost / total_requests, 6)
            },
            "model_breakdown": model_stats,
            "generated_at": datetime.now().isoformat()
        }
    
    def save_report(self, report_data: Dict, filename: str = None) -> str:
        """
        Save report to JSON file
        
        Args:
            report_data: Report data dictionary
            filename: Optional custom filename
            
        Returns:
            Path to saved report file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        return str(filepath)
    
    def generate_csv_report(self, metrics_history: List[RequestMetrics]) -> str:
        """
        Generate CSV report from metrics history
        
        Args:
            metrics_history: List of RequestMetrics objects
            
        Returns:
            CSV content as string
        """
        if not metrics_history:
            return "No data available"
        
        headers = [
            "timestamp", "model", "input_tokens", "output_tokens", 
            "total_tokens", "latency_seconds", "estimated_cost_usd", "finish_reason"
        ]
        
        lines = [",".join(headers)]
        
        for metric in metrics_history:
            line = ",".join([
                metric.timestamp,
                metric.model,
                str(metric.input_tokens),
                str(metric.output_tokens),
                str(metric.total_tokens),
                str(metric.latency_seconds),
                str(metric.estimated_cost_usd),
                metric.finish_reason
            ])
            lines.append(line)
        
        return "\n".join(lines)
    
    def save_csv_report(self, metrics_history: List[RequestMetrics], filename: str = None) -> str:
        """
        Save CSV report to file
        
        Args:
            metrics_history: List of RequestMetrics objects
            filename: Optional custom filename
            
        Returns:
            Path to saved CSV file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.csv"
        
        filepath = self.output_dir / filename
        csv_content = self.generate_csv_report(metrics_history)
        
        with open(filepath, 'w') as f:
            f.write(csv_content)
        
        return str(filepath)


# Global report generator instance
report_generator = ReportGenerator()
