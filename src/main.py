"""
Main FastAPI application
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from typing import Optional

from config.settings import settings
from metrics.tracker import metrics_tracker
from prompts.templates import PromptTemplate
from reports.generator import report_generator


app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)


class QuestionRequest(BaseModel):
    """Request model for user question"""
    question: str
    model: Optional[str] = settings.DEFAULT_MODEL
    max_tokens: Optional[int] = settings.DEFAULT_MAX_TOKENS
    temperature: Optional[float] = settings.DEFAULT_TEMPERATURE
    task_type: Optional[str] = "general"


class MetricsResponse(BaseModel):
    """Response model with answer and metrics"""
    question: str
    answer: str
    model: str
    metrics: dict


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": settings.APP_TITLE,
        "version": settings.APP_VERSION
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
    if not settings.OPENAI_API_KEY:
        raise HTTPException(
            status_code=500, 
            detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
        )
    
    # Start metrics tracking
    metrics_tracker.start()
    
    try:
        # Build conversation with appropriate prompt
        messages = PromptTemplate.build_conversation(
            question=request.question,
            task_type=request.task_type
        )
        
        # Make OpenAI API call
        response = client.chat.completions.create(
            model=request.model,
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        # Extract response details
        answer = response.choices[0].message.content
        
        # Create metrics
        request_metrics = metrics_tracker.create_metrics(
            model=request.model,
            input_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
            finish_reason=response.choices[0].finish_reason
        )
        
        return MetricsResponse(
            question=request.question,
            answer=answer,
            model=request.model,
            metrics=metrics_tracker.get_metrics_dict(request_metrics)
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
        "available_models": list(settings.PRICING.keys()),
        "pricing_per_1k_tokens": settings.PRICING,
        "note": "Prices are in USD and may change. Please verify current pricing on OpenAI's website."
    }


@app.get("/task-types")
async def list_task_types():
    """List available task types for prompts"""
    return {
        "available_task_types": PromptTemplate.get_available_task_types(),
        "description": "Task types determine the system prompt behavior"
    }


@app.get("/metrics/summary")
async def get_metrics_summary():
    """Get summary of all metrics collected"""
    return metrics_tracker.get_summary_statistics()


@app.post("/reports/generate")
async def generate_report(format: str = "json"):
    """
    Generate and save a usage report
    
    Args:
        format: Report format ('json' or 'csv')
        
    Returns:
        Report data and file path
    """
    if format not in ["json", "csv"]:
        raise HTTPException(status_code=400, detail="Format must be 'json' or 'csv'")
    
    if not metrics_tracker.metrics_history:
        raise HTTPException(status_code=400, detail="No metrics data available to generate report")
    
    if format == "json":
        report_data = report_generator.generate_summary_report(metrics_tracker.metrics_history)
        filepath = report_generator.save_report(report_data)
        return {
            "report": report_data,
            "saved_to": filepath
        }
    else:
        filepath = report_generator.save_csv_report(metrics_tracker.metrics_history)
        return {
            "message": "CSV report generated successfully",
            "saved_to": filepath
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
