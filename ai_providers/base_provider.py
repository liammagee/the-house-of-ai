"""
Abstract base class for AI providers in The House of AI
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from enum import Enum


class AIProviderType(Enum):
    """Enumeration of supported AI provider types"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GROQ = "groq"
    OPENROUTER = "openrouter"
    OLLAMA = "ollama"
    HUGGINGFACE = "huggingface"
    RULE_BASED = "rule_based"


class AIProvider(ABC):
    """
    Abstract base class for AI providers that can generate responses
    for The House of AI consciousness simulation
    """
    
    def __init__(self, provider_type: AIProviderType, **kwargs):
        self.provider_type = provider_type
        self.is_available = False
        self.config = kwargs
        self.initialize()
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the AI provider (set up clients, check API keys, etc.)
        Returns True if initialization successful, False otherwise
        """
        pass
    
    @abstractmethod
    def generate_response(self, 
                         user_action: str, 
                         context: Dict, 
                         user_patterns: Dict, 
                         house_state: Dict) -> Dict:
        """
        Generate an intelligent response based on user action and patterns
        
        Args:
            user_action: The action the user performed
            context: Current context information
            user_patterns: Historical user behavior patterns
            house_state: Current state of the house simulation
            
        Returns:
            Dict containing the AI response with structure:
            {
                "message": "AI response message",
                "analysis": {...},
                "house_modifications": {...},
                "gamification": {...}
            }
        """
        pass
    
    @abstractmethod
    def generate_welcome_message(self) -> str:
        """
        Generate a welcome message for new users
        
        Returns:
            String containing the welcome message
        """
        pass
    
    @abstractmethod
    def generate_consciousness_stream(self, prompt_context: str, room_data: Dict) -> Dict:
        """
        Generate consciousness stream for hotel room inspection
        
        Args:
            prompt_context: Context about the room being inspected
            room_data: Data about the room
            
        Returns:
            Dict containing consciousness stream response
        """
        pass
    
    @abstractmethod
    def generate_hotel_room(self, room_count: int, room_schema: Dict = None) -> Dict:
        """
        Generate a new hotel room with AI-driven characteristics
        
        Args:
            room_count: Current number of rooms
            room_schema: Optional room schema configuration
            
        Returns:
            Dict containing new room data
        """
        pass
    
    @abstractmethod
    def generate_hotel_refresh(self) -> Dict:
        """
        Generate AI response for hotel refresh
        
        Returns:
            Dict containing refresh response
        """
        pass
    
    def check_availability(self) -> bool:
        """
        Check if the provider is currently available
        
        Returns:
            True if available, False otherwise
        """
        return self.is_available
    
    def get_provider_info(self) -> Dict[str, Any]:
        """
        Get information about this provider
        
        Returns:
            Dict containing provider information
        """
        return {
            "type": self.provider_type.value,
            "available": self.is_available,
            "config": {k: v for k, v in self.config.items() if k not in ['api_key', 'token']}
        }


class AIProviderError(Exception):
    """Exception raised when an AI provider encounters an error"""
    
    def __init__(self, provider: AIProvider, message: str, original_error: Exception = None):
        self.provider = provider
        self.original_error = original_error
        super().__init__(f"[{provider.provider_type.value}] {message}")