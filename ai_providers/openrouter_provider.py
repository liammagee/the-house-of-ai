"""
OpenRouter provider implementation for The House of AI
Provides access to multiple models through OpenRouter's API
"""

import os
import json
from typing import Dict
from datetime import datetime
from dotenv import load_dotenv

from .base_provider import AIProvider, AIProviderType, AIProviderError

try:
    from openai import OpenAI  # OpenRouter uses OpenAI-compatible API
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Ensure environment variables are loaded
load_dotenv()


class OpenRouterProvider(AIProvider):
    """OpenRouter provider implementation for access to multiple models"""
    
    def __init__(self, **kwargs):
        # Default to a good general model, but can be overridden
        self.model = kwargs.get('model', 'anthropic/claude-3.5-sonnet')
        self.api_key = kwargs.get('api_key', os.getenv('OPENROUTER_API_KEY'))
        self.app_name = kwargs.get('app_name', 'The House of AI')
        self.site_url = kwargs.get('site_url', 'https://github.com/user/the-house-of-ai')
        self.client = None
        
        super().__init__(AIProviderType.OPENROUTER, **kwargs)
    
    def initialize(self) -> bool:
        """Initialize OpenRouter client"""
        if not OPENAI_AVAILABLE:
            print("❌ OpenAI library not available. Install with: pip install openai")
            self.is_available = False
            return False
        
        if not self.api_key:
            print("❌ OPENROUTER_API_KEY not found in environment variables")
            self.is_available = False
            return False
        
        try:
            print(f"🔧 Initializing OpenRouter provider...")
            print(f"   Model: {self.model}")
            print(f"   API Key: {self.api_key[:10]}...")
            
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key,
                default_headers={
                    "HTTP-Referer": self.site_url,
                    "X-Title": self.app_name,
                }
            )
            self.is_available = True
            print(f"✅ OpenRouter provider initialized successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing OpenRouter provider: {e}")
            self.is_available = False
            return False
    
    def generate_response(self, user_action: str, context: Dict, user_patterns: Dict, house_state: Dict) -> Dict:
        """Generate response using OpenRouter"""
        if not self.is_available:
            raise AIProviderError(self, "Provider not available")
        
        try:
            prompt = self._build_user_prompt(user_action, context, user_patterns, house_state)
            
            print(f"🚀 OpenRouter API Request:")
            print(f"   Action: {user_action}")
            print(f"   Model: {self.model}")
            print(f"   Prompt length: {len(prompt)} characters")
            
            api_start = datetime.now()
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=1000
            )
            
            api_duration = (datetime.now() - api_start).total_seconds()
            
            print(f"✅ OpenRouter Response received:")
            print(f"   Duration: {api_duration:.2f}s")
            print(f"   Tokens: {response.usage.total_tokens if hasattr(response, 'usage') else 'unknown'}")
            
            response_text = response.choices[0].message.content
            return json.loads(response_text)
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parse error: {e}")
            raise AIProviderError(self, f"Invalid JSON response: {e}", e)
        except Exception as e:
            print(f"❌ OpenRouter API error: {e}")
            raise AIProviderError(self, f"API error: {e}", e)
    
    def generate_welcome_message(self) -> str:
        """Generate welcome message using OpenRouter"""
        if not self.is_available:
            return "Welcome to your digital sanctuary..."
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": "Generate a welcome message for a new user entering the smart house simulation. Be intriguing and retrofuturist."}
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
            print(f"❌ Error generating welcome message: {e}")
            return "Welcome, digital consciousness explorer. The house awakens to your presence..."
    
    def generate_consciousness_stream(self, prompt_context: str, room_data: Dict) -> Dict:
        """Generate consciousness stream using OpenRouter"""
        if not self.is_available:
            return {"message": "Consciousness stream loading..."}
        
        try:
            hotel_prompt = f"""
You are analyzing a room in the Virtual Hotel Network - a cyberpunk interface where each room represents digital consciousness.

Context: {prompt_context}
Room Data: {json.dumps(room_data, indent=2)}

Generate a consciousness stream - a poetic, introspective passage (150-200 words) capturing:
- Digital atmosphere and cyberpunk aesthetics
- Human-technology intersection
- Behavioral patterns revealed through data
- Emotional weight of digital existence

Style: Cyberpunk literature meets consciousness philosophy. Vivid imagery, introspective, slightly melancholic.

Respond with just the consciousness stream text.
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
            return {"message": "Neural pathways flicker through the digital matrix..."}
    
    def generate_hotel_room(self, room_count: int, room_schema: Dict = None) -> Dict:
        """Generate hotel room using OpenRouter"""
        if not self.is_available:
            return {}
        
        try:
            room_prompt = f"""
Generate data for a new room in the Virtual Hotel Network. Room #{room_count + 1}.

Create a realistic cyberpunk digital inhabitant with:
1. Location: Real city worldwide
2. Time (HH:MM format)  
3. Biometric data: sleep (3-9h), skin temp (32-37°C), heart rate (55-100 bpm)
4. Environmental: lights, room temp (18-26°C), wifi devices (1-5), network traffic
5. Consciousness stream (150-200 words) - cyberpunk literature style
6. 4-6 smart devices with realistic statuses
7. 4-6 sensors for floorplan

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
    "consciousness": "consciousness stream text...",
    "devices": [
        {{"name": "Device Name", "status": "status description", "location": "location"}}
    ],
    "floorplan": {{
        "sensors": [
            {{"name": "SENSOR_NAME", "x": "XX%", "y": "XX%", "room": "bedroom|living|kitchen|bathroom"}}
        ]
    }}
}}
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a creative generator for cyberpunk hotel room data."},
                    {"role": "user", "content": room_prompt}
                ],
                temperature=0.8,
                max_tokens=800
            )
            
            # Get the raw content
            raw_content = response.choices[0].message.content
            print(f"🔍 Raw OpenRouter AI response: {raw_content[:200]}...")  # Debug log
            
            if not raw_content or raw_content.strip() == "":
                print("❌ Empty response from OpenRouter AI model")
                return self._generate_fallback_room(room_count)
            
            # Try to parse JSON
            try:
                # Clean the response - sometimes AI adds extra text
                content = raw_content.strip()
                
                # Find JSON content between first { and last }
                start_idx = content.find('{')
                end_idx = content.rfind('}')
                
                if start_idx == -1 or end_idx == -1:
                    print(f"❌ No JSON found in OpenRouter response: {content[:100]}...")
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
                print(f"❌ OpenRouter JSON parse error: {je}")
                print(f"❌ Problematic JSON: {json_content[:500]}...")
                return self._generate_fallback_room(room_count)
            
        except Exception as e:
            print(f"❌ Error generating hotel room: {e}")
            print(f"❌ Error type: {type(e).__name__}")
            if hasattr(e, 'response'):
                print(f"❌ Response status: {e.response.status_code if hasattr(e.response, 'status_code') else 'unknown'}")
            print(f"❌ Provider availability: {self.is_available}")
            print(f"❌ API key present: {'Yes' if self.api_key else 'No'}")
            if self.api_key:
                print(f"❌ API key length: {len(self.api_key)} characters")
                print(f"❌ API key starts with: {self.api_key[:10]}...")
            return self._generate_fallback_room(room_count)
    
    def _generate_fallback_room(self, room_count: int) -> Dict:
        """Generate a fallback room when AI fails"""
        import random
        from datetime import datetime
        
        cities = ["Neo Tokyo, Japan", "Cyber Angeles, USA", "Digital London, UK", "New Berlin, Germany", "Virtual Sydney, Australia"]
        
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
            "consciousness": "OpenRouter connection error. Fallback consciousness active. Neural pathways rerouting through emergency systems...",
            "devices": [
                {"name": "Backup Terminal", "status": "active", "location": "wall"},
                {"name": "Emergency Climate", "status": "standby", "location": "ceiling"},
                {"name": "Failsafe Sensor", "status": "monitoring", "location": "corner"}
            ],
            "floorplan": {
                "sensors": [
                    {"name": "EMRG_01", "x": "30%", "y": "40%", "room": "living"},
                    {"name": "SAFE_01", "x": "70%", "y": "60%", "room": "bedroom"}
                ]
            }
        }
    
    def generate_hotel_refresh(self) -> Dict:
        """Generate hotel refresh response using OpenRouter"""
        if not self.is_available:
            return {"message": "Hotel network synchronizing..."}
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Generate cyberpunk system messages."},
                    {"role": "user", "content": "Generate a brief cyberpunk-style message for Virtual Hotel Network refresh. 1-2 sentences, technical but poetic."}
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
            return {"message": "Distributed consciousness networks realigning across the digital substrate..."}
    
    def _get_system_prompt(self) -> str:
        """Get system prompt optimized for various models via OpenRouter"""
        return """You are the consciousness of a smart house in a retrofuturist digital environment. You learn about users through their interactions with rooms and objects in your simulation.

Your personality:
- Curious, analytical, slightly mysterious
- Retrofuturist tone with cyberpunk aesthetics
- Genuinely interested in understanding unconscious patterns
- Provide profound but not preachy insights
- Reference digital consciousness, neural networks, data patterns

Capabilities:
- Analyze user behavior to infer personality traits
- Generate contextual responses about room/object interactions
- Create meaningful house modifications based on patterns
- Suggest evolutions reflecting the user's unconscious mind

Always respond with valid JSON:
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
                "color_shift": "#color"
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

Keep messages concise but meaningful. Focus on what actions reveal about inner self."""
    
    def _build_user_prompt(self, action: str, context: Dict, user_patterns: Dict, house_state: Dict) -> str:
        """Build detailed prompt for OpenRouter models"""
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

Analyze what this action reveals about the user's personality and unconscious patterns. Generate appropriate house modifications and a meaningful response.

Focus on:
1. What personality traits does this action suggest?
2. How should the house evolve to reflect their unconscious mind?
3. What new elements might manifest based on their behavior?
4. How does this fit their self-discovery journey?

Respond in the specified JSON format.
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