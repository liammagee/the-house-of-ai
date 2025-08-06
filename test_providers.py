#!/usr/bin/env python3
"""
Test script for AI providers
Run this to test your AI provider configuration and debug connection issues
"""

import os
from dotenv import load_dotenv
from ai_providers import AIProviderFactory, AIProviderType

# Load environment variables
load_dotenv()

def test_provider(provider_type: AIProviderType):
    """Test a specific AI provider"""
    print(f"\n{'='*50}")
    print(f"Testing {provider_type.value.upper()} Provider")
    print(f"{'='*50}")
    
    try:
        # Get configuration for this provider
        config = AIProviderFactory.get_config_from_env()
        provider_config = AIProviderFactory._extract_provider_config(config, provider_type)
        
        print(f"Configuration found:")
        for key, value in provider_config.items():
            if 'api_key' in key.lower() and value:
                print(f"  {key}: {value[:10]}...{value[-4:] if len(value) > 14 else value}")
            else:
                print(f"  {key}: {value}")
        
        # Create provider
        provider = AIProviderFactory.create_provider(provider_type, **provider_config)
        
        if provider.check_availability():
            print(f"✅ Provider {provider_type.value} is available")
            
            # Test basic functionality
            print("🧪 Testing welcome message generation...")
            try:
                welcome = provider.generate_welcome_message()
                print(f"✅ Welcome message: {welcome[:100]}...")
            except Exception as e:
                print(f"❌ Welcome message failed: {e}")
            
            # Test consciousness stream
            print("🧪 Testing consciousness stream generation...")
            try:
                stream = provider.generate_consciousness_stream("Test context", {"id": "TEST_ROOM"})
                print(f"✅ Consciousness stream: {stream.get('message', '')[:100]}...")
            except Exception as e:
                print(f"❌ Consciousness stream failed: {e}")
            
            # Test hotel room generation
            print("🧪 Testing hotel room generation...")
            try:
                room = provider.generate_hotel_room(1)
                if room:
                    print(f"✅ Hotel room generated: {room.get('id', 'Unknown ID')}")
                else:
                    print("❌ Hotel room generation returned empty")
            except Exception as e:
                print(f"❌ Hotel room generation failed: {e}")
                
        else:
            print(f"❌ Provider {provider_type.value} is not available")
            
    except Exception as e:
        print(f"❌ Failed to create {provider_type.value} provider: {e}")

def main():
    print("🏠 The House of AI - Provider Test Suite")
    print("Testing all configured AI providers...\n")
    
    # Check environment variables
    print("Environment Variables:")
    ai_provider = os.getenv('AI_PROVIDER', 'not_set')
    print(f"  AI_PROVIDER: {ai_provider}")
    
    providers_to_test = [
        AIProviderType.OPENAI,
        AIProviderType.ANTHROPIC, 
        AIProviderType.GROQ,
        AIProviderType.OPENROUTER,
        AIProviderType.RULE_BASED
    ]
    
    # Test each provider
    for provider_type in providers_to_test:
        test_provider(provider_type)
    
    print(f"\n{'='*50}")
    print("Testing Auto-Selection")
    print(f"{'='*50}")
    
    try:
        auto_provider = AIProviderFactory.auto_select_provider()
        print(f"✅ Auto-selected provider: {auto_provider.provider_type.value}")
        
        # Test the auto-selected provider
        try:
            welcome = auto_provider.generate_welcome_message()
            print(f"✅ Auto-selected provider works: {welcome[:50]}...")
        except Exception as e:
            print(f"❌ Auto-selected provider failed: {e}")
            
    except Exception as e:
        print(f"❌ Auto-selection failed: {e}")
    
    print(f"\n{'='*50}")
    print("Test Complete")
    print(f"{'='*50}")
    print("If you see connection errors:")
    print("1. Check your API keys are valid and not expired")
    print("2. Verify you have internet connectivity") 
    print("3. Try setting AI_PROVIDER=rule_based for offline mode")
    print("4. Check the model names are correct for each provider")

if __name__ == "__main__":
    main()