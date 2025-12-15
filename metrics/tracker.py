"""
Metrics tracking and calculation module
"""

import time
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from config.settings import settings


@dataclass
class RequestMetrics:
    """Data class for storing request metrics"""
    latency_seconds: float
    input_tokens: int
    output_tokens: int
    total_tokens: int
    estimated_cost_usd: float
    finish_reason: str
    timestamp: str
    model: str


class MetricsTracker:
    """Handles metrics tracking and cost calculation"""
    
    def __init__(self):
        self.start_time: Optional[float] = None
        self.metrics_history = []
    
    def start(self):
        """Start timing a request"""
        self.start_time = time.time()
    
    def calculate_latency(self) -> float:
        """Calculate request latency"""
        if self.start_time is None:
            return 0.0
        return round(time.time() - self.start_time, 3)
    
    @staticmethod
    def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate estimated cost based on token usage
        
        Args:
            model: Model name
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            
        Returns:
            Estimated cost in USD
        """
        if model not in settings.PRICING:
            return 0.0
        
        input_cost = (input_tokens / 1000) * settings.PRICING[model]["input"]
        output_cost = (output_tokens / 1000) * settings.PRICING[model]["output"]
        return round(input_cost + output_cost, 6)
    
    def create_metrics(
        self, 
        model: str,
        input_tokens: int, 
        output_tokens: int, 
        total_tokens: int,
        finish_reason: str
    ) -> RequestMetrics:
        """
        Create a RequestMetrics object with all calculated metrics
        
        Args:
            model: Model name used
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            total_tokens: Total tokens used
            finish_reason: Why the model stopped generating
            
        Returns:
            RequestMetrics object
        """
        latency = self.calculate_latency()
        cost = self.calculate_cost(model, input_tokens, output_tokens)
        
        metrics = RequestMetrics(
            latency_seconds=latency,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            estimated_cost_usd=cost,
            finish_reason=finish_reason,
            timestamp=datetime.now().isoformat(),
            model=model
        )
        
        self.metrics_history.append(metrics)
        return metrics
    
    def get_metrics_dict(self, metrics: RequestMetrics) -> Dict:
        """Convert RequestMetrics to dictionary format for API response"""
        return {
            "latency_seconds": metrics.latency_seconds,
            "tokens": {
                "input": metrics.input_tokens,
                "output": metrics.output_tokens,
                "total": metrics.total_tokens
            },
            "estimated_cost_usd": metrics.estimated_cost_usd,
            "finish_reason": metrics.finish_reason,
            "timestamp": metrics.timestamp
        }
    
    def get_summary_statistics(self) -> Dict:
        """Get summary statistics from metrics history"""
        if not self.metrics_history:
            return {}
        
        total_requests = len(self.metrics_history)
        total_cost = sum(m.estimated_cost_usd for m in self.metrics_history)
        total_tokens = sum(m.total_tokens for m in self.metrics_history)
        avg_latency = sum(m.latency_seconds for m in self.metrics_history) / total_requests
        
        return {
            "total_requests": total_requests,
            "total_cost_usd": round(total_cost, 6),
            "total_tokens": total_tokens,
            "average_latency_seconds": round(avg_latency, 3),
            "models_used": list(set(m.model for m in self.metrics_history))
        }


# Global metrics tracker instance
metrics_tracker = MetricsTracker()
