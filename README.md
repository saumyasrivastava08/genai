# Multi-Task Text Utility

A FastAPI backend service that accepts user questions, makes OpenAI API calls to an LLM endpoint, and returns structured JSON responses with comprehensive metrics tracking.

## Features

- **FastAPI Backend**: RESTful API for processing user questions
- **OpenAI Integration**: Seamlessly connects to OpenAI's LLM models
- **Metrics Tracking**: Captures latency, token usage, and estimated costs
- **Report Generation**: Generate JSON and CSV reports of usage statistics
- **Prompt Templates**: Pre-built and customizable prompt templates
- **Structured JSON Responses**: Clean, well-formatted output
- **Multiple Model Support**: Choose from GPT-4o, GPT-4o-mini, or GPT-3.5-turbo
- **Configurable Parameters**: Adjust temperature, max tokens, and model selection
- **Comprehensive Testing**: Unit and integration tests included

## Project Structure

```
GenAI/
├── config/                 # Configuration settings
│   ├── __init__.py
│   └── settings.py        # Application settings and pricing
├── metrics/               # Metrics tracking module
│   ├── __init__.py
│   └── tracker.py         # Metrics calculation and tracking
├── prompts/               # Prompt templates module
│   ├── __init__.py
│   └── templates.py       # Predefined prompt templates
├── reports/               # Report generation module
│   ├── __init__.py
│   ├── generator.py       # JSON and CSV report generation
│   └── output/            # Generated reports directory
├── src/                   # Main application source
│   ├── __init__.py
│   └── main.py            # FastAPI application
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── test_api.py        # API endpoint tests
│   ├── test_metrics.py    # Metrics module tests
│   ├── test_prompts.py    # Prompts module tests
│   └── test_reports.py    # Reports module tests
├── .env.example           # Environment variable template
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Prerequisites

- Python 3.8 or higher
- OpenAI API key (get one from [OpenAI Platform](https://platform.openai.com/api-keys))

## Setup Instructions

### 1. Clone or Navigate to the Project Directory

```bash
cd "c:\Users\saumya.srivastava\Documents\GenAI"
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate the virtual environment:
- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

   **Important**: Never commit your `.env` file with actual API keys to version control!

### 5. Run the Application

From the project root directory:

```bash
python src/main.py
```

Or using uvicorn directly:
```bash
uvicorn src.main:app --reload
```

The server will start at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- **Interactive API Documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Documentation (ReDoc)**: http://localhost:8000/redoc

## Usage Examples

### 1. Health Check

**Request:**
```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "status": "online",
  "service": "Multi-Task Text Utility",
  "version": "1.0.0"
}
```

### 2. Ask a Question (Basic)

**Request:**
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is the capital of France?\"}"
```

**Response:**
```json
{
  "question": "What is the capital of France?",
  "answer": "The capital of France is Paris.",
  "model": "gpt-4o-mini",
  "metrics": {
    "latency_seconds": 1.234,
    "tokens": {
      "input": 15,
      "output": 8,
      "total": 23
    },
    "estimated_cost_usd": 0.000007,
    "finish_reason": "stop",
    "timestamp": "2025-12-15T10:30:00.123456"
  }
}
```

### 3. Ask a Question with Custom Task Type

**Request:**
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"Explain quantum computing in simple terms\",
    \"model\": \"gpt-4o\",
    \"max_tokens\": 150,
    \"temperature\": 0.5,
    \"task_type\": \"educational\"
  }"
```

### 4. List Available Task Types

**Request:**
```bash
curl http://localhost:8000/task-types
```

**Response:**
```json
{
  "available_task_types": ["general", "technical", "creative", "analytical", "educational", "code"],
  "description": "Task types determine the system prompt behavior"
}
```

### 5. Generate Usage Report

**Request (JSON format):**
```bash
curl -X POST "http://localhost:8000/reports/generate?format=json"
```

**Request (CSV format):**
```bash
curl -X POST "http://localhost:8000/reports/generate?format=csv"
```

### 6. Get Metrics Summary

**Request:**
```bash
curl http://localhost:8000/metrics/summary
```

**Response:**
```json
{
  "total_requests": 10,
  "total_cost_usd": 0.05,
  "total_tokens": 2500,
  "average_latency_seconds": 1.5,
  "models_used": ["gpt-4o-mini", "gpt-4o"]
}
```

### 7. List Available Models

**Request:**
```bash
curl http://localhost:8000/models
```

**Response:**
```json
{
  "available_models": ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
  "pricing_per_1k_tokens": {
    "gpt-4o": {"input": 0.0025, "output": 0.01},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
    "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015}
  },
  "note": "Prices are in USD and may change. Please verify current pricing on OpenAI's website."
}
```

### Python Example

```python
import requests

url = "http://localhost:8000/ask"
payload = {
    "question": "What are the benefits of using FastAPI?",
    "model": "gpt-4o-mini",
    "max_tokens": 200,
    "temperature": 0.7
}

response = requests.post(url, json=payload)
data = response.json()

print(f"Question: {data['question']}")
print(f"Answer: {data['answer']}")
print(f"Tokens used: {data['metrics']['tokens']['total']}")
print(f"Cost: ${data['metrics']['estimated_cost_usd']}")
print(f"Latency: {data['metrics']['latency_seconds']}s")
```

### JavaScript/Node.js Example

```javascript
const axios = require('axios');

async function askQuestion() {
  const response = await axios.post('http://localhost:8000/ask', {
    question: 'What is machine learning?',
    model: 'gpt-4o-mini',
    max_tokens: 150,
    temperature: 0.7
  });

  const data = response.data;
  console.log('Answer:', data.answer);
  console.log('Metrics:', data.metrics);
}

askQuestion();
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check endpoint |
| POST | `/ask` | Submit a question and get an AI response with metrics |
| GET | `/models` | List available models and pricing |
| GET | `/task-types` | List available task types for prompts |
| GET | `/metrics/summary` | Get summary of all collected metrics |
| POST | `/reports/generate` | Generate and save usage report (JSON or CSV) |
| GET | `/docs` | Interactive API documentation (Swagger UI) |
| GET | `/redoc` | Alternative API documentation (ReDoc) |

## Request Parameters

### POST /ask

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| question | string | Yes | - | The question to ask the AI |
| model | string | No | "gpt-4o-mini" | OpenAI model to use |
| max_tokens | integer | No | 500 | Maximum tokens in response |
| temperature | float | No | 0.7 | Randomness (0.0 to 2.0) |
| task_type | string | No | "general" | Type of task (general, technical, creative, etc.) |

## Response Metrics

Each response includes the following metrics:

- **latency_seconds**: Time taken to process the request
- **tokens.input**: Number of input tokens (prompt)
- **tokens.output**: Number of output tokens (completion)
- **tokens.total**: Total tokens used
- **estimated_cost_usd**: Estimated cost in USD based on current pricing
- **finish_reason**: Why the model stopped (e.g., "stop", "length")

## Environment Variables

Create a `.env` file based on `.env.example`:

| Variable | Required | Description |
|----------|----------|-------------|
| OPENAI_API_KEY | Yes | Your OpenAI API key |

## Error Handling

The API returns appropriate HTTP status codes:

- **200**: Successful request
- **400**: Bad request (e.g., empty question)
- **500**: Server error (e.g., OpenAI API issues, missing API key)

## Cost Estimation

The application provides cost estimates based on token usage. Pricing is configured for:

- **GPT-4o**: $0.0025/1K input tokens, $0.01/1K output tokens
- **GPT-4o-mini**: $0.00015/1K input tokens, $0.0006/1K output tokens
- **GPT-3.5-turbo**: $0.0005/1K input tokens, $0.0015/1K output tokens

**Note**: Prices may change. Always verify current pricing on [OpenAI's pricing page](https://openai.com/pricing).

## Development

### Running in Development Mode

```bash
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The `--reload` flag enables auto-reload on code changes.

### Running Tests

Install test dependencies:
```bash
pip install pytest pytest-cov
```

Run all tests:
```bash
pytest tests/ -v
```

Run tests with coverage:
```bash
pytest tests/ -v --cov=. --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_metrics.py -v
```

### Project Modules

#### Config Module (`config/`)
- `settings.py`: Application configuration and pricing information

#### Metrics Module (`metrics/`)
- `tracker.py`: Metrics tracking, cost calculation, and statistics

#### Prompts Module (`prompts/`)
- `templates.py`: Prompt templates for different task types

#### Reports Module (`reports/`)
- `generator.py`: JSON and CSV report generation
- `output/`: Directory for saved reports

#### Source (`src/`)
- `main.py`: FastAPI application with all endpoints

#### Tests (`tests/`)
- `test_api.py`: API endpoint integration tests
- `test_metrics.py`: Metrics module unit tests
- `test_prompts.py`: Prompts module unit tests
- `test_reports.py`: Reports module unit tests

## Security Best Practices

1. **Never commit `.env` files** with real API keys
2. **Keep your OpenAI API key secret** and rotate it if exposed
3. **Use environment variables** for all sensitive configuration
4. **Implement rate limiting** in production environments
5. **Add authentication** if deploying publicly

## Troubleshooting

### "OpenAI API key not configured" error
- Ensure your `.env` file exists and contains a valid `OPENAI_API_KEY`
- Restart the application after adding/updating the `.env` file

### "Module not found" errors
- Activate your virtual environment
- Run `pip install -r requirements.txt` again

### Port already in use
- Change the port in `main.py` or when running uvicorn:
  ```bash
  uvicorn main:app --port 8001
  ```

## License

This project is provided as-is for educational and development purposes.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Support

For issues related to:
- **OpenAI API**: Check [OpenAI's documentation](https://platform.openai.com/docs)
- **FastAPI**: Check [FastAPI documentation](https://fastapi.tiangolo.com/)

---

**Built with FastAPI and OpenAI** 🚀
#   g e n a i  
 #   g e n a i  
 #   g e n a i  
 