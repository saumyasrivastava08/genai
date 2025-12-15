"""
Multi-Task Text Utility - FastAPI Backend
Accepts user questions, makes OpenAI API calls, and returns structured JSON with metrics
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import time
import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Multi-Task Text Utility",
    description="FastAPI backend for OpenAI LLM queries with metrics tracking",
    version="1.0.0"
)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Pricing per 1K tokens (Update these based on current OpenAI pricing)
PRICING = {
    "gpt-4o": {"input": 0.0025, "output": 0.01},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
    "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
}


class QuestionRequest(BaseModel):
    """Request model for user question"""
    question: str
    model: Optional[str] = "gpt-4o-mini"
    max_tokens: Optional[int] = 500
    temperature: Optional[float] = 0.7


class MetricsResponse(BaseModel):
    """Response model with answer and metrics"""
    question: str
    answer: str
    model: str
    metrics: dict


def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Calculate estimated cost based on token usage"""
    if model not in PRICING:
        return 0.0
    
    input_cost = (input_tokens / 1000) * PRICING[model]["input"]
    output_cost = (output_tokens / 1000) * PRICING[model]["output"]
    return round(input_cost + output_cost, 6)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Multi-Task Text Utility",
        "version": "1.0.0"
    }


@app.post("/ask", response_model=MetricsResponse)
async def ask_question(request: QuestionRequest):
    """
    Process user question through OpenAI API and return structured response with metrics
    
    Args:
        request: QuestionRequest containing question and optional parameters
        
    Returns:
        MetricsResponse with answer and detailed metrics
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    # Validate API key
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=500, 
            detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
        )
    
    # Start timer for latency measurement
    start_time = time.time()
    
    try:
        # Make OpenAI API call
        response = client.chat.completions.create(
            model=request.model,
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful assistant that provides clear and concise answers."
                },
                {
                    "role": "user", 
                    "content": request.question
                }
            ],
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        # Calculate latency
        latency = round(time.time() - start_time, 3)
        
        # Extract response details
        answer = response.choices[0].message.content
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens
        
        # Calculate estimated cost
        estimated_cost = calculate_cost(request.model, input_tokens, output_tokens)
        
        # Build metrics
        metrics = {
            "latency_seconds": latency,
            "tokens": {
                "input": input_tokens,
                "output": output_tokens,
                "total": total_tokens
            },
            "estimated_cost_usd": estimated_cost,
            "finish_reason": response.choices[0].finish_reason
        }
        
        return MetricsResponse(
            question=request.question,
            answer=answer,
            model=request.model,
            metrics=metrics
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )


@app.get("/models")
async def list_models():
    """List available models with pricing information"""
    return {
        "available_models": list(PRICING.keys()),
        "pricing_per_1k_tokens": PRICING,
        "note": "Prices are in USD and may change. Please verify current pricing on OpenAI's website."
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
