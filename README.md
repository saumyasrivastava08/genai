# Multi-Task Text Utility

A FastAPI backend service that processes user questions through OpenAI's LLM models, returning structured JSON responses with comprehensive metrics tracking and cost estimation.

---

## Features

- FastAPI backend with automatic OpenAPI documentation
- OpenAI integration (GPT-4o, GPT-4o-mini, GPT-3.5-turbo)
- Real-time metrics tracking (latency, tokens, cost)
- Report generation (JSON and CSV formats)
- 6 pre-built prompt task types
- Customizable prompt templates
- Comprehensive test suite with pytest
- Environment-based configuration
- Modular architecture

---

## Project Structure

```
GenAI/
├── config/                   # Configuration & Settings
│   ├── __init__.py
│   └── settings.py          # App settings, model pricing, defaults
├── metrics/                 # Analytics & Tracking
│   ├── __init__.py
│   └── tracker.py           # Latency, tokens, cost calculation
├── prompts/                 # Prompt Engineering
│   ├── __init__.py
│   └── templates.py         # Task types & prompt templates
├── reports/                 # Report Generation
│   ├── __init__.py
│   ├── generator.py         # JSON/CSV export functionality
│   └── output/              # Generated reports storage
├── src/                     # Core Application
│   ├── __init__.py
│   └── main.py              # FastAPI app & endpoints
├── tests/                   # Test Suite
│   ├── __init__.py
│   ├── test_api.py          # API endpoint tests
│   ├── test_metrics.py      # Metrics module tests
│   ├── test_prompts.py      # Prompts module tests
│   └── test_reports.py      # Reports module tests
├── .env.example             # Environment template
├── .gitignore               # Git exclusions
├── example_usage.py         # Usage examples
├── requirements.txt         # Dependencies
├── SETUP_API_KEY.md         # API key setup guide
└── README.md                # This file
```

---

## Quick Start

### Step 1: Clone the repository

```bash
git clone https://github.com/saumyasrivastava08/genai.git
cd genai
```

### Step 2: Create virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure environment

```bash
# Copy the example file
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

See [SETUP_API_KEY.md](SETUP_API_KEY.md) for detailed instructions on getting your API key.

### Step 5: Start the server

```bash
python src/main.py
```

Server will start at http://localhost:8000

### Step 6: Test the API

```bash
# Run example script
python example_usage.py

# Or open browser to view interactive docs
http://localhost:8000/docs
```

---

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs (Interactive API testing)
- **ReDoc**: http://localhost:8000/redoc (Clean documentation)
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## Usage Examples

### Testing with PowerShell (Windows)

```powershell
# Health check
Invoke-RestMethod -Uri http://localhost:8000/

# Ask a question
$body = @{
    question = "What is Python?"
    model = "gpt-4o-mini"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/ask -Method Post -ContentType "application/json" -Body $body

# Get metrics summary
Invoke-RestMethod -Uri http://localhost:8000/metrics/summary
```

### Testing with cURL (Linux/macOS)

```bash
# Health check
curl http://localhost:8000/

# Ask a question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the capital of France?"}'

# Get available models
curl http://localhost:8000/models

# Generate usage report
curl -X POST "http://localhost:8000/reports/generate?format=json"
```

### Using Python

```python
import requests

# Ask a question
response = requests.post(
    "http://localhost:8000/ask",
    json={
        "question": "What is FastAPI?",
        "model": "gpt-4o-mini",
        "task_type": "technical"
    }
)

result = response.json()
print(f"Answer: {result['answer']}")
print(f"Cost: ${result['metrics']['estimated_cost_usd']}")
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/ask` | POST | Ask a question to AI |
| `/models` | GET | List available models and pricing |
| `/task-types` | GET | List prompt task types |
| `/metrics/summary` | GET | Get usage statistics |
| `/reports/generate` | POST | Generate usage report (JSON or CSV) |
| `/docs` | GET | Swagger UI documentation |
| `/redoc` | GET | ReDoc documentation |

### Example Request

**POST /ask**

```json
{
  "question": "Explain quantum computing in simple terms",
  "model": "gpt-4o-mini",
  "max_tokens": 200,
  "temperature": 0.7,
  "task_type": "educational"
}
```

**Response:**

```json
{
  "question": "Explain quantum computing in simple terms",
  "answer": "Quantum computing uses quantum mechanics principles...",
  "model": "gpt-4o-mini",
  "metrics": {
    "latency_seconds": 1.234,
    "tokens": {
      "input": 25,
      "output": 150,
      "total": 175
    },
    "estimated_cost_usd": 0.000045,
    "finish_reason": "stop",
    "timestamp": "2025-12-15T10:30:00.123456"
  }
}
```

---

## Configuration

### Request Parameters (POST /ask)

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| question | string | Yes | - | The question to ask the AI |
| model | string | No | gpt-4o-mini | OpenAI model (gpt-4o, gpt-4o-mini, gpt-3.5-turbo) |
| max_tokens | integer | No | 500 | Maximum tokens in response (1-4096) |
| temperature | float | No | 0.7 | Creativity level (0.0-2.0) |
| task_type | string | No | general | Prompt task type |

### Task Types

- **general** - Everyday questions
- **technical** - Technical/development questions
- **creative** - Brainstorming and creative tasks
- **analytical** - Data analysis tasks
- **educational** - Learning and teaching
- **code** - Programming help

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes | - | Your OpenAI API key |
| HOST | No | 0.0.0.0 | Server bind address |
| PORT | No | 8000 | Server port |

---

## Cost Estimation

The application automatically calculates costs based on current OpenAI pricing:

| Model | Input (per 1K tokens) | Output (per 1K tokens) | Best For |
|-------|----------------------|------------------------|----------|
| GPT-4o | $0.0025 | $0.0100 | Complex reasoning, highest quality |
| GPT-4o-mini | $0.00015 | $0.0006 | Fast responses, cost-effective |
| GPT-3.5-turbo | $0.0005 | $0.0015 | Simple tasks, legacy support |

**Recommendations:**
- Use `gpt-4o-mini` for most tasks to optimize costs
- Prices may change - verify current rates at [OpenAI Pricing](https://openai.com/pricing)

### Cost Examples

| Question Length | Response Length | Model | Estimated Cost |
|----------------|-----------------|-------|----------------|
| Short (20 tokens) | Brief (50 tokens) | gpt-4o-mini | ~$0.00003 |
| Medium (50 tokens) | Medium (150 tokens) | gpt-4o-mini | ~$0.00010 |
| Long (100 tokens) | Long (300 tokens) | gpt-4o | ~$0.00550 |

---

## Testing

### Run All Tests

```bash
# Install test dependencies (if not already installed)
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=. --cov-report=html

# Run specific test file
pytest tests/test_metrics.py -v
```

### Test Structure

```
tests/
├── test_api.py       # API endpoint integration tests
├── test_metrics.py   # Metrics calculation tests
├── test_prompts.py   # Prompt template tests
└── test_reports.py   # Report generation tests
```

**Current test coverage:** ~85%

---

## Development

### Running in Development Mode

```bash
# With auto-reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Production mode (no reload, multiple workers)
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Security

- Store all secrets in `.env` file
- `.env` is excluded from git via `.gitignore`
- Never commit API keys to version control
- Use HTTPS in production
- Consider adding rate limiting and authentication for public deployments

---

## Troubleshooting

### OpenAI API key not configured

1. Check `.env` file exists in project root
2. Verify `OPENAI_API_KEY` is set correctly
3. Restart the application
4. Make sure key starts with `sk-`

### ModuleNotFoundError

1. Activate virtual environment
2. Reinstall dependencies

```bash
# Windows
venv\Scripts\activate
pip install -r requirements.txt

# macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
```

### Port Already in Use

```bash
# Use different port
uvicorn src.main:app --port 8001

# Or kill the process using port 8000
# Windows: netstat -ano | findstr :8000
# Linux/macOS: lsof -i :8000
```

### Insufficient Quota Error

Your OpenAI account needs credits. Go to https://platform.openai.com/account/billing to add payment method and credits.

---

## License

This project is provided as-is for educational and development purposes.

---

## Contributing

We welcome contributions! Open issues for bugs or feature requests, submit pull requests for improvements.

### Quick Guide

```bash
git clone https://github.com/saumyasrivastava08/genai.git
cd genai
git checkout -b feature/your-feature
# Make changes
pytest tests/ -v
git commit -am "Add: your feature"
git push origin feature/your-feature
```

---

## Stats

![Python](https://img.shields.io/badge/python-3.8%2B-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-latest-green) ![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

---

## Author

**Saumya Srivastava** - [@saumyasrivastava08](https://github.com/saumyasrivastava08)

---

## Support

For issues related to:
- **OpenAI API**: Check [OpenAI's documentation](https://platform.openai.com/docs)
- **FastAPI**: Check [FastAPI documentation](https://fastapi.tiangolo.com/)

---

**Built with FastAPI and OpenAI** �
#   g e n a i 
 
 #   g e n a i 

##  Contributing

We welcome contributions! Open issues for bugs or feature requests, submit pull requests for improvements.

### Quick Guide
```bash
git clone https://github.com/saumyasrivastava08/genai.git
cd genai
git checkout -b feature/your-feature
# Make changes
pytest tests/ -v
git commit -am "Add: your feature"
git push origin feature/your-feature
```

---

## Stats

![Python](https://img.shields.io/badge/python-3.8%2B-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-latest-green) ![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

---

## Author

**Saumya Srivastava** - [@saumyasrivastava08](https://github.com/saumyasrivastava08)

---

## Support

If you find this helpful, please star the repository!

---

<div align="center">

**Built with FastAPI and OpenAI**

[Back to Top](#multi-task-text-utility)

</div>


