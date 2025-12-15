"""
Example usage script for the Multi-Task Text Utility API
"""

import requests
import json


# API base URL
BASE_URL = "http://localhost:8000"


def check_health():
    """Check if the API is running"""
    print("=== Health Check ===")
    response = requests.get(f"{BASE_URL}/")
    print(json.dumps(response.json(), indent=2))
    print()


def ask_basic_question():
    """Ask a basic question"""
    print("=== Basic Question ===")
    payload = {
        "question": "What is the capital of France?"
    }
    response = requests.post(f"{BASE_URL}/ask", json=payload)
    data = response.json()
    print(f"Question: {data['question']}")
    print(f"Answer: {data['answer']}")
    print(f"Tokens: {data['metrics']['tokens']['total']}")
    print(f"Cost: ${data['metrics']['estimated_cost_usd']}")
    print()


def ask_with_task_type():
    """Ask a question with specific task type"""
    print("=== Question with Task Type (Educational) ===")
    payload = {
        "question": "Explain machine learning",
        "task_type": "educational",
        "max_tokens": 200
    }
    response = requests.post(f"{BASE_URL}/ask", json=payload)
    data = response.json()
    print(f"Answer: {data['answer'][:200]}...")
    print(f"Latency: {data['metrics']['latency_seconds']}s")
    print()


def list_models():
    """List available models"""
    print("=== Available Models ===")
    response = requests.get(f"{BASE_URL}/models")
    data = response.json()
    print("Models:", data['available_models'])
    print()


def list_task_types():
    """List available task types"""
    print("=== Available Task Types ===")
    response = requests.get(f"{BASE_URL}/task-types")
    data = response.json()
    print("Task Types:", data['available_task_types'])
    print()


def get_metrics_summary():
    """Get metrics summary"""
    print("=== Metrics Summary ===")
    response = requests.get(f"{BASE_URL}/metrics/summary")
    print(json.dumps(response.json(), indent=2))
    print()


def generate_report():
    """Generate a usage report"""
    print("=== Generate Report ===")
    response = requests.post(f"{BASE_URL}/reports/generate?format=json")
    if response.status_code == 200:
        data = response.json()
        print(f"Report saved to: {data['saved_to']}")
        print("Summary:", json.dumps(data['report']['summary'], indent=2))
    else:
        print(f"Error: {response.json()}")
    print()


def main():
    """Run all examples"""
    try:
        check_health()
        list_models()
        list_task_types()
        ask_basic_question()
        ask_with_task_type()
        get_metrics_summary()
        generate_report()
        
        print("✓ All examples completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Make sure the server is running.")
        print("Run: python src/main.py")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
