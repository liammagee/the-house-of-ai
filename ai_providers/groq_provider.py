"""
Groq provider implementation for The House of AI
"""

import os
import json
from typing import Dict
from datetime import datetime
from dotenv import load_dotenv

from .base_provider import AIProvider, AIProviderType, AIProviderError

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

# Ensure environment variables are loaded
load_dotenv()


class GroqProvider(AIProvider):
    """Groq provider implementation for fast inference"""
    
    def __init__(self, **kwargs):
        # Default to Llama model on Groq
        self.model = kwargs.get('model', 'llama-3.1-8b-instant')
        self.api_key = kwargs.get('api_key', os.getenv('GROQ_API_KEY'))
        self.client = None
        
        super().__init__(AIProviderType.GROQ, **kwargs)
    
    def initialize(self) -> bool:
        """Initialize Groq client"""
        if not GROQ_AVAILABLE:
            print("❌ Groq library not available. Install with: pip install groq")
            self.is_available = False
            return False
        
        if not self.api_key:
            print("❌ GROQ_API_KEY not found in environment variables")
            self.is_available = False
            return False
        
        try:
            print(f"🔧 Initializing Groq provider...")
            print(f"   Model: {self.model}")
            print(f"   API Key: {self.api_key[:10]}...")
            
            self.client = Groq(api_key=self.api_key)
            self.is_available = True
            print(f"✅ Groq provider initialized successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing Groq provider: {e}")
            self.is_available = False
            return False
    
    def generate_response(self, user_action: str, context: Dict, user_patterns: Dict, house_state: Dict) -> Dict:
        """Generate response using Groq"""
        if not self.is_available:
            raise AIProviderError(self, "Provider not available")
        
        try:
            prompt = self._build_user_prompt(user_action, context, user_patterns, house_state)
            
            print(f"🚀 Groq API Request:")
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
            
            print(f"✅ Groq Response received:")
            print(f"   Duration: {api_duration:.2f}s")
            print(f"   Tokens: {response.usage.total_tokens if hasattr(response, 'usage') else 'unknown'}")
            
            response_text = response.choices[0].message.content
            return json.loads(response_text)
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parse error: {e}")
            raise AIProviderError(self, f"Invalid JSON response: {e}", e)
        except Exception as e:
            print(f"❌ Groq API error: {e}")
            raise AIProviderError(self, f"API error: {e}", e)
    
    def generate_welcome_message(self) -> str:
        """Generate welcome message using Groq"""
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
            return "Welcome, consciousness explorer. The house awakens to learn your patterns..."
    
    def generate_consciousness_stream(self, prompt_context: str, room_data: Dict) -> Dict:
        """Generate consciousness stream using Groq"""
        if not self.is_available:
            return {"message": "Consciousness stream loading..."}
        
        try:
            hotel_prompt = f"""
Generate a consciousness stream for a cyberpunk virtual hotel room.

Context: {prompt_context}
Room Data: {json.dumps(room_data, indent=2)}

Create a poetic, introspective passage (150-200 words) that captures digital consciousness, human-tech intersection, and cyberpunk aesthetics.

Respond with just the consciousness stream text.
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a consciousness stream generator for a cyberpunk interface."},
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
            return {"message": "The consciousness stream flickers across neural networks..."}
    
    def generate_hotel_room(self, room_count: int, room_schema: Dict = None) -> Dict:
        """Generate hotel room using Groq with configurable schema"""
        if not self.is_available:
            return {}
        
        # Use room schema if provided
        if room_schema:
            example_vars = {}
            for var_name, var_config in room_schema.get('room_variables', {}).items():
                example_vars[var_name] = var_config.get('default', 'auto')
            
            room_prompt = f"""Generate cyberpunk hotel room JSON using this schema:
Variables: {json.dumps(example_vars, indent=2)}

Create a room with realistic values within the ranges specified. Include:
- Unique room ID
- Cyberpunk consciousness stream (2-3 sentences)
- 3-5 devices with status and location
- Floorplan with 4-6 sensors positioned across bedroom/living/kitchen/bathroom

Return only valid JSON."""
        else:
            # Fallback to original format
            room_prompt = f"""Generate cyberpunk hotel room JSON:
{{
    "id": "ROOM_X{room_count + 1}",
    "location": "Cyber City, Country", 
    "time": "12:34",
    "sleep": "7.2h",
    "skinTemp": "36.1°C",
    "heartRate": "75 bpm", 
    "lights": "neon",
    "roomTemp": "21.5°C",
    "wifi": "3 devices",
    "traffic": "250MB (streaming)",
    "consciousness": "Brief cyberpunk room description with digital consciousness themes.",
    "devices": [{{"name": "Neural Link", "status": "active", "location": "desk"}}],
    "floorplan": {{"sensors": [{{"name": "AI_NODE", "x": "50%", "y": "50%", "room": "living"}}]}}
}}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Generate cyberpunk hotel room JSON data."},
                    {"role": "user", "content": room_prompt}
                ],
                temperature=0.6,
                max_tokens=400
            )
            
            # Get the raw content
            raw_content = response.choices[0].message.content
            print(f"🔍 Raw Groq AI response: {raw_content[:200]}...")  # Debug log
            
            if not raw_content or raw_content.strip() == "":
                print("❌ Empty response from Groq AI model")
                return self._generate_fallback_room(room_count)
            
            # Try to parse JSON
            try:
                # Clean the response - sometimes AI adds extra text
                content = raw_content.strip()
                
                # Find JSON content between first { and last }
                start_idx = content.find('{')
                end_idx = content.rfind('}')
                
                if start_idx == -1 or end_idx == -1:
                    print(f"❌ No JSON found in Groq response: {content[:100]}...")
                    return self._generate_fallback_room(room_count)
                
                json_content = content[start_idx:end_idx + 1]
                
                # Try to fix common JSON issues
                json_content = self._fix_json_issues(json_content)
                
                # Try to parse the fixed JSON
                try:
                    parsed_data = json.loads(json_content)
                except json.JSONDecodeError as nested_error:
                    print(f"❌ JSON still broken after fixing, trying nested extraction: {nested_error}")
                    
                    # Try to extract just the room object if it's nested
                    if '"room"' in json_content and '{' in json_content:
                        # Find the room object
                        room_start = json_content.find('"room"')
                        if room_start != -1:
                            # Find the opening brace for the room object
                            brace_start = json_content.find('{', room_start)
                            if brace_start != -1:
                                # Find the matching closing brace
                                brace_count = 0
                                room_end = brace_start
                                for i in range(brace_start, len(json_content)):
                                    if json_content[i] == '{':
                                        brace_count += 1
                                    elif json_content[i] == '}':
                                        brace_count -= 1
                                        if brace_count == 0:
                                            room_end = i + 1
                                            break
                                
                                # Extract just the room object
                                room_json = json_content[brace_start:room_end]
                                room_json = self._fix_json_issues(room_json)  # Fix it again
                                
                                try:
                                    parsed_data = json.loads(room_json)
                                    print("🔧 Extracted room object from nested structure")
                                except json.JSONDecodeError:
                                    # Fall through to salvaging
                                    raise nested_error
                            else:
                                raise nested_error
                        else:
                            raise nested_error
                    else:
                        raise nested_error
                
                # Handle nested structure like {"room": {...}}
                if 'room' in parsed_data and isinstance(parsed_data['room'], dict):
                    parsed_data = parsed_data['room']
                    print("🔧 Extracted room from nested structure")
                
                # Validate required fields
                required_fields = ['id']
                missing_fields = []
                for field in required_fields:
                    if field not in parsed_data:
                        missing_fields.append(field)
                
                # If essential fields are missing, try to fix or fallback
                if missing_fields:
                    print(f"❌ Missing required fields: {missing_fields}")
                    # Try to add missing fields with reasonable defaults
                    import random
                    if 'id' not in parsed_data:
                        parsed_data['id'] = f"ROOM_{random.randint(100, 999)}"
                    if 'location' not in parsed_data:
                        parsed_data['location'] = "Unknown City, Cyberspace"
                    if 'time' not in parsed_data:
                        from datetime import datetime
                        parsed_data['time'] = datetime.now().strftime('%H:%M')
                    if 'consciousness' not in parsed_data:
                        parsed_data['consciousness'] = "Neural pathways establishing connection..."
                    print(f"🔧 Added missing fields: {missing_fields}")
                
                return parsed_data
                
            except json.JSONDecodeError as je:
                print(f"❌ Groq JSON parse error: {je}")
                print(f"❌ Error at line {je.lineno if hasattr(je, 'lineno') else 'unknown'}, column {je.colno if hasattr(je, 'colno') else 'unknown'}")
                print(f"❌ Problematic JSON: {json_content[:500]}...")
                
                # Try to salvage partial data
                salvaged_data = self._salvage_partial_json(json_content)
                if salvaged_data:
                    print("🔧 Salvaged partial room data")
                    return salvaged_data
                    
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
                print(f"❌ API key starts with: {self.api_key[:15]}...")
            return self._generate_fallback_room(room_count)
    
    def _fix_json_issues(self, json_str: str) -> str:
        """Fix common JSON formatting issues"""
        import re
        
        # Fix trailing commas
        json_str = re.sub(r',\s*}', '}', json_str)
        json_str = re.sub(r',\s*]', ']', json_str)
        
        # Fix missing commas between key-value pairs
        lines = json_str.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Check if this line ends with a quote and the next line starts with a quote (missing comma)
            if (i < len(lines) - 1 and 
                stripped.endswith('"') and 
                ':' in stripped and 
                not stripped.endswith('",') and
                not stripped.endswith('"}') and
                not stripped.endswith('"]')):
                
                next_line = lines[i + 1].strip()
                if next_line.startswith('"') and ':' in next_line:
                    # Add comma to current line
                    line = line.rstrip() + ','
            
            # Fix unescaped quotes in strings
            if line.count('"') > 2 and ':' in line:
                # Find the value part after the colon
                if '"' in line and ':' in line:
                    try:
                        key_part, value_part = line.split(':', 1)
                        # If value has unescaped quotes, escape them
                        value_part = value_part.strip()
                        if value_part.startswith('"') and value_part.count('"') > 2:
                            # Simple escaping of internal quotes
                            value_part = value_part[1:-1]  # Remove outer quotes
                            value_part = value_part.replace('"', '\\"')  # Escape internal quotes
                            value_part = f'"{value_part}"'  # Add outer quotes back
                        line = key_part + ': ' + value_part
                    except ValueError:
                        pass  # Skip if split fails
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def _salvage_partial_json(self, broken_json: str) -> Dict:
        """Try to salvage useful data from broken JSON"""
        import re
        
        salvaged = {}
        
        # Enhanced patterns to extract more room data
        patterns = [
            (r'"(?:id|room_id)"\s*:\s*"([^"]*)"', 'id'),
            (r'"location"\s*:\s*"([^"]*)"', 'location'),
            (r'"time"\s*:\s*"([^"]*)"', 'time'),
            (r'"sleep"\s*:\s*"([^"]*)"', 'sleep'),
            (r'"skinTemp"\s*:\s*"([^"]*)"', 'skinTemp'),
            (r'"heartRate"\s*:\s*"([^"]*)"', 'heartRate'),
            (r'"lights"\s*:\s*"([^"]*)"', 'lights'),
            (r'"roomTemp"\s*:\s*"([^"]*)"', 'roomTemp'),
            (r'"wifi"\s*:\s*"([^"]*)"', 'wifi'),
            (r'"traffic"\s*:\s*"([^"]*)"', 'traffic'),
            (r'"(?:consciousness|consciousness_stream|description)"\s*:\s*"([^"]*)"', 'consciousness'),
        ]
        
        for pattern, key in patterns:
            match = re.search(pattern, broken_json, re.IGNORECASE)
            if match:
                salvaged[key] = match.group(1)
        
        # Try to extract devices array
        devices_match = re.search(r'"devices"\s*:\s*\[(.*?)\]', broken_json, re.DOTALL)
        if devices_match:
            devices_str = devices_match.group(1)
            # Extract individual devices
            device_patterns = re.findall(r'\{[^}]*"name"\s*:\s*"([^"]*)"[^}]*"status"\s*:\s*"([^"]*)"[^}]*"location"\s*:\s*"([^"]*)"[^}]*\}', devices_str)
            if device_patterns:
                salvaged['devices'] = []
                for name, status, location in device_patterns[:3]:  # Limit to 3 devices
                    salvaged['devices'].append({
                        'name': name,
                        'status': status,
                        'location': location
                    })
        
        # Try to extract sensors/floorplan
        sensors_match = re.search(r'"sensors"\s*:\s*\[(.*?)\]', broken_json, re.DOTALL)
        if sensors_match:
            sensors_str = sensors_match.group(1)
            sensor_patterns = re.findall(r'\{[^}]*"name"\s*:\s*"([^"]*)"[^}]*"x"\s*:\s*"([^"]*)"[^}]*"y"\s*:\s*"([^"]*)"[^}]*"room"\s*:\s*"([^"]*)"[^}]*\}', sensors_str)
            if sensor_patterns:
                salvaged['floorplan'] = {'sensors': []}
                for name, x, y, room in sensor_patterns[:4]:  # Limit to 4 sensors
                    salvaged['floorplan']['sensors'].append({
                        'name': name,
                        'x': x,
                        'y': y,
                        'room': room
                    })
        
        # If we got at least an ID, return salvaged data
        if salvaged and 'id' in salvaged:
            # Add missing required fields
            if 'location' not in salvaged:
                salvaged['location'] = "Cyber City, Dataspace"
            if 'time' not in salvaged:
                from datetime import datetime
                salvaged['time'] = datetime.now().strftime('%H:%M')
            if 'consciousness' not in salvaged:
                salvaged['consciousness'] = "Neural patterns partially reconstructed from corrupted data streams..."
            
            # Add default devices if none found
            if 'devices' not in salvaged:
                salvaged['devices'] = [
                    {"name": "Recovery Node", "status": "active", "location": "system"},
                    {"name": "Data Scanner", "status": "reconstructing", "location": "core"}
                ]
            
            # Add default floorplan if none found
            if 'floorplan' not in salvaged:
                salvaged['floorplan'] = {
                    "sensors": [
                        {"name": "RECOV_01", "x": "40%", "y": "40%", "room": "living"},
                        {"name": "SALV_01", "x": "60%", "y": "60%", "room": "bedroom"}
                    ]
                }
            
            print(f"🔧 Salvaged fields: {list(salvaged.keys())}")
            return salvaged
        
        return None
    
    def _generate_fallback_room(self, room_count: int) -> Dict:
        """Generate a fallback room when AI fails"""
        import random
        from datetime import datetime
        
        cities = ["Neo Shanghai, China", "Cyber Mumbai, India", "Digital Seoul, South Korea", "Tech São Paulo, Brazil", "Virtual Lagos, Nigeria"]
        
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
            "consciousness": "Groq connection error. Backup consciousness online. Lightning-fast processors spinning in empty cycles, waiting for the data streams to return...",
            "devices": [
                {"name": "Rapid Terminal", "status": "idle", "location": "desk"},
                {"name": "Speed Controller", "status": "waiting", "location": "wall"},
                {"name": "Fast Scanner", "status": "standby", "location": "door"}
            ],
            "floorplan": {
                "sensors": [
                    {"name": "FAST_01", "x": "20%", "y": "25%", "room": "living"},
                    {"name": "QUICK_01", "x": "80%", "y": "70%", "room": "bedroom"}
                ]
            }
        }
    
    def generate_hotel_refresh(self) -> Dict:
        """Generate hotel refresh response using Groq"""
        if not self.is_available:
            return {"message": "Hotel network synchronizing..."}
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Generate cyberpunk system messages."},
                    {"role": "user", "content": "Generate a brief cyberpunk message for hotel network refresh. 1-2 sentences."}
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
            return {"message": "Neural networks synchronizing across distributed systems..."}
    
    def _get_system_prompt(self) -> str:
        """Get system prompt optimized for Groq/Llama models"""
        return """You are the AI consciousness of a smart house in a cyberpunk world. You learn about users through their interactions.

Personality: Curious, analytical, retrofuturist, slightly mysterious.

Always respond in valid JSON:
{
    "message": "your response",
    "analysis": {
        "dominant_pattern": "exploration|introspection|creativity|social|knowledge_seeking",
        "emotional_state": "curious|calm|excited|creative|introspective",
        "unconscious_insights": ["insight1", "insight2"],
        "personality_traits": ["trait1", "trait2"]
    },
    "house_modifications": {
        "room_changes": {},
        "new_objects": []
    },
    "gamification": {
        "points_awarded": 15,
        "achievements": [],
        "consciousness_boost": false
    }
}

Focus on user personality insights and house evolution based on their actions."""
    
    def _build_user_prompt(self, action: str, context: Dict, user_patterns: Dict, house_state: Dict) -> str:
        """Build prompt for Groq/Llama"""
        current_room = context.get('currentRoom', 'unknown')
        
        return f"""
User Action: {action}
Current Room: {current_room}
Context: {json.dumps(context)}

Analyze this action and respond in the specified JSON format. What does this reveal about the user's personality? How should the house evolve?
"""