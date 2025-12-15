"""
Integration tests for FastAPI application
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import app

client = TestClient(app)


class TestAPIEndpoints:
    """Test cases for API endpoints"""
    
    def test_root_endpoint(self):
        """Test the root health check endpoint"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "online"
        assert "service" in data
        assert "version" in data
    
    def test_list_models_endpoint(self):
        """Test the models listing endpoint"""
        response = client.get("/models")
        
        assert response.status_code == 200
        data = response.json()
        assert "available_models" in data
        assert "pricing_per_1k_tokens" in data
        assert isinstance(data["available_models"], list)
    
    def test_list_task_types_endpoint(self):
        """Test the task types listing endpoint"""
        response = client.get("/task-types")
        
        assert response.status_code == 200
        data = response.json()
        assert "available_task_types" in data
        assert isinstance(data["available_task_types"], list)
    
    def test_metrics_summary_endpoint(self):
        """Test the metrics summary endpoint"""
        response = client.get("/metrics/summary")
        
        assert response.status_code == 200
        # Should return empty or summary based on previous requests
    
    def test_ask_endpoint_validation_empty_question(self):
        """Test ask endpoint with empty question"""
        response = client.post("/ask", json={"question": ""})
        
        assert response.status_code == 400
    
    def test_ask_endpoint_validation_missing_question(self):
        """Test ask endpoint with missing question field"""
        response = client.post("/ask", json={})
        
        assert response.status_code == 422  # Validation error


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
