"""
Unit tests for prompts module
"""

import pytest
from prompts.templates import PromptTemplate, get_template, PROMPT_TEMPLATES


class TestPromptTemplate:
    """Test cases for PromptTemplate"""
    
    def test_get_system_prompt_general(self):
        """Test getting general system prompt"""
        prompt = PromptTemplate.get_system_prompt("general")
        assert isinstance(prompt, str)
        assert len(prompt) > 0
    
    def test_get_system_prompt_technical(self):
        """Test getting technical system prompt"""
        prompt = PromptTemplate.get_system_prompt("technical")
        assert "technical" in prompt.lower()
    
    def test_get_system_prompt_unknown(self):
        """Test getting prompt for unknown task type defaults to general"""
        prompt = PromptTemplate.get_system_prompt("unknown_type")
        general_prompt = PromptTemplate.get_system_prompt("general")
        assert prompt == general_prompt
    
    def test_build_conversation_basic(self):
        """Test building basic conversation"""
        messages = PromptTemplate.build_conversation("What is AI?")
        
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "What is AI?"
    
    def test_build_conversation_with_context(self):
        """Test building conversation with context"""
        messages = PromptTemplate.build_conversation(
            question="What is AI?",
            context="Focus on machine learning"
        )
        
        assert len(messages) == 3
        assert messages[1]["role"] == "system"
        assert "context" in messages[1]["content"].lower()
    
    def test_build_conversation_with_task_type(self):
        """Test building conversation with specific task type"""
        messages = PromptTemplate.build_conversation(
            question="Explain quantum computing",
            task_type="educational"
        )
        
        assert len(messages) == 2
        assert "educational" in messages[0]["content"].lower()
    
    def test_get_available_task_types(self):
        """Test getting list of available task types"""
        task_types = PromptTemplate.get_available_task_types()
        
        assert isinstance(task_types, list)
        assert len(task_types) > 0
        assert "general" in task_types
        assert "technical" in task_types


class TestPredefinedTemplates:
    """Test cases for predefined templates"""
    
    def test_get_template_summarize(self):
        """Test getting summarize template"""
        template = get_template("summarize")
        
        assert "system" in template
        assert "user_template" in template
        assert isinstance(template["system"], str)
    
    def test_get_template_unknown(self):
        """Test getting unknown template defaults to explain"""
        template = get_template("unknown_template")
        explain_template = get_template("explain")
        
        assert template == explain_template
    
    def test_all_templates_exist(self):
        """Test that all predefined templates are accessible"""
        for template_name in ["summarize", "translate", "explain", "analyze"]:
            template = get_template(template_name)
            assert template is not None
            assert "system" in template
            assert "user_template" in template


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
