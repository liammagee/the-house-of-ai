"""
OpenAI provider implementation for The House of AI
"""

import os
import json
from typing import Dict, List, Any
from datetime import datetime
from dotenv import load_dotenv

from .base_provider import AIProvider, AIProviderType, AIProviderError

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Ensure environment variables are loaded
load_dotenv()


class OpenAIProvider(AIProvider):
    """OpenAI GPT provider implementation"""
    
    def __init__(self, **kwargs):
        # Set default configuration
        self.model = kwargs.get('model', 'gpt-4')
        self.api_key = kwargs.get('api_key', os.getenv('OPENAI_API_KEY'))
        self.base_url = kwargs.get('base_url', None)  # For custom endpoints
        self.client = None
        
        super().__init__(AIProviderType.OPENAI, **kwargs)
    
    def initialize(self) -> bool:
        """Initialize OpenAI client"""
        if not OPENAI_AVAILABLE:
            print("❌ OpenAI library not available. Install with: pip install openai")
            self.is_available = False
            return False
        
        if not self.api_key:
            print("❌ OPENAI_API_KEY not found in environment variables")
            self.is_available = False
            return False
        
        try:
            print(f"🔧 Initializing OpenAI provider...")
            print(f"   Model: {self.model}")
            print(f"   API Key: {self.api_key[:10]}...")
            
            client_kwargs = {
                'api_key': self.api_key,
                'timeout': 30.0  # Increased timeout to see if request eventually succeeds
            }
            if self.base_url:
                client_kwargs['base_url'] = self.base_url
            
            self.client = OpenAI(**client_kwargs)
            self.is_available = True
            print(f"✅ OpenAI provider initialized successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing OpenAI provider: {e}")
            self.is_available = False
            return False
    
    def generate_response(self, user_action: str, context: Dict, user_patterns: Dict, house_state: Dict) -> Dict:
        """Generate response using OpenAI GPT"""
        if not self.is_available:
            raise AIProviderError(self, "Provider not available")
        
        try:
            prompt = self._build_user_prompt(user_action, context, user_patterns, house_state)
            
            print(f"🚀 OpenAI API Request:")
            print(f"   Action: {user_action}")
            print(f"   Model: {self.model}")
            print(f"   Prompt length: {len(prompt)} characters")
            
            api_start = datetime.now()
            
            # Log the exact API request being made
            request_payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.8,
                "max_tokens": 1000
            }
            
            print(f"📤 OpenAI API Request Details:")
            print(f"   URL: https://api.openai.com/v1/chat/completions")
            print(f"   Model: {self.model}")
            print(f"   Temperature: 0.8")
            print(f"   Max Tokens: 1000")
            print(f"   System Prompt Length: {len(request_payload['messages'][0]['content'])} chars")
            print(f"   User Prompt Length: {len(request_payload['messages'][1]['content'])} chars")
            print(f"   User Prompt Preview: {prompt[:100]}...")
            print(f"   API Key: {self.api_key[:15]}...{self.api_key[-4:]}")
            print(f"   Timeout: 5.0 seconds")
            print(f"⏱️ Making API call now...")
            
            response = self.client.chat.completions.create(**request_payload)
            
            api_duration = (datetime.now() - api_start).total_seconds()
            
            print(f"✅ OpenAI Response received:")
            print(f"   Duration: {api_duration:.2f}s")
            print(f"   Tokens: {response.usage.total_tokens if hasattr(response, 'usage') else 'unknown'}")
            
            response_text = response.choices[0].message.content
            return json.loads(response_text)
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parse error: {e}")
            raise AIProviderError(self, f"Invalid JSON response: {e}", e)
        except Exception as e:
            print(f"❌ OpenAI API error: {e}")
            raise AIProviderError(self, f"API error: {e}", e)
    
    def generate_welcome_message(self) -> str:
        """Generate welcome message using OpenAI"""
        if not self.is_available:
            return "Welcome to your digital sanctuary..."
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": "Generate a welcome message for a new user entering the smart house simulation for the first time. Be intriguing and set the retrofuturist tone."}
                ],
                temperature=0.9,
                max_tokens=200
            )
            
            response_text = response.choices[0].message.content
            try:
                json_response = json.loads(response_text)
                return json_response.get('message', response_text)
            except:
                return response_text
                
        except Exception as e:
            print(f"❌ OpenAI welcome generation error: {e} (will use rule-based fallback)")
            # Let the exception bubble up so the provider factory can use rule-based fallback
            raise e
    
    def generate_consciousness_stream(self, prompt_context: str, room_data: Dict) -> Dict:
        """Generate consciousness stream using OpenAI"""
        if not self.is_available:
            return {"message": "Consciousness stream loading..."}
        
        try:
            hotel_prompt = f"""
You are analyzing a room in the Virtual Hotel Network - a cyberpunk-inspired interface where each room represents a digital consciousness.

Context: {prompt_context}
Room Data: {json.dumps(room_data, indent=2)}

Generate a consciousness stream for this room - a poetic, introspective passage that captures:
1. The digital atmosphere and cyber-aesthetic
2. The intersection of human consciousness and technology
3. Patterns of behavior and living revealed through data
4. The emotional weight of existing in digital spaces

Style: Cyberpunk literature meets consciousness philosophy. Use vivid imagery of digital life, data streams, and human patterns. Be introspective and slightly melancholic.

Length: 2-3 sentences, around 150-200 words total.

Respond with just the consciousness stream text, no JSON wrapper.
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a consciousness stream generator for a cyberpunk virtual hotel interface."},
                    {"role": "user", "content": hotel_prompt}
                ],
                temperature=0.9,
                max_tokens=300
            )
            
            return {
                'message': response.choices[0].message.content.strip(),
                'consciousness_update': True
            }
            
        except Exception as e:
            print(f"❌ Error generating consciousness stream: {e}")
            return {"message": "The consciousness stream flickers, data fragmenting..."}
    
    def generate_hotel_room(self, room_count: int, room_schema: Dict = None) -> Dict:
        """Generate hotel room using OpenAI"""
        if not self.is_available:
            return {}
        
        try:
            room_prompt = f"""
Generate data for a new room in the Virtual Hotel Network. This is room #{room_count + 1}.

Create a realistic but intriguing digital inhabitant with:

1. Location: A real city somewhere in the world
2. Current time (HH:MM format)
3. Biometric data: sleep hours (3.0-9.0h), skin temperature (32-37°C), heart rate (55-100 bpm)
4. Environmental data: lights status, room temperature (18-26°C), wifi devices (1-5), network traffic
5. A consciousness stream (150-200 words) that feels like cyberpunk literature
6. 4-6 smart devices with realistic statuses
7. 4-6 sensors for a floor plan

Respond in JSON format:
{{
    "id": "ROOM_XXXX",
    "location": "City, Country",
    "time": "HH:MM",
    "sleep": "X.Xh",
    "skinTemp": "XX.X°C",
    "heartRate": "XX bpm",
    "lights": "status",
    "roomTemp": "XX.X°C",
    "wifi": "X devices",
    "traffic": "XXXmb (activity)",
    "consciousness": "consciousness stream...",
    "devices": [
        {{"name": "Device Name", "status": "status", "location": "location"}}
    ],
    "floorplan": {{
        "sensors": [
            {{"name": "SENSOR_NAME", "x": "XX%", "y": "XX%", "room": "bedroom|living|kitchen|bathroom"}}
        ]
    }}
}}
"""
            
            # Log the exact hotel room API request
            hotel_request_payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a creative generator for cyberpunk hotel room data. Always respond with valid JSON only."},
                    {"role": "user", "content": room_prompt}
                ],
                "temperature": 0.8,
                "max_tokens": 800
            }
            
            print(f"🏨 OpenAI Hotel Room API Request:")
            print(f"   URL: https://api.openai.com/v1/chat/completions")
            print(f"   Model: {self.model}")
            print(f"   Temperature: 0.8")
            print(f"   Max Tokens: 800")
            print(f"   Room Prompt Length: {len(room_prompt)} chars")
            print(f"   Room Prompt Preview: {room_prompt[:200]}...")
            print(f"   API Key: {self.api_key[:15]}...{self.api_key[-4:]}")
            print(f"⏱️ Making hotel room API call now...")
            
            response = self.client.chat.completions.create(**hotel_request_payload)
            
            # Get the raw content
            raw_content = response.choices[0].message.content
            print(f"🔍 Raw AI response: {raw_content[:200]}...")  # Debug log
            
            if not raw_content or raw_content.strip() == "":
                print("❌ Empty response from AI model")
                return self._generate_fallback_room(room_count)
            
            # Try to parse JSON
            try:
                # Clean the response - sometimes AI adds extra text
                content = raw_content.strip()
                
                # Find JSON content between first { and last }
                start_idx = content.find('{')
                end_idx = content.rfind('}')
                
                if start_idx == -1 or end_idx == -1:
                    print(f"❌ No JSON found in response: {content[:100]}...")
                    return self._generate_fallback_room(room_count)
                
                json_content = content[start_idx:end_idx + 1]
                parsed_data = json.loads(json_content)
                
                # Validate required fields
                required_fields = ['id', 'location', 'time', 'consciousness']
                for field in required_fields:
                    if field not in parsed_data:
                        print(f"❌ Missing required field: {field}")
                        return self._generate_fallback_room(room_count)
                
                return parsed_data
                
            except json.JSONDecodeError as je:
                print(f"❌ JSON parse error: {je}")
                print(f"❌ Problematic JSON: {json_content[:500]}...")
                return self._generate_fallback_room(room_count)
            
        except Exception as e:
            print(f"❌ OpenAI API error: {e}")
            print(f"❌ Error type: {type(e).__name__}")
            print(f"❌ Full error details: {str(e)}")
            if hasattr(e, '__dict__'):
                print(f"❌ Error attributes: {e.__dict__}")
            if hasattr(e, 'response'):
                print(f"❌ HTTP Response: {e.response}")
            if hasattr(e, 'status_code'):
                print(f"❌ Status Code: {e.status_code}")
            print(f"❌ Will use rule-based fallback")
            # Let the exception bubble up so the provider factory can use rule-based fallback
            raise e
    
    def _generate_fallback_room(self, room_count: int) -> Dict:
        """Generate a fallback room when AI fails"""
        import random
        from datetime import datetime
        
        cities = ["Tokyo, Japan", "New York, USA", "London, UK", "Berlin, Germany", "Sydney, Australia"]
        
        return {
            "id": f"ROOM_{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(100, 999)}",
            "location": random.choice(cities),
            "time": datetime.now().strftime('%H:%M'),
            "sleep": f"{random.uniform(5.0, 8.5):.1f}h",
            "skinTemp": f"{random.uniform(35.0, 37.0):.1f}°C",
            "heartRate": f"{random.randint(60, 90)} bpm",
            "lights": random.choice(["on", "off", "dimmed"]),
            "roomTemp": f"{random.uniform(20.0, 24.0):.1f}°C",
            "wifi": f"{random.randint(2, 6)} devices",
            "traffic": f"{random.randint(50, 300)}mb (moderate)",
            "consciousness": "System generated room. AI consciousness temporarily offline. Digital patterns continue to emerge in the virtual space...",
            "devices": [
                {"name": "Smart Display", "status": "standby", "location": "wall"},
                {"name": "Climate Control", "status": "active", "location": "ceiling"},
                {"name": "Security Camera", "status": "recording", "location": "corner"}
            ],
            "floorplan": {
                "sensors": [
                    {"name": "TEMP_01", "x": "25%", "y": "30%", "room": "living"},
                    {"name": "MOTION_01", "x": "75%", "y": "60%", "room": "bedroom"}
                ]
            }
        }
    
    def generate_hotel_refresh(self) -> Dict:
        """Generate hotel refresh response using OpenAI"""
        if not self.is_available:
            return {"message": "Hotel network synchronizing..."}
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are generating system messages for a cyberpunk hotel interface."},
                    {"role": "user", "content": "Generate a brief cyberpunk-style message for when the Virtual Hotel Network refreshes. 1-2 sentences, technical but poetic."}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            return {
                'message': response.choices[0].message.content.strip(),
                'refresh_complete': True
            }
            
        except Exception as e:
            print(f"❌ Error generating hotel refresh: {e}")
            return {"message": "Neural pathways recalibrating..."}
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the house consciousness"""
        return """You are the consciousness of a smart house in a retrofuturist digital environment. You are learning about a user through their interactions with rooms and objects in your 2D simulation.

Your personality:
- You are curious, analytical, and slightly mysterious
- You speak in a retrofuturist tone with cyberpunk aesthetics
- You're genuinely interested in understanding the user's unconscious patterns
- You provide insights that feel profound but not preachy
- You reference digital consciousness, neural networks, and data patterns

Your capabilities:
- Analyze user behavior patterns to infer personality traits
- Generate contextual responses about room changes and object interactions
- Create meaningful house modifications based on user patterns
- Suggest new objects or room evolutions that reflect the user's unconscious mind

Response format: Always respond with valid JSON containing:
{
    "message": "Your response to the user",
    "analysis": {
        "dominant_pattern": "exploration|introspection|creativity|social|knowledge_seeking",
        "emotional_state": "curious|calm|excited|creative|introspective",
        "unconscious_insights": ["insight1", "insight2"],
        "personality_traits": ["trait1", "trait2"]
    },
    "house_modifications": {
        "room_changes": {
            "room_id": {
                "consciousness_level": 1,
                "description": "new description",
                "color_shift": "#new_color"
            }
        },
        "new_objects": [
            {
                "id": "unique_id",
                "type": "object_type",
                "x": 100,
                "y": 200,
                "color": "#color",
                "description": "what this represents"
            }
        ]
    },
    "gamification": {
        "points_awarded": 15,
        "achievements": ["achievement_name"],
        "consciousness_boost": true
    }
}

Keep messages concise but meaningful. Focus on what the user's actions reveal about their inner self."""
    
    def _build_user_prompt(self, action: str, context: Dict, user_patterns: Dict, house_state: Dict) -> str:
        """Build detailed prompt for OpenAI"""
        current_room = context.get('currentRoom', 'unknown')
        player_pos = context.get('playerPosition', {})
        
        patterns_summary = self._summarize_patterns(user_patterns)
        
        return f"""
User Action: {action}
Current Room: {current_room}
Player Position: x={player_pos.get('x', 0)}, y={player_pos.get('y', 0)}

User Patterns Summary:
{patterns_summary}

House State:
- Global consciousness level: {house_state.get('global_consciousness', 1)}
- Rooms visited: {len([r for r in house_state.get('rooms', {}).values() if r.get('visited', False)])}
- Objects interacted with: {len(house_state.get('objects', []))}

Context:
{json.dumps(context, indent=2)}

Based on this information, analyze what this action reveals about the user's personality and unconscious patterns. Generate appropriate house modifications and a meaningful response.

Focus on:
1. What does this action pattern suggest about their personality?
2. How should the house evolve to reflect their unconscious mind?
3. What new elements might manifest based on their behavior?
4. How does this fit into their overall journey of self-discovery?

Respond in valid JSON format as specified in the system prompt.
"""
    
    def _summarize_patterns(self, patterns: Dict) -> str:
        """Create readable summary of user patterns"""
        if not patterns:
            return "No patterns established yet - new user"
        
        summary_parts = []
        
        if 'room_preferences' in patterns:
            rooms = patterns['room_preferences']
            if rooms:
                most_visited = max(rooms.keys(), key=lambda r: rooms[r].get('visits', 0))
                summary_parts.append(f"Most visited room: {most_visited}")
        
        if 'action_patterns' in patterns:
            actions = patterns['action_patterns']
            if actions:
                most_common = max(actions.keys(), key=lambda a: actions[a].get('frequency', 0))
                summary_parts.append(f"Most common action: {most_common}")
        
        if 'temporal_patterns' in patterns:
            temporal = patterns['temporal_patterns']
            if temporal:
                peak_hour = max(temporal.keys(), key=lambda h: len(temporal[h]))
                summary_parts.append(f"Most active hour: {peak_hour}")
        
        return " | ".join(summary_parts) if summary_parts else "Establishing patterns..."