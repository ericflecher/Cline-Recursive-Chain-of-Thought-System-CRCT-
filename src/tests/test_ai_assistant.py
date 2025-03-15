"""
Tests for the AI Assistant module.
"""

import json
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from cli_onboarding_agent.ai_assistant import AIAssistant


@pytest.fixture
def mock_openai_client():
    """Create a mock OpenAI client."""
    mock_client = MagicMock()
    mock_completion = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    
    # Set up the mock response structure
    mock_message.content = "Generated content"
    mock_choice.message = mock_message
    mock_completion.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_completion
    
    return mock_client


@pytest.fixture
def ai_assistant(mock_openai_client):
    """Create an AI assistant with a mock OpenAI client."""
    with patch("openai.OpenAI", return_value=mock_openai_client):
        assistant = AIAssistant(api_key="test_key")
        assistant.client = mock_openai_client
        return assistant


def test_init_with_api_key():
    """Test initializing the AI assistant with an API key."""
    with patch("openai.OpenAI") as mock_openai:
        assistant = AIAssistant(api_key="test_key")
        assert assistant.api_key == "test_key"
        mock_openai.assert_called_once()


def test_init_without_api_key():
    """Test initializing the AI assistant without an API key."""
    with patch("os.environ.get", return_value="env_test_key"), patch("openai.OpenAI"):
        assistant = AIAssistant()
        assert assistant.api_key == "env_test_key"


def test_init_without_api_key_raises_error():
    """Test that initializing without an API key raises an error if the environment variable is not set."""
    with patch("os.environ.get", return_value=None):
        with pytest.raises(ValueError):
            AIAssistant()


def test_generate_content(ai_assistant):
    """Test generating content."""
    content = ai_assistant.generate_content("Test prompt")
    assert content == "Generated content"
    
    # Verify the call to the OpenAI API
    ai_assistant.client.chat.completions.create.assert_called_once()
    call_args = ai_assistant.client.chat.completions.create.call_args[1]
    assert call_args["model"] == ai_assistant.model
    assert len(call_args["messages"]) == 2
    assert call_args["messages"][1]["content"] == "Test prompt"


def test_analyze_template(ai_assistant):
    """Test analyzing a template structure."""
    # Mock the generate_content method to return a JSON string
    mock_response = json.dumps({
        "assessment": "Good template",
        "suggestions": ["Add more files"],
        "recommendations": ["Use better naming"],
        "issues": ["Missing documentation"]
    })
    ai_assistant.generate_content = MagicMock(return_value=mock_response)
    
    template_structure = {"files": ["file1.py", "file2.py"], "dirs": ["dir1", "dir2"]}
    result = ai_assistant.analyze_template(template_structure)
    
    assert result["assessment"] == "Good template"
    assert "Add more files" in result["suggestions"]
    assert "Use better naming" in result["recommendations"]
    assert "Missing documentation" in result["issues"]


def test_analyze_template_invalid_json(ai_assistant):
    """Test analyzing a template structure with invalid JSON response."""
    # Mock the generate_content method to return an invalid JSON string
    ai_assistant.generate_content = MagicMock(return_value="Not a JSON string")
    
    template_structure = {"files": ["file1.py", "file2.py"], "dirs": ["dir1", "dir2"]}
    result = ai_assistant.analyze_template(template_structure)
    
    assert "Analysis completed" in result["assessment"]
    assert "raw_response" in result
    assert result["suggestions"] == []
    assert result["recommendations"] == []
    assert "Response format error" in result["issues"]


def test_resolve_conflict(ai_assistant):
    """Test resolving conflicts between source and target content."""
    # Mock the generate_content method to return a formatted response
    mock_response = """
    MERGED CONTENT:
    This is the merged content.
    
    EXPLANATION:
    This is the explanation.
    """
    ai_assistant.generate_content = MagicMock(return_value=mock_response)
    
    source_content = "Source content"
    target_content = "Target content"
    file_path = "test.py"
    
    merged_content, explanation = ai_assistant.resolve_conflict(source_content, target_content, file_path)
    
    assert merged_content.strip() == "This is the merged content."
    assert explanation.strip() == "This is the explanation."


def test_resolve_conflict_invalid_format(ai_assistant):
    """Test resolving conflicts with an invalid response format."""
    # Mock the generate_content method to return an invalid format
    ai_assistant.generate_content = MagicMock(return_value="Invalid format")
    
    source_content = "Source content"
    target_content = "Target content"
    file_path = "test.py"
    
    merged_content, explanation = ai_assistant.resolve_conflict(source_content, target_content, file_path)
    
    assert merged_content == "Invalid format"
    assert "did not follow the expected format" in explanation


def test_generate_readme(ai_assistant):
    """Test generating a README file."""
    # Mock the generate_content method
    ai_assistant.generate_content = MagicMock(return_value="# Generated README")
    
    project_info = {
        "project_name": "Test Project",
        "project_description": "A test project",
        "author": "Test Author"
    }
    
    readme_content = ai_assistant.generate_readme(project_info)
    
    assert readme_content == "# Generated README"
    ai_assistant.generate_content.assert_called_once()


def test_generate_readme_error(ai_assistant):
    """Test generating a README file with an error."""
    # Mock the generate_content method to raise an exception
    ai_assistant.generate_content = MagicMock(side_effect=Exception("Test error"))
    
    project_info = {
        "project_name": "Test Project",
        "project_description": "A test project",
        "author": "Test Author"
    }
    
    readme_content = ai_assistant.generate_readme(project_info)
    
    assert "Test Project" in readme_content
    assert "Test error" in readme_content


def test_generate_docstrings(ai_assistant):
    """Test generating docstrings for code."""
    # Mock the generate_content method
    ai_assistant.generate_content = MagicMock(return_value="""
    ```python
    def test_function():
        \"\"\"This is a test function.\"\"\"
        pass
    ```
    """)
    
    code = "def test_function():\n    pass"
    file_path = "test.py"
    
    improved_code = ai_assistant.generate_docstrings(code, file_path)
    
    assert "This is a test function" in improved_code
    ai_assistant.generate_content.assert_called_once()


def test_generate_docstrings_error(ai_assistant):
    """Test generating docstrings with an error."""
    # Mock the generate_content method to raise an exception
    ai_assistant.generate_content = MagicMock(side_effect=Exception("Test error"))
    
    code = "def test_function():\n    pass"
    file_path = "test.py"
    
    improved_code = ai_assistant.generate_docstrings(code, file_path)
    
    # Should return the original code on error
    assert improved_code == code


def test_suggest_template_variables(ai_assistant):
    """Test suggesting template variables."""
    # Mock the generate_content method to return a JSON string
    mock_response = json.dumps([
        {
            "name": "project_name",
            "description": "Name of the project",
            "default_value": "My Project"
        }
    ])
    ai_assistant.generate_content = MagicMock(return_value=mock_response)
    
    template_content = "Project: {{project_name}}"
    result = ai_assistant.suggest_template_variables(template_content)
    
    assert len(result) == 1
    assert result[0]["name"] == "project_name"
    assert result[0]["description"] == "Name of the project"
    assert result[0]["default_value"] == "My Project"


def test_suggest_template_variables_invalid_json(ai_assistant):
    """Test suggesting template variables with invalid JSON response."""
    # Mock the generate_content method to return an invalid JSON string
    ai_assistant.generate_content = MagicMock(return_value="Not a JSON string")
    
    template_content = "Project: {{project_name}}"
    result = ai_assistant.suggest_template_variables(template_content)
    
    assert len(result) == 1
    assert result[0]["name"] == "error"
    assert "Failed to parse AI response" in result[0]["description"]
    assert "raw_response" in result[0]
