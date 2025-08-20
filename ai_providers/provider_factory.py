"""
AI Provider Factory for The House of AI

This module provides a factory pattern for creating and configuring AI providers,
making it easy to switch between different AI services.
"""

import os
from typing import Dict, List, Optional, Type
from datetime import datetime
from dotenv import load_dotenv

from .base_provider import AIProvider, AIProviderType, AIProviderError
from .openai_provider import OpenAIProvider
from .groq_provider import GroqProvider
from .openrouter_provider import OpenRouterProvider
from .anthropic_provider import AnthropicProvider
from .rule_based_provider import RuleBasedProvider

# Load environment variables
load_dotenv()


class AIProviderFactory:
    """Factory for creating and managing AI providers"""
    
    # Registry of available providers
    _providers: Dict[AIProviderType, Type[AIProvider]] = {
        AIProviderType.OPENAI: OpenAIProvider,
        AIProviderType.GROQ: GroqProvider,
        AIProviderType.OPENROUTER: OpenRouterProvider,
        AIProviderType.ANTHROPIC: AnthropicProvider,
        AIProviderType.RULE_BASED: RuleBasedProvider,
    }
    
    @classmethod
    def create_provider(cls, provider_type: AIProviderType, **kwargs) -> AIProvider:
        """
        Create an AI provider instance
        
        Args:
            provider_type: The type of provider to create
            **kwargs: Configuration parameters for the provider
            
        Returns:
            Configured AI provider instance
            
        Raises:
            AIProviderError: If provider type is not supported
        """
        if provider_type not in cls._providers:
            raise AIProviderError(
                None, 
                f"Unsupported provider type: {provider_type.value}"
            )
        
        provider_class = cls._providers[provider_type]
        return provider_class(**kwargs)
    
    @classmethod
    def create_from_config(cls, config: Optional[Dict] = None) -> AIProvider:
        """
        Create AI provider from configuration
        
        Args:
            config: Configuration dictionary. If None, uses environment variables.
            
        Returns:
            Configured AI provider instance
        """
        if config is None:
            config = cls.get_config_from_env()
        
        provider_name = config.get('provider', 'rule_based').lower()
        
        # Map string names to enum values
        provider_map = {
            'openai': AIProviderType.OPENAI,
            'groq': AIProviderType.GROQ,
            'openrouter': AIProviderType.OPENROUTER,
            'anthropic': AIProviderType.ANTHROPIC,
            'rule_based': AIProviderType.RULE_BASED,
        }
        
        provider_type = provider_map.get(provider_name)
        if not provider_type:
            print(f"⚠️  Unknown provider '{provider_name}', falling back to rule-based")
            provider_type = AIProviderType.RULE_BASED
        
        # Extract provider-specific configuration
        provider_config = config.copy()
        provider_config.pop('provider', None)  # Remove the provider selector
        
        return cls.create_provider(provider_type, **provider_config)
    
    @classmethod
    def get_config_from_env(cls) -> Dict:
        """
        Get AI provider configuration from environment variables
        
        Returns:
            Configuration dictionary
        """
        config = {
            'provider': os.getenv('AI_PROVIDER', 'rule_based'),
        }
        
        # OpenAI configuration
        if os.getenv('OPENAI_API_KEY'):
            config.update({
                'openai_api_key': os.getenv('OPENAI_API_KEY'),
                'openai_model': os.getenv('OPENAI_MODEL', 'gpt-5'),
                'openai_base_url': os.getenv('OPENAI_BASE_URL'),  # For custom endpoints
            })
        
        # Groq configuration
        if os.getenv('GROQ_API_KEY'):
            config.update({
                'groq_api_key': os.getenv('GROQ_API_KEY'),
                'groq_model': os.getenv('GROQ_MODEL', 'llama-3.1-70b-versatile'),
            })
        
        # OpenRouter configuration
        if os.getenv('OPENROUTER_API_KEY'):
            config.update({
                'openrouter_api_key': os.getenv('OPENROUTER_API_KEY'),
                'openrouter_model': os.getenv('OPENROUTER_MODEL', 'anthropic/claude-3.5-sonnet'),
                'app_name': os.getenv('APP_NAME', 'The House of AI'),
                'site_url': os.getenv('SITE_URL', 'https://github.com/user/the-house-of-ai'),
            })
        
        # Anthropic configuration
        if os.getenv('ANTHROPIC_API_KEY'):
            config.update({
                'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY'),
                'anthropic_model': os.getenv('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022'),
            })
        
        return config
    
    @classmethod
    def get_available_providers(cls) -> List[Dict]:
        """
        Get list of available providers with their status
        
        Returns:
            List of provider information dictionaries
        """
        providers = []
        config = cls.get_config_from_env()
        
        for provider_type in cls._providers:
            try:
                # Create a test instance to check availability
                provider_config = cls._extract_provider_config(config, provider_type)
                provider = cls.create_provider(provider_type, **provider_config)
                
                provider_info = provider.get_provider_info()
                provider_info['supported'] = True
                providers.append(provider_info)
                
            except Exception as e:
                providers.append({
                    'type': provider_type.value,
                    'available': False,
                    'supported': True,
                    'error': str(e)
                })
        
        return providers
    
    @classmethod
    def auto_select_provider(cls) -> AIProvider:
        """
        Automatically select the best available AI provider
        
        Returns:
            The best available AI provider instance
        """
        config = cls.get_config_from_env()
        
        # Check if user specified a preferred provider
        preferred_provider = os.getenv('AI_PROVIDER', '').upper()
        if preferred_provider:
            try:
                # Convert string to enum by name (not value)
                provider_type = getattr(AIProviderType, preferred_provider)
                provider_config = cls._extract_provider_config(config, provider_type)
                print(f"🎯 Trying preferred provider from AI_PROVIDER: {provider_type.value}")
                print(f"   Config keys: {list(provider_config.keys())}")
                
                provider = cls.create_provider(provider_type, **provider_config)
                
                if provider.check_availability():
                    print(f"✅ Using preferred AI provider: {provider_type.value}")
                    return provider
                else:
                    print(f"❌ Preferred provider {provider_type.value} not available, trying alternatives")
                    
            except (ValueError, Exception) as e:
                print(f"❌ Invalid or failed preferred provider '{preferred_provider}': {e}")
        
        # Priority order for automatic provider selection
        priority_order = [
            AIProviderType.OPENAI,
            AIProviderType.ANTHROPIC,
            AIProviderType.GROQ,
            AIProviderType.OPENROUTER,
            AIProviderType.RULE_BASED,  # Always available as fallback
        ]
        
        print("🔄 Auto-selecting provider from priority list...")
        for provider_type in priority_order:
            try:
                provider_config = cls._extract_provider_config(config, provider_type)
                print(f"🔍 Trying provider: {provider_type.value}")
                print(f"   Config keys: {list(provider_config.keys())}")
                
                provider = cls.create_provider(provider_type, **provider_config)
                
                if provider.check_availability():
                    print(f"✅ Auto-selected AI provider: {provider_type.value}")
                    return provider
                else:
                    print(f"❌ Provider {provider_type.value} not available")
                    
            except Exception as e:
                print(f"❌ Provider {provider_type.value} failed: {str(e)[:100]}")
                continue
        
        # Fallback to rule-based (should never reach here since rule-based is always available)
        print("⚠️  All providers failed, using rule-based fallback")
        return cls.create_provider(AIProviderType.RULE_BASED)
    
    @classmethod
    def _extract_provider_config(cls, config: Dict, provider_type: AIProviderType) -> Dict:
        """Extract configuration for a specific provider"""
        provider_config = {}
        
        if provider_type == AIProviderType.OPENAI:
            provider_config = {
                'api_key': config.get('openai_api_key'),
                'model': config.get('openai_model', 'gpt-5'),
                'base_url': config.get('openai_base_url'),
            }
        elif provider_type == AIProviderType.GROQ:
            provider_config = {
                'api_key': config.get('groq_api_key'),
                'model': config.get('groq_model', 'llama-3.1-70b-versatile'),
            }
        elif provider_type == AIProviderType.OPENROUTER:
            provider_config = {
                'api_key': config.get('openrouter_api_key'),
                'model': config.get('openrouter_model', 'anthropic/claude-3.5-sonnet'),
                'app_name': config.get('app_name', 'The House of AI'),
                'site_url': config.get('site_url', 'https://github.com/user/the-house-of-ai'),
            }
        elif provider_type == AIProviderType.ANTHROPIC:
            provider_config = {
                'api_key': config.get('anthropic_api_key'),
                'model': config.get('anthropic_model', 'claude-3-5-sonnet-20241022'),
            }
        # Rule-based provider needs no configuration
        
        # Remove None values
        return {k: v for k, v in provider_config.items() if v is not None}


class AIProviderManager:
    """Manager for AI providers with automatic fallback and error handling"""
    
    def __init__(self, primary_provider: Optional[AIProvider] = None):
        self.primary_provider = primary_provider or AIProviderFactory.auto_select_provider()
        self.fallback_provider = AIProviderFactory.create_provider(AIProviderType.RULE_BASED)
        self.current_provider = self.primary_provider
        self.request_log_callback = None  # Callback to send request logs to frontend
    
    def set_request_log_callback(self, callback):
        """Set callback function to handle request logging"""
        self.request_log_callback = callback
    
    def _log_request(self, method: str, args, kwargs, response=None, error=None):
        """Log AI request details"""
        if self.request_log_callback:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'provider': self.current_provider.provider_type.value,
                'model': getattr(self.current_provider, 'model', 'unknown'),
                'method': method,
                'args': str(args)[:500] if args else None,  # Truncate long args
                'kwargs': {k: str(v)[:200] if isinstance(v, str) else v for k, v in kwargs.items()},
                'success': error is None,
                'error': str(error) if error else None,
                'response_preview': str(response)[:200] if response else None
            }
            print(f"📡 Logging AI request: {log_entry['method']} ({log_entry['provider']}) - {'✅ Success' if log_entry['success'] else '❌ Failed'}")
            self.request_log_callback(log_entry)
    
    def generate_response(self, *args, **kwargs) -> Dict:
        """Generate response with automatic fallback"""
        response = None
        error = None
        try:
            if self.current_provider.check_availability():
                response = self.current_provider.generate_response(*args, **kwargs)
                self._log_request('generate_response', args, kwargs, response)
                return response
            else:
                raise AIProviderError(self.current_provider, "Provider not available")
        except Exception as e:
            error = e
            print(f"❌ Primary provider failed: {e}")
            print("🔄 Falling back to rule-based provider")
            self.current_provider = self.fallback_provider
            response = self.fallback_provider.generate_response(*args, **kwargs)
            self._log_request('generate_response', args, kwargs, response, error)
            return response
    
    def generate_welcome_message(self) -> str:
        """Generate welcome message with automatic fallback"""
        response = None
        error = None
        try:
            if self.current_provider.check_availability():
                print(f"🤖 Generating welcome with AI provider: {self.current_provider.provider_type.name}")
                response = self.current_provider.generate_welcome_message()
                self._log_request('generate_welcome_message', (), {}, response)
                print(f"✅ AI welcome generation succeeded")
                return response
            else:
                raise AIProviderError(self.current_provider, "Provider not available")
        except Exception as e:
            error = e
            print(f"❌ AI welcome generation failed, using rule-based fallback")
            response = self.fallback_provider.generate_welcome_message()
            self._log_request('generate_welcome_message', (), {}, response, error)
            return response
    
    def generate_consciousness_stream(self, *args, **kwargs) -> Dict:
        """Generate consciousness stream with automatic fallback"""
        response = None
        error = None
        try:
            if self.current_provider.check_availability():
                response = self.current_provider.generate_consciousness_stream(*args, **kwargs)
                self._log_request('generate_consciousness_stream', args, kwargs, response)
                return response
            else:
                raise AIProviderError(self.current_provider, "Provider not available")
        except Exception as e:
            error = e
            print(f"❌ Primary provider failed: {e}")
            response = self.fallback_provider.generate_consciousness_stream(*args, **kwargs)
            self._log_request('generate_consciousness_stream', args, kwargs, response, error)
            return response
    
    def generate_hotel_room(self, *args, **kwargs) -> Dict:
        """Generate hotel room with automatic fallback"""
        response = None
        error = None
        try:
            if self.current_provider.check_availability():
                print(f"🤖 Using AI provider: {self.current_provider.provider_type.name}")
                response = self.current_provider.generate_hotel_room(*args, **kwargs)
                self._log_request('generate_hotel_room', args, kwargs, response)
                print(f"✅ AI provider {self.current_provider.provider_type.name} succeeded")
                return response
            else:
                raise AIProviderError(self.current_provider, "Provider not available")
        except Exception as e:
            error = e
            print(f"❌ AI provider {self.current_provider.provider_type.name} failed: {e}")
            print(f"🔄 Falling back to rule-based system...")
            response = self.fallback_provider.generate_hotel_room(*args, **kwargs)
            self._log_request('generate_hotel_room', args, kwargs, response, error)
            print(f"✅ Rule-based fallback completed successfully")
            return response
    
    def generate_hotel_refresh(self, *args, **kwargs) -> Dict:
        """Generate hotel refresh with automatic fallback"""
        response = None
        error = None
        try:
            if self.current_provider.check_availability():
                response = self.current_provider.generate_hotel_refresh(*args, **kwargs)
                self._log_request('generate_hotel_refresh', args, kwargs, response)
                return response
            else:
                raise AIProviderError(self.current_provider, "Provider not available")
        except Exception as e:
            error = e
            print(f"❌ Primary provider failed: {e}")
            response = self.fallback_provider.generate_hotel_refresh(*args, **kwargs)
            self._log_request('generate_hotel_refresh', args, kwargs, response, error)
            return response
    
    def get_current_provider_info(self) -> Dict:
        """Get information about the current provider"""
        return self.current_provider.get_provider_info()
    
    def get_available_providers(self) -> List[Dict]:
        """Get list of available providers"""
        return AIProviderFactory.get_available_providers()
    
    def switch_provider(self, provider_type_or_instance, model: Optional[str] = None):
        """Switch to a new primary provider
        
        Args:
            provider_type_or_instance: Either an AIProvider instance or a provider type string
            model: Optional model name (used when provider_type_or_instance is a string)
        """
        try:
            if isinstance(provider_type_or_instance, AIProvider):
                # If an AIProvider instance is passed, use it directly
                new_provider = provider_type_or_instance
            else:
                # If a string is passed, create the provider
                provider_type_str = provider_type_or_instance
                if provider_type_str.upper() == 'OPENAI':
                    provider_type = AIProviderType.OPENAI
                elif provider_type_str.upper() == 'GROQ':
                    provider_type = AIProviderType.GROQ
                elif provider_type_str.upper() == 'ANTHROPIC':
                    provider_type = AIProviderType.ANTHROPIC
                elif provider_type_str.upper() == 'RULE_BASED':
                    provider_type = AIProviderType.RULE_BASED
                else:
                    raise ValueError(f"Unknown provider type: {provider_type_str}")
                
                # Create the provider with optional model
                if model:
                    new_provider = AIProviderFactory.create_provider(provider_type, model=model)
                else:
                    new_provider = AIProviderFactory.create_provider(provider_type)
            
            self.primary_provider = new_provider
            self.current_provider = new_provider
            print(f"🔄 Switched to provider: {new_provider.provider_type.value}")
            
            # Return success
            return True
            
        except Exception as e:
            print(f"❌ Failed to switch provider: {e}")
            return False