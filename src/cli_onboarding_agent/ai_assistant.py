"""
AI Assistant module for the CLI Onboarding Agent.

This module provides AI-powered capabilities for template customization,
content generation, and intelligent conflict resolution using the OpenAI API.
"""

import os
import logging
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union

import openai

# Set up logging
logger = logging.getLogger("cli_onboarding_agent.ai_assistant")


class AIAssistant:
    """
    AI Assistant for enhancing CLI Onboarding Agent with AI capabilities.
    
    This class provides methods for template customization, content generation,
    and intelligent conflict resolution using the OpenAI API.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """
        Initialize the AI Assistant with an API key.
        
        Args:
            api_key: OpenAI API key. If not provided, it will be read from the
                    OPENAI_API_KEY environment variable.
            model: The OpenAI model to use for completions. Default is "gpt-4".
        
        Raises:
            ValueError: If no API key is provided and OPENAI_API_KEY is not set.
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or provide it directly.")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = model
        logger.debug(f"AI Assistant initialized with model {model}")
    
    def generate_content(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
        """
        Generate content based on a prompt.
        
        Args:
            prompt: The prompt to generate content from.
            max_tokens: Maximum number of tokens to generate.
            temperature: Controls randomness. Lower values make output more deterministic.
        
        Returns:
            Generated text content.
        """
        try:
            logger.debug(f"Generating content with prompt: {prompt[:50]}...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for software development."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            
            content = response.choices[0].message.content.strip()
            logger.debug(f"Generated content: {content[:50]}...")
            return content
            
        except Exception as e:
            logger.error(f"Error generating content: {str(e)}")
            return f"Error generating content: {str(e)}"
    
    def analyze_template(self, template_structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a template structure and provide recommendations.
        
        Args:
            template_structure: Dictionary representing the template structure.
        
        Returns:
            Dictionary with analysis results and recommendations.
        """
        try:
            # Convert template structure to a readable format
            template_str = json.dumps(template_structure, indent=2)
            
            prompt = f"""
            Analyze the following project template structure and provide recommendations:
            
            {template_str}
            
            Please provide:
            1. An assessment of the template's completeness
            2. Suggestions for additional files or directories that might be useful
            3. Recommendations for improving the template
            4. Any potential issues or inconsistencies in the structure
            
            Format your response as JSON with the following keys:
            - assessment: Overall assessment of the template
            - suggestions: List of suggested additions
            - recommendations: List of recommendations for improvement
            - issues: List of potential issues
            """
            
            response = self.generate_content(prompt, max_tokens=1000)
            
            # Try to parse the response as JSON
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                # If parsing fails, return a formatted response
                logger.warning("Failed to parse AI response as JSON")
                return {
                    "assessment": "Analysis completed, but response format was not as expected.",
                    "raw_response": response,
                    "suggestions": [],
                    "recommendations": [],
                    "issues": ["Response format error"]
                }
                
        except Exception as e:
            logger.error(f"Error analyzing template: {str(e)}")
            return {
                "assessment": f"Error analyzing template: {str(e)}",
                "suggestions": [],
                "recommendations": [],
                "issues": [str(e)]
            }
    
    def resolve_conflict(self, source_content: str, target_content: str, 
                         file_path: str) -> Tuple[str, str]:
        """
        Resolve conflicts between source and target content.
        
        Args:
            source_content: Content from the source file.
            target_content: Content from the target file.
            file_path: Path to the file with conflict.
        
        Returns:
            Tuple containing (resolved_content, explanation).
        """
        try:
            file_extension = Path(file_path).suffix
            
            prompt = f"""
            I need to resolve a conflict between two versions of a file.
            
            File path: {file_path}
            File type: {file_extension}
            
            SOURCE VERSION:
            ```
            {source_content}
            ```
            
            TARGET VERSION:
            ```
            {target_content}
            ```
            
            Please analyze both versions and create a merged version that preserves the important parts of both.
            Explain your merge strategy and any decisions you made.
            
            Return your response in the following format:
            
            MERGED CONTENT:
            [Your merged content here]
            
            EXPLANATION:
            [Your explanation here]
            """
            
            response = self.generate_content(prompt, max_tokens=2000, temperature=0.3)
            
            # Extract merged content and explanation
            if "MERGED CONTENT:" in response and "EXPLANATION:" in response:
                parts = response.split("EXPLANATION:")
                merged_content = parts[0].replace("MERGED CONTENT:", "").strip()
                explanation = parts[1].strip()
            else:
                # Fallback if the format is not as expected
                merged_content = response
                explanation = "AI generated a merged version but did not follow the expected format."
            
            return merged_content, explanation
            
        except Exception as e:
            logger.error(f"Error resolving conflict: {str(e)}")
            return (
                f"# Error resolving conflict\n# {str(e)}\n\n# SOURCE VERSION:\n{source_content}\n\n# TARGET VERSION:\n{target_content}",
                f"Error resolving conflict: {str(e)}"
            )
    
    def generate_readme(self, project_info: Dict[str, Any]) -> str:
        """
        Generate a README file based on project information.
        
        Args:
            project_info: Dictionary containing project information.
        
        Returns:
            Generated README content.
        """
        try:
            # Extract project information
            project_name = project_info.get("project_name", "Unnamed Project")
            project_description = project_info.get("project_description", "No description provided")
            author = project_info.get("author", "Unknown")
            
            # Get additional information if available
            structure = project_info.get("structure", {})
            structure_str = json.dumps(structure, indent=2) if structure else "Not provided"
            
            prompt = f"""
            Generate a comprehensive README.md file for the following project:
            
            Project Name: {project_name}
            Description: {project_description}
            Author: {author}
            
            Project Structure:
            {structure_str}
            
            The README should include:
            1. A clear title and description
            2. Installation instructions
            3. Usage examples
            4. Project structure explanation
            5. Contributing guidelines
            6. License information
            
            Format the README using proper Markdown syntax with headings, code blocks, lists, etc.
            """
            
            readme_content = self.generate_content(prompt, max_tokens=1500)
            return readme_content
            
        except Exception as e:
            logger.error(f"Error generating README: {str(e)}")
            return f"""# {project_info.get('project_name', 'Project')}

{project_info.get('project_description', 'No description provided')}

## Note
This README was supposed to be AI-generated, but an error occurred: {str(e)}

## Basic Information
- Project: {project_info.get('project_name', 'Unnamed Project')}
- Author: {project_info.get('author', 'Unknown')}
"""
    
    def generate_docstrings(self, code: str, file_path: str) -> str:
        """
        Generate or improve docstrings for code.
        
        Args:
            code: The source code to add docstrings to.
            file_path: Path to the file containing the code.
        
        Returns:
            Code with added or improved docstrings.
        """
        try:
            file_extension = Path(file_path).suffix
            language = "python" if file_extension == ".py" else file_extension.lstrip(".")
            
            prompt = f"""
            Add or improve docstrings for the following {language} code:
            
            ```{language}
            {code}
            ```
            
            Follow these guidelines:
            1. Use the appropriate docstring format for the language
            2. For Python, use Google-style docstrings
            3. Document parameters, return values, and exceptions
            4. Keep the docstrings concise but informative
            5. Do not change the functionality of the code
            
            Return only the improved code with docstrings.
            """
            
            improved_code = self.generate_content(prompt, max_tokens=2000, temperature=0.3)
            
            # Clean up the response to extract just the code
            if "```" in improved_code:
                # Extract code from code blocks
                code_blocks = improved_code.split("```")
                for i in range(1, len(code_blocks), 2):
                    if i < len(code_blocks):
                        # Remove language identifier if present
                        code_part = code_blocks[i]
                        if code_part and "\n" in code_part:
                            first_line, rest = code_part.split("\n", 1)
                            if first_line.strip() in ["python", "py", language, ""]:
                                code_blocks[i] = rest
                
                # Join only the code parts
                improved_code = "".join(code_blocks[1::2])
            
            return improved_code.strip()
            
        except Exception as e:
            logger.error(f"Error generating docstrings: {str(e)}")
            return code  # Return original code on error
    
    def suggest_template_variables(self, template_content: str) -> List[Dict[str, str]]:
        """
        Suggest template variables based on template content.
        
        Args:
            template_content: Content of the template file.
        
        Returns:
            List of dictionaries with variable names and descriptions.
        """
        try:
            prompt = f"""
            Analyze the following template content and suggest variables that could be used for customization:
            
            ```
            {template_content}
            ```
            
            Identify patterns like {{variable_name}} or placeholders that could be replaced with variables.
            
            Return your suggestions as a JSON array of objects with the following structure:
            [
                {{
                    "name": "variable_name",
                    "description": "Description of what this variable represents",
                    "default_value": "Suggested default value"
                }}
            ]
            """
            
            response = self.generate_content(prompt, max_tokens=1000)
            
            # Try to parse the response as JSON
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                logger.warning("Failed to parse AI response as JSON")
                # Return a basic structure with the raw response
                return [
                    {
                        "name": "error",
                        "description": "Failed to parse AI response",
                        "default_value": "",
                        "raw_response": response
                    }
                ]
                
        except Exception as e:
            logger.error(f"Error suggesting template variables: {str(e)}")
            return [
                {
                    "name": "error",
                    "description": f"Error: {str(e)}",
                    "default_value": ""
                }
            ]
