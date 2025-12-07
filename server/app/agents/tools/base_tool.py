"""
Abstract base class for all agent tools.
Defines interface for tool implementation and documentation.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class BaseTool(ABC, BaseModel):
    """
    Abstract base class for all agent tools.
    All tools must inherit from this class and implement the _run method.
    """
    
    name: str = Field(..., description="Name of the tool")
    description: str = Field(..., description="Description of what the tool does")
    
    class Config:
        arbitrary_types_allowed = True
    
    @abstractmethod
    def _run(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Execute the tool's main functionality.
        
        Args:
            **kwargs: Tool-specific parameters
            
        Returns:
            Dict containing the tool's output
        """
        pass
    
    def run(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Public method to run the tool with error handling.
        
        Args:
            **kwargs: Tool-specific parameters
            
        Returns:
            Dict containing the tool's output or error message
        """
        try:
            return self._run(**kwargs)
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "tool": self.name
            }
    
    def get_schema(self) -> Dict[str, Any]:
        """
        Get the tool's schema for LangChain integration.
        
        Returns:
            Dict containing tool metadata
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.schema()
        }
