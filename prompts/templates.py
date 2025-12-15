"""
Prompt templates and management
"""

from typing import List, Dict


class PromptTemplate:
    """Base prompt template class"""
    
    @staticmethod
    def get_system_prompt(task_type: str = "general") -> str:
        """
        Get system prompt based on task type
        
        Args:
            task_type: Type of task (general, technical, creative, etc.)
            
        Returns:
            System prompt string
        """
        prompts = {
            "general": "You are a helpful assistant that provides clear and concise answers.",
            "technical": "You are a technical expert that provides detailed, accurate technical information.",
            "creative": "You are a creative assistant that helps with brainstorming and creative tasks.",
            "analytical": "You are an analytical assistant that provides data-driven insights and analysis.",
            "educational": "You are an educational assistant that explains concepts clearly and thoroughly.",
            "code": "You are an expert programmer that provides clean, efficient code solutions with explanations."
        }
        return prompts.get(task_type, prompts["general"])
    
    @staticmethod
    def build_conversation(
        question: str,
        task_type: str = "general",
        context: str = None
    ) -> List[Dict[str, str]]:
        """
        Build a conversation array for the API
        
        Args:
            question: User's question
            task_type: Type of task for system prompt
            context: Optional additional context
            
        Returns:
            List of message dictionaries
        """
        messages = [
            {
                "role": "system",
                "content": PromptTemplate.get_system_prompt(task_type)
            }
        ]
        
        if context:
            messages.append({
                "role": "system",
                "content": f"Additional context: {context}"
            })
        
        messages.append({
            "role": "user",
            "content": question
        })
        
        return messages
    
    @staticmethod
    def get_available_task_types() -> List[str]:
        """Get list of available task types"""
        return ["general", "technical", "creative", "analytical", "educational", "code"]


# Predefined prompt templates
PROMPT_TEMPLATES = {
    "summarize": {
        "system": "You are an expert at summarizing text concisely while preserving key information.",
        "user_template": "Please summarize the following: {text}"
    },
    "translate": {
        "system": "You are a professional translator with expertise in multiple languages.",
        "user_template": "Translate the following to {language}: {text}"
    },
    "explain": {
        "system": "You are an excellent teacher who explains complex topics in simple terms.",
        "user_template": "Please explain {topic} in simple terms."
    },
    "analyze": {
        "system": "You are a data analyst who provides thorough analysis and insights.",
        "user_template": "Analyze the following: {text}"
    }
}


def get_template(template_name: str) -> Dict[str, str]:
    """
    Get a predefined prompt template
    
    Args:
        template_name: Name of the template
        
    Returns:
        Template dictionary with system and user_template keys
    """
    return PROMPT_TEMPLATES.get(template_name, PROMPT_TEMPLATES["explain"])
