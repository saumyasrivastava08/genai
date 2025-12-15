"""
Configuration settings for the Multi-Task Text Utility
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings"""
    
    # API Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # App Configuration
    APP_TITLE: str = "Multi-Task Text Utility"
    APP_DESCRIPTION: str = "FastAPI backend for OpenAI LLM queries with metrics tracking"
    APP_VERSION: str = "1.0.0"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Model Defaults
    DEFAULT_MODEL: str = "gpt-4o-mini"
    DEFAULT_MAX_TOKENS: int = 500
    DEFAULT_TEMPERATURE: float = 0.7
    
    # Pricing per 1K tokens (Update these based on current OpenAI pricing)
    PRICING = {
        "gpt-4o": {"input": 0.0025, "output": 0.01},
        "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
    }


settings = Settings()
