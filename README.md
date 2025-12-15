<div align="center">

# 🤖 Multi-Task Text Utility

### AI-Powered Text Processing API with Comprehensive Analytics

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![Python](https://img.shields.io/badge/python-3.8+-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)](LICENSE)

A production-ready FastAPI backend service that processes user questions through OpenAI's LLM models, returning structured JSON responses with comprehensive metrics tracking, cost estimation, and detailed analytics.

[Features](#-features) • [Quick Start](#-quick-start) • [API Documentation](#-api-documentation) • [Examples](#-usage-examples) • [Contributing](#-contributing)

</div>

---

## ✨ Features

- 🚀 **FastAPI Backend**: High-performance RESTful API with automatic OpenAPI documentation
- 🧠 **OpenAI Integration**: Seamless connection to GPT-4o, GPT-4o-mini, and GPT-3.5-turbo
- 📊 **Advanced Metrics**: Real-time tracking of latency, token usage, and cost estimation
- 📈 **Report Generation**: Export usage statistics in JSON and CSV formats
- 🎯 **Smart Prompts**: 6 pre-built task types (general, technical, creative, analytical, educational, code)
- 🎨 **Prompt Templates**: Customizable templates for summarize, translate, explain, and analyze tasks
- ⚡ **Multiple Models**: Support for latest OpenAI models with automatic pricing calculation
- 🧪 **Comprehensive Testing**: Full test suite with pytest (unit + integration tests)
- 🔒 **Secure by Design**: Environment-based configuration with .gitignore protection
- 📦 **Modular Architecture**: Clean separation of concerns (config, metrics, prompts, reports)

## 🎯 Use Cases

- **Customer Support Bots**: Process user queries with detailed analytics
- **Content Generation**: Create summaries, translations, and explanations
- **Research Tools**: Ask complex questions with cost tracking
- **Educational Platforms**: Explain concepts with different teaching styles
- **Development Assistants**: Get code help with technical prompts
- **Analytics Dashboards**: Generate usage reports and monitor API costs

## 📁 Project Structure

```
GenAI/
├── 📂 config/                 # ⚙️ Configuration & Settings
│   ├── __init__.py
│   └── settings.py           # App settings, model pricing, defaults
├── 📂 metrics/                # 📊 Analytics & Tracking
│   ├── __init__.py
│   └── tracker.py            # Latency, tokens, cost calculation
├── 📂 prompts/                # 🎯 Prompt Engineering
│   ├── __init__.py
│   └── templates.py          # Task types & prompt templates
├── 📂 reports/                # 📈 Report Generation
│   ├── __init__.py
│   ├── generator.py          # JSON/CSV export functionality
│   └── output/               # 📁 Generated reports storage
├── 📂 src/                    # 🚀 Core Application
│   ├── __init__.py
│   └── main.py               # FastAPI app & endpoints
├── 📂 tests/                  # 🧪 Test Suite
│   ├── __init__.py
│   ├── test_api.py           # API endpoint tests
│   ├── test_metrics.py       # Metrics module tests
│   ├── test_prompts.py       # Prompts module tests
│   └── test_reports.py       # Reports module tests
├── 📄 .env.example            # 🔐 Environment template
├── 📄 .gitignore              # 🚫 Git exclusions
├── 📄 example_usage.py        # 💡 Usage examples
├── 📄 requirements.txt        # 📦 Dependencies
├── 📄 SETUP_API_KEY.md        # 🔑 API key setup guide
└── 📄 README.md               # 📖 This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Git (for cloning)

### Installation

**1️⃣ Clone the repository**
```bash
git clone https://github.com/saumyasrivastava08/genai.git
cd genai
```

**2️⃣ Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

**3️⃣ Install dependencies**
```bash
pip install -r requirements.txt
```

**4️⃣ Configure environment**
```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

> 📘 **Need help?** See [SETUP_API_KEY.md](SETUP_API_KEY.md) for detailed instructions

**5️⃣ Start the server**
```bash
python src/main.py
```

Server will start at **http://localhost:8000** 🎉

### Quick Test

```bash
# Run example script
python example_usage.py

# Or visit interactive docs
# Open browser: http://localhost:8000/docs
```

## 📚 API Documentation

Once the server is running, explore the interactive documentation:

| Documentation | URL | Description |
|---------------|-----|-------------|
| **Swagger UI** | http://localhost:8000/docs | Interactive API testing interface |
| **ReDoc** | http://localhost:8000/redoc | Clean, readable API documentation |
| **OpenAPI JSON** | http://localhost:8000/openapi.json | Raw OpenAPI specification |

<div align="center">
  <img src="https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black" alt="Swagger" />
  <img src="https://img.shields.io/badge/OpenAPI-6BA539?style=for-the-badge&logo=openapi-initiative&logoColor=white" alt="OpenAPI" />
</div>

## 💻 Usage Examples

### PowerShell (Windows)

```powershell
# Health check
Invoke-RestMethod -Uri http://localhost:8000/

# Ask a question
$body = @{
    question = "What is Python?"
    model = "gpt-4o-mini"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/ask -Method Post -ContentType "application/json" -Body $body

# Get metrics
Invoke-RestMethod -Uri http://localhost:8000/metrics/summary
```

### cURL (Linux/macOS)

```bash
# Health check
curl http://localhost:8000/

# Ask a question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the capital of France?"}'

# List models and pricing
curl http://localhost:8000/models

# Generate report
curl -X POST "http://localhost:8000/reports/generate?format=json"
```

### Python SDK

```python
import requests

class TextUtilityClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def ask(self, question, model="gpt-4o-mini", task_type="general"):
        response = requests.post(
            f"{self.base_url}/ask",
            json={
                "question": question,
                "model": model,
                "task_type": task_type
            }
        )
        return response.json()
    
    def get_metrics(self):
        return requests.get(f"{self.base_url}/metrics/summary").json()

# Usage
client = TextUtilityClient()
result = client.ask("What is FastAPI?", task_type="technical")
print(f"Answer: {result['answer']}")
print(f"Cost: ${result['metrics']['estimated_cost_usd']}")
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

class TextUtilityClient {
  constructor(baseUrl = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }

  async ask(question, options = {}) {
    const response = await axios.post(`${this.baseUrl}/ask`, {
      question,
      model: options.model || 'gpt-4o-mini',
      task_type: options.taskType || 'general',
      max_tokens: options.maxTokens || 500,
      temperature: options.temperature || 0.7
    });
    return response.data;
  }

  async getMetrics() {
    const response = await axios.get(`${this.baseUrl}/metrics/summary`);
    return response.data;
  }

  async generateReport(format = 'json') {
    const response = await axios.post(
      `${this.baseUrl}/reports/generate?format=${format}`
    );
    return response.data;
  }
}

// Usage
(async () => {
  const client = new TextUtilityClient();
  const result = await client.ask('What is machine learning?', {
    taskType: 'educational'
  });
  console.log('Answer:', result.answer);
  console.log('Metrics:', result.metrics);
})();
```

## 🛣️ API Endpoints

### Core Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/` | Health check | ❌ |
| `POST` | `/ask` | Ask a question to AI | ❌ |
| `GET` | `/models` | List available models & pricing | ❌ |
| `GET` | `/task-types` | List prompt task types | ❌ |
| `GET` | `/metrics/summary` | Get usage statistics | ❌ |
| `POST` | `/reports/generate` | Generate usage report | ❌ |
| `GET` | `/docs` | Swagger UI documentation | ❌ |
| `GET` | `/redoc` | ReDoc documentation | ❌ |

### Request/Response Examples

<details>
<summary><b>📤 POST /ask - Ask a Question</b></summary>

**Request Body:**
```json
{
  "question": "Explain quantum computing in simple terms",
  "model": "gpt-4o-mini",
  "max_tokens": 200,
  "temperature": 0.7,
  "task_type": "educational"
}
```

**Response (200 OK):**
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
</details>

<details>
<summary><b>📊 GET /metrics/summary - Usage Statistics</b></summary>

**Response (200 OK):**
```json
{
  "total_requests": 42,
  "total_cost_usd": 0.127,
  "total_tokens": 15420,
  "average_latency_seconds": 1.35,
  "models_used": ["gpt-4o-mini", "gpt-4o"]
}
```
</details>

<details>
<summary><b>📈 POST /reports/generate - Generate Report</b></summary>

**Query Parameters:**
- `format`: `json` or `csv`

**Response (200 OK):**
```json
{
  "report": {
    "summary": {
      "total_requests": 42,
      "total_cost_usd": 0.127,
      "total_tokens": 15420
    },
    "model_breakdown": {
      "gpt-4o-mini": {
        "requests": 35,
        "total_cost": 0.095,
        "total_tokens": 12000
      }
    },
    "generated_at": "2025-12-15T10:30:00"
  },
  "saved_to": "reports/output/report_20251215_103000.json"
}
```
</details>

## ⚙️ Configuration

### Request Parameters

#### POST /ask

| Parameter | Type | Required | Default | Range/Options | Description |
|-----------|------|----------|---------|---------------|-------------|
| `question` | string | ✅ Yes | - | - | The question to ask the AI |
| `model` | string | ❌ No | `gpt-4o-mini` | `gpt-4o`, `gpt-4o-mini`, `gpt-3.5-turbo` | OpenAI model to use |
| `max_tokens` | integer | ❌ No | `500` | `1-4096` | Maximum tokens in response |
| `temperature` | float | ❌ No | `0.7` | `0.0-2.0` | Creativity/randomness level |
| `task_type` | string | ❌ No | `general` | See below | Prompt task type |

#### Available Task Types

| Task Type | Best For | System Prompt Behavior |
|-----------|----------|------------------------|
| `general` | Everyday questions | Helpful, clear, concise answers |
| `technical` | Tech/dev questions | Detailed technical information |
| `creative` | Brainstorming | Creative, innovative ideas |
| `analytical` | Data analysis | Data-driven insights |
| `educational` | Learning/teaching | Clear concept explanations |
| `code` | Programming help | Code solutions with explanations |

### Response Metrics

Each `/ask` response includes comprehensive metrics:

```json
{
  "metrics": {
    "latency_seconds": 1.234,        // Request processing time
    "tokens": {
      "input": 25,                    // Prompt tokens used
      "output": 150,                  // Completion tokens generated
      "total": 175                    // Total tokens consumed
    },
    "estimated_cost_usd": 0.000045,  // Calculated API cost
    "finish_reason": "stop",          // Why generation stopped
    "timestamp": "2025-12-15T..."    // Request timestamp
  }
}
```

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | - | Your OpenAI API secret key |
| `HOST` | ❌ No | `0.0.0.0` | Server bind address |
| `PORT` | ❌ No | `8000` | Server port number |

> ⚠️ **Security**: Never commit `.env` files to version control!

## 💰 Cost Estimation

The application automatically calculates costs based on current OpenAI pricing:

| Model | Input (per 1K tokens) | Output (per 1K tokens) | Best For |
|-------|----------------------|------------------------|----------|
| **GPT-4o** | $0.0025 | $0.0100 | Complex reasoning, highest quality |
| **GPT-4o-mini** | $0.00015 | $0.0006 | Fast responses, cost-effective |
| **GPT-3.5-turbo** | $0.0005 | $0.0015 | Simple tasks, legacy support |

> 💡 **Tip**: Use `gpt-4o-mini` for most tasks to optimize costs
>
> ⚠️ **Note**: Prices may change. Verify current rates at [OpenAI Pricing](https://openai.com/pricing)

### Cost Examples

| Question Length | Response Length | Model | Estimated Cost |
|----------------|-----------------|-------|----------------|
| Short (20 tokens) | Brief (50 tokens) | gpt-4o-mini | ~$0.00003 |
| Medium (50 tokens) | Medium (150 tokens) | gpt-4o-mini | ~$0.00010 |
| Long (100 tokens) | Long (300 tokens) | gpt-4o | ~$0.00550 |

## 🧪 Testing

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
├── test_api.py       # 🌐 API endpoint integration tests
├── test_metrics.py   # 📊 Metrics calculation tests
├── test_prompts.py   # 🎯 Prompt template tests
└── test_reports.py   # 📈 Report generation tests
```

### Coverage

Current test coverage: **~85%**

- ✅ All core functionality tested
- ✅ Edge cases covered
- ✅ Error handling validated

## 🏗️ Development

### Running in Development Mode

```bash
# With auto-reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# With custom port
uvicorn src.main:app --reload --port 8001

# Production mode (no reload)
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Project Architecture

#### 🗂️ Modules Overview

**Config Module** (`config/`)
- Centralized settings management
- Model pricing configuration
- Environment variable handling

**Metrics Module** (`metrics/`)
- Real-time latency tracking
- Token usage monitoring
- Cost calculation engine
- Statistics aggregation

**Prompts Module** (`prompts/`)
- Task-based system prompts
- Template management
- Conversation building

**Reports Module** (`reports/`)
- JSON export functionality
- CSV generation
- Usage analytics

**Source** (`src/`)
- FastAPI application
- Route handlers
- Request/response models

**Tests** (`tests/`)
- Unit tests for each module
- Integration tests for API
- Mocking external dependencies

### Adding New Features

**1. Add a new endpoint:**

```python
# src/main.py
@app.get("/custom-endpoint")
async def custom_endpoint():
    return {"message": "Custom feature"}
```

**2. Add a new prompt template:**

```python
# prompts/templates.py
PROMPT_TEMPLATES["custom_task"] = {
    "system": "Your custom system prompt",
    "user_template": "Template with {placeholder}"
}
```

**3. Extend metrics tracking:**

```python
# metrics/tracker.py
def track_custom_metric(self, value):
    # Your custom tracking logic
    pass
```

## 🔒 Security Best Practices

- ✅ **Environment Variables**: All secrets in `.env` file
- ✅ **`.gitignore` Protection**: `.env` excluded from version control
- ✅ **No Hardcoded Keys**: All credentials externalized
- ⚠️ **Rate Limiting**: Recommended for production
- ⚠️ **Authentication**: Add auth middleware for public deployment
- ⚠️ **HTTPS**: Use HTTPS in production environments
- ⚠️ **CORS**: Configure CORS for web applications

### Production Deployment Checklist

- [ ] Set up reverse proxy (nginx/Apache)
- [ ] Enable HTTPS with SSL certificates
- [ ] Implement rate limiting
- [ ] Add authentication layer
- [ ] Configure CORS properly
- [ ] Set up monitoring and logging
- [ ] Use environment-specific configs
- [ ] Enable API key rotation

## 🐛 Troubleshooting

### Common Issues

<details>
<summary><b>❌ "OpenAI API key not configured" Error</b></summary>

**Solution:**
1. Check `.env` file exists in project root
2. Verify `OPENAI_API_KEY` is set correctly
3. Restart the application
4. Check key starts with `sk-`

```bash
# Verify key is loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('✅ Key loaded' if os.getenv('OPENAI_API_KEY') else '❌ Key NOT loaded')"
```
</details>

<details>
<summary><b>❌ "ModuleNotFoundError" Errors</b></summary>

**Solution:**
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
</details>

<details>
<summary><b>❌ Port Already in Use</b></summary>

**Solution:**
```bash
# Use different port
uvicorn src.main:app --port 8001

# Or kill process on port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS
lsof -i :8000
kill -9 <PID>
```
</details>

<details>
<summary><b>❌ "Error code: 429 - insufficient_quota"</b></summary>

**Solution:**
- Your OpenAI account needs credits
- Go to https://platform.openai.com/account/billing
- Add payment method and credits
- Verify your usage limits
</details>

### Getting Help

- 📖 [OpenAI Documentation](https://platform.openai.com/docs)
- 📚 [FastAPI Documentation](https://fastapi.tiangolo.com/)
- 🐛 [Report Issues](https://github.com/saumyasrivastava08/genai/issues)
- 💬 [Discussions](https://github.com/saumyasrivastava08/genai/discussions)

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

##  Stats

![Python](https://img.shields.io/badge/python-3.8%2B-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-latest-green) ![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

##  Author

**Saumya Srivastava** - [@saumyasrivastava08](https://github.com/saumyasrivastava08)

##  Support

If you find this helpful, please  star the repository!

---

<div align="center">

**Built with  using FastAPI and OpenAI**

[ Back to Top](#-multi-task-text-utility)

</div>
