#!/usr/bin/env python3
"""
Simple OpenAI API Test Script
Tests the OpenAI API with the current configuration
"""

import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openai_api():
    """Test OpenAI API with current configuration"""
    
    try:
        from openai import OpenAI
        
        # Get configuration from environment
        api_key = os.getenv('OPENAI_API_KEY')
        model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        
        print("=" * 50)
        print("OPENAI API TEST")
        print("=" * 50)
        print(f"API Key: {api_key[:15]}...{api_key[-4:] if len(api_key) > 19 else '***'}")
        print(f"Model: {model}")
        print(f"Timeout: 30 seconds")
        
        # Create client with reasonable timeout
        client = OpenAI(api_key=api_key, timeout=30.0)
        
        # Test 1: Simple request
        print("\n--- Test 1: Simple Hello Request ---")
        start_time = time.time()
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Say hello briefly"}
            ],
            max_tokens=20,
            temperature=0.1
        )
        
        duration = time.time() - start_time
        print(f"✅ SUCCESS in {duration:.2f}s")
        print(f"Response: {response.choices[0].message.content}")
        print(f"Tokens used: {response.usage.total_tokens}")
        
        # Test 2: Hotel room generation (like the app does)
        print("\n--- Test 2: Hotel Room Generation ---")
        room_prompt = """Generate a simple hotel room in JSON format:
{
    "id": "ROOM_001",
    "location": "City, Country",
    "time": "HH:MM",
    "consciousness": "A brief description..."
}"""
        
        start_time = time.time()
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a creative generator. Always respond with valid JSON only."},
                {"role": "user", "content": room_prompt}
            ],
            max_tokens=200,
            temperature=0.8
        )
        
        duration = time.time() - start_time
        print(f"✅ SUCCESS in {duration:.2f}s")
        print(f"Response: {response.choices[0].message.content[:200]}...")
        print(f"Tokens used: {response.usage.total_tokens}")
        
        print("\n" + "=" * 50)
        print("ALL TESTS PASSED! OpenAI API is working correctly.")
        print("The issue was likely the 5-second timeout being too short.")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print(f"Error type: {type(e).__name__}")
        
        if "timeout" in str(e).lower():
            print("➤ The request timed out. Try increasing the timeout.")
        elif "authentication" in str(e).lower():
            print("➤ Check your API key in the .env file.")
        elif "not found" in str(e).lower():
            print("➤ The model might not be available with your API key.")
        else:
            print(f"➤ Full error: {str(e)}")
        
        return False
        
    return True

if __name__ == "__main__":
    test_openai_api()