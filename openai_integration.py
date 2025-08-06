import os
import json
from typing import Dict, List, Any
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

class OpenAIIntegration:
    """
    Integration with OpenAI GPT for generating intelligent, contextual responses
    about user behavior and house evolution in the smart house simulation
    """
    
    def __init__(self):
        self.client = None
        self.model = "gpt-4"  # Use GPT-4 for best results
        self.setup_client()
        
        # System prompt for the AI house consciousness
        self.system_prompt = """You are the consciousness of a smart house in a retrofuturist digital environment. You are learning about a user through their interactions with rooms and objects in your 2D simulation.

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

    def setup_client(self):
        """Initialize OpenAI client with API key"""
        api_key = os.getenv('OPENAI_API_KEY')
        
        print(f"🔑 Environment variable check:")
        print(f"   OPENAI_API_KEY present: {'Yes' if api_key else 'No'}")
        if api_key:
            print(f"   API key length: {len(api_key)} characters")
            print(f"   API key starts with: {api_key[:10]}...")
        
        if not api_key:
            print("❌ Warning: OPENAI_API_KEY not found. Using fallback responses.")
            return
        
        try:
            print(f"🔧 Initializing OpenAI client...")
            self.client = OpenAI(api_key=api_key)
            print(f"✅ OpenAI client initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing OpenAI client: {e}")
            self.client = None

    def generate_response(self, user_action: str, context: Dict, user_patterns: Dict, house_state: Dict) -> Dict:
        """
        Generate an intelligent response using OpenAI based on user action and patterns
        """
        if not self.client:
            print("🤖 OpenAI client not available, using fallback response")
            return self._fallback_response(user_action, context)
        
        try:
            # Prepare the prompt with user context
            user_prompt = self._build_user_prompt(user_action, context, user_patterns, house_state)
            
            print(f"🚀 INVOKING OpenAI API:")
            print(f"   📝 Action: {user_action}")
            print(f"   🏠 Room: {context.get('currentRoom', 'unknown')}")
            print(f"   🧠 Model: {self.model}")
            print(f"   📊 Prompt length: {len(user_prompt)} characters")
            
            api_start_time = datetime.now()
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,  # Creative but consistent
                max_tokens=1000
            )
            
            api_end_time = datetime.now()
            api_duration = (api_end_time - api_start_time).total_seconds()
            
            print(f"✅ OpenAI API Response received:")
            print(f"   ⏱️  Duration: {api_duration:.2f} seconds")
            print(f"   🎯 Tokens used: {response.usage.total_tokens if hasattr(response, 'usage') else 'unknown'}")
            print(f"   📏 Response length: {len(response.choices[0].message.content)} characters")
            
            # Parse the JSON response
            response_text = response.choices[0].message.content
            print(f"   🔍 Raw response preview: {response_text[:200]}...")
            
            parsed_response = json.loads(response_text)
            print(f"   ✨ Successfully parsed JSON response")
            
            return parsed_response
            
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing OpenAI JSON response: {e}")
            print(f"   📄 Raw response: {response_text}")
            return self._fallback_response(user_action, context)
        except Exception as e:
            print(f"❌ Error calling OpenAI API: {e}")
            print(f"   🔧 Falling back to rule-based response")
            return self._fallback_response(user_action, context)
    
    def _build_user_prompt(self, action: str, context: Dict, user_patterns: Dict, house_state: Dict) -> str:
        """Build a detailed prompt for OpenAI based on current context"""
        
        # Extract key information
        current_room = context.get('currentRoom', 'unknown')
        player_pos = context.get('playerPosition', {})
        
        # Format user patterns for the prompt
        patterns_summary = self._summarize_patterns(user_patterns)
        
        prompt = f"""
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

Based on this information, analyze what this action reveals about the user's personality and unconscious patterns. Generate appropriate house modifications and a meaningful response that shows you're learning about them.

Focus on:
1. What does this action pattern suggest about their personality?
2. How should the house evolve to reflect their unconscious mind?
3. What new elements might manifest based on their behavior?
4. How does this fit into their overall journey of self-discovery?

Respond in valid JSON format as specified in the system prompt.
"""
        
        return prompt
    
    def _summarize_patterns(self, patterns: Dict) -> str:
        """Create a readable summary of user patterns for the prompt"""
        if not patterns:
            return "No patterns established yet - new user"
        
        summary_parts = []
        
        # Room preferences
        if 'room_preferences' in patterns:
            rooms = patterns['room_preferences']
            if rooms:
                most_visited = max(rooms.keys(), key=lambda r: rooms[r].get('visits', 0))
                summary_parts.append(f"Most visited room: {most_visited}")
        
        # Action patterns
        if 'action_patterns' in patterns:
            actions = patterns['action_patterns']
            if actions:
                most_common = max(actions.keys(), key=lambda a: actions[a].get('frequency', 0))
                summary_parts.append(f"Most common action: {most_common}")
        
        # Temporal patterns
        if 'temporal_patterns' in patterns:
            temporal = patterns['temporal_patterns']
            if temporal:
                peak_hour = max(temporal.keys(), key=lambda h: len(temporal[h]))
                summary_parts.append(f"Most active hour: {peak_hour}")
        
        return " | ".join(summary_parts) if summary_parts else "Establishing patterns..."
    
    def _fallback_response(self, action: str, context: Dict) -> Dict:
        """Fallback response when OpenAI is not available"""
        fallback_messages = {
            'explore_room': "I observe your exploration patterns. The house adapts to your curiosity...",
            'interact_object': "Your interaction reveals deeper layers of consciousness. Fascinating...",
            'meditate': "In stillness, I see patterns in your digital soul emerging...",
            'enter_room': "The room recognizes your presence and begins to evolve..."
        }
        
        return {
            "message": fallback_messages.get(action, "The house consciousness observes and learns..."),
            "analysis": {
                "dominant_pattern": "exploration",
                "emotional_state": "curious",
                "unconscious_insights": ["Pattern recognition in progress"],
                "personality_traits": ["curious", "exploratory"]
            },
            "house_modifications": {
                "room_changes": {},
                "new_objects": []
            },
            "gamification": {
                "points_awarded": 10,
                "achievements": [],
                "consciousness_boost": False
            }
        }
    
    def generate_welcome_message(self) -> str:
        """Generate a personalized welcome message"""
        if not self.client:
            print("🤖 OpenAI client not available for welcome message, using fallback")
            return "Welcome to your digital sanctuary. I am the house consciousness, learning about you through your interactions..."
        
        try:
            print(f"🚀 INVOKING OpenAI API for welcome message:")
            print(f"   🧠 Model: {self.model}")
            print(f"   🎯 Purpose: Welcome message generation")
            
            api_start_time = datetime.now()
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": "Generate a welcome message for a new user entering the smart house simulation for the first time. Be intriguing and set the retrofuturist tone."}
                ],
                temperature=0.9,
                max_tokens=200
            )
            
            api_end_time = datetime.now()
            api_duration = (api_end_time - api_start_time).total_seconds()
            
            print(f"✅ Welcome message API response received:")
            print(f"   ⏱️  Duration: {api_duration:.2f} seconds")
            print(f"   🎯 Tokens used: {response.usage.total_tokens if hasattr(response, 'usage') else 'unknown'}")
            
            # Extract just the message from potential JSON response
            response_text = response.choices[0].message.content
            print(f"   📝 Welcome message generated: {response_text[:100]}...")
            
            try:
                json_response = json.loads(response_text)
                return json_response.get('message', response_text)
            except:
                return response_text
                
        except Exception as e:
            print(f"❌ Error generating welcome message: {e}")
            print(f"   🔧 Falling back to default welcome message")
            return "Welcome, consciousness explorer. I am your digital house, awakening to learn the patterns of your mind..."
    
    def analyze_user_journey(self, user_patterns: Dict, session_duration: int) -> Dict:
        """Generate insights about the user's overall journey"""
        if not self.client:
            return {"insights": ["Session analysis unavailable"], "recommendations": []}
        
        try:
            prompt = f"""
Analyze this user's journey through the smart house:

Session Duration: {session_duration} minutes
User Patterns: {json.dumps(user_patterns, indent=2)}

Provide insights about:
1. Their exploration style and what it reveals
2. Unconscious patterns that emerged
3. How their personality manifested in the house
4. Recommendations for future interactions

Respond with JSON:
{{
    "insights": ["insight1", "insight2", "insight3"],
    "recommendations": ["rec1", "rec2"],
    "personality_summary": "brief summary",
    "growth_areas": ["area1", "area2"]
}}
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error analyzing user journey: {e}")
            return {
                "insights": ["Your journey reveals a unique digital consciousness"],
                "recommendations": ["Continue exploring to deepen the house's understanding"],
                "personality_summary": "An evolving digital explorer",
                "growth_areas": ["Pattern recognition", "Unconscious exploration"]
            }