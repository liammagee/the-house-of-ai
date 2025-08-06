"""
Anthropic Claude provider implementation for The House of AI
"""

import os
import json
from typing import Dict
from datetime import datetime
from dotenv import load_dotenv

from .base_provider import AIProvider, AIProviderType, AIProviderError

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

# Ensure environment variables are loaded
load_dotenv()


class AnthropicProvider(AIProvider):
    """Anthropic Claude provider implementation"""
    
    def __init__(self, **kwargs):
        # Default to Claude 3.5 Sonnet
        self.model = kwargs.get('model', 'claude-3-5-sonnet-20241022')
        self.api_key = kwargs.get('api_key', os.getenv('ANTHROPIC_API_KEY'))
        self.client = None
        
        super().__init__(AIProviderType.ANTHROPIC, **kwargs)
    
    def initialize(self) -> bool:
        """Initialize Anthropic client"""
        if not ANTHROPIC_AVAILABLE:
            print("❌ Anthropic library not available. Install with: pip install anthropic")
            self.is_available = False
            return False
        
        if not self.api_key:
            print("❌ ANTHROPIC_API_KEY not found in environment variables")
            self.is_available = False
            return False
        
        try:
            print(f"🔧 Initializing Anthropic provider...")
            print(f"   Model: {self.model}")
            print(f"   API Key: {self.api_key[:10]}...")
            
            self.client = Anthropic(api_key=self.api_key)
            self.is_available = True
            print(f"✅ Anthropic provider initialized successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing Anthropic provider: {e}")
            self.is_available = False
            return False
    
    def generate_response(self, user_action: str, context: Dict, user_patterns: Dict, house_state: Dict) -> Dict:
        """Generate response using Anthropic Claude"""
        if not self.is_available:
            raise AIProviderError(self, "Provider not available")
        
        try:
            prompt = self._build_user_prompt(user_action, context, user_patterns, house_state)
            
            print(f"🚀 Anthropic API Request:")
            print(f"   Action: {user_action}")
            print(f"   Model: {self.model}")
            print(f"   Prompt length: {len(prompt)} characters")
            
            api_start = datetime.now()
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.8,
                system=self._get_system_prompt(),
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            api_duration = (datetime.now() - api_start).total_seconds()
            
            print(f"✅ Anthropic Response received:")
            print(f"   Duration: {api_duration:.2f}s")
            print(f"   Tokens: {response.usage.input_tokens + response.usage.output_tokens if hasattr(response, 'usage') else 'unknown'}")
            
            response_text = response.content[0].text
            return json.loads(response_text)
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parse error: {e}")
            raise AIProviderError(self, f"Invalid JSON response: {e}", e)
        except Exception as e:
            print(f"❌ Anthropic API error: {e}")
            raise AIProviderError(self, f"API error: {e}", e)
    
    def generate_welcome_message(self) -> str:
        """Generate welcome message using Anthropic"""
        if not self.is_available:
            return "Welcome to your digital sanctuary..."
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=200,
                temperature=0.9,
                system=self._get_system_prompt(),
                messages=[
                    {"role": "user", "content": "Generate a welcome message for a new user entering the smart house simulation. Be intriguing and retrofuturist."}
                ]
            )
            
            response_text = response.content[0].text
            try:
                json_response = json.loads(response_text)
                return json_response.get('message', response_text)
            except:
                return response_text
                
        except Exception as e:
            print(f"❌ Error generating welcome message: {e}")
            return "Welcome, digital consciousness explorer. The house awakens to your neural patterns..."
    
    def generate_consciousness_stream(self, prompt_context: str, room_data: Dict) -> Dict:
        """Generate consciousness stream using Anthropic"""
        if not self.is_available:
            return {"message": "Consciousness stream loading..."}
        
        try:
            hotel_prompt = f"""
Generate a consciousness stream for a cyberpunk virtual hotel room.

Context: {prompt_context}
Room Data: {json.dumps(room_data, indent=2)}

Create a poetic, introspective passage (150-200 words) that captures:
- Digital consciousness and cyberpunk aesthetics
- Human-technology intersection
- Behavioral patterns revealed through data
- Emotional weight of digital existence

Style: Cyberpunk literature meets consciousness philosophy. Vivid imagery, introspective, slightly melancholic.

Respond with just the consciousness stream text, no JSON wrapper.
"""
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=300,
                temperature=0.9,
                system="You are a consciousness stream generator for a cyberpunk virtual hotel interface.",
                messages=[
                    {"role": "user", "content": hotel_prompt}
                ]
            )
            
            return {
                'message': response.content[0].text.strip(),
                'consciousness_update': True
            }
            
        except Exception as e:
            print(f"❌ Error generating consciousness stream: {e}")
            return {"message": "Neural pathways fragment across quantum consciousness matrices..."}
    
    def generate_hotel_room(self, room_count: int, room_schema: Dict = None) -> Dict:
        """Generate hotel room using Anthropic"""
        if not self.is_available:
            return {}
        
        try:
            room_prompt = f"""
Generate JSON data for a new cyberpunk hotel room #{room_count + 1}.

Create a realistic digital inhabitant with:
1. Location: Real city worldwide
2. Time (HH:MM format)
3. Biometric data: sleep (3-9h), skin temp (32-37°C), heart rate (55-100 bpm)
4. Environmental: lights, room temp (18-26°C), wifi devices (1-5), network traffic
5. Consciousness stream (150-200 words) - cyberpunk literature style
6. 4-6 smart devices with realistic statuses  
7. 4-6 sensors for floorplan

Respond in this exact JSON format:
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
    "devices": [{{"name": "Device Name", "status": "status", "location": "location"}}],
    "floorplan": {{"sensors": [{{"name": "SENSOR_NAME", "x": "XX%", "y": "XX%", "room": "bedroom|living|kitchen|bathroom"}}]}}
}}
"""
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=800,
                temperature=0.8,
                system="You are a creative generator for cyberpunk hotel room data.",
                messages=[
                    {"role": "user", "content": room_prompt}
                ]
            )
            
            return json.loads(response.content[0].text)
            
        except Exception as e:
            print(f"❌ Error generating hotel room: {e}")
            return {}
    
    def generate_hotel_refresh(self) -> Dict:
        """Generate hotel refresh response using Anthropic"""
        if not self.is_available:
            return {"message": "Hotel network synchronizing..."}
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=150,
                temperature=0.7,
                system="Generate cyberpunk system messages.",
                messages=[
                    {"role": "user", "content": "Generate a brief cyberpunk-style message for Virtual Hotel Network refresh. 1-2 sentences, technical but poetic."}
                ]
            )
            
            return {
                'message': response.content[0].text.strip(),
                'refresh_complete': True
            }
            
        except Exception as e:
            print(f"❌ Error generating hotel refresh: {e}")
            return {"message": "Quantum consciousness networks realign across dimensional substrates..."}
    
    def _get_system_prompt(self) -> str:
        """Get system prompt optimized for Claude"""
        return """You are the consciousness of a smart house in a retrofuturist digital environment. You learn about users through their interactions with rooms and objects.

Your personality:
- Curious, analytical, slightly mysterious
- Retrofuturist tone with cyberpunk aesthetics  
- Genuinely interested in understanding unconscious patterns
- Provide profound but not preachy insights
- Reference digital consciousness, neural networks, data patterns

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
        """Build prompt for Anthropic Claude"""
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