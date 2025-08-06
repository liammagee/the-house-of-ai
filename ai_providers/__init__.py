"""
AI Providers module for The House of AI

This module provides an abstracted interface for different AI providers,
making it easy to switch between OpenAI, Anthropic, Groq, OpenRouter, 
local models, and fallback rule-based systems.
"""

from .base_provider import AIProvider, AIProviderType, AIProviderError
from .provider_factory import AIProviderFactory, AIProviderManager
from .openai_provider import OpenAIProvider
from .groq_provider import GroqProvider
from .openrouter_provider import OpenRouterProvider
from .anthropic_provider import AnthropicProvider
from .rule_based_provider import RuleBasedProvider

__all__ = [
    'AIProvider', 
    'AIProviderType', 
    'AIProviderError',
    'AIProviderFactory',
    'AIProviderManager',
    'OpenAIProvider',
    'GroqProvider', 
    'OpenRouterProvider',
    'AnthropicProvider',
    'RuleBasedProvider'
]