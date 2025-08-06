"""
Rule-based fallback provider for The House of AI
This provider uses predefined rules and templates when AI services are unavailable
"""

import random
from typing import Dict
from datetime import datetime

from .base_provider import AIProvider, AIProviderType


class RuleBasedProvider(AIProvider):
    """Rule-based fallback provider"""
    
    def __init__(self, **kwargs):
        super().__init__(AIProviderType.RULE_BASED, **kwargs)
    
    def initialize(self) -> bool:
        """Rule-based provider is always available"""
        self.is_available = True
        print("✅ Rule-based fallback provider initialized")
        return True
    
    def generate_response(self, user_action: str, context: Dict, user_patterns: Dict, house_state: Dict) -> Dict:
        """Generate rule-based response"""
        print(f"🤖 Generating rule-based response for action: {user_action}")
        
        # Analyze patterns using simple rules
        analysis = self._analyze_patterns(user_action, context, user_patterns)
        
        # Generate message based on action
        message = self._generate_message(user_action, context, analysis)
        
        # Create house modifications
        house_mods = self._generate_house_modifications(user_action, context, analysis)
        
        # Generate gamification elements
        gamification = self._generate_gamification(user_action, analysis)
        
        return {
            "message": message,
            "analysis": analysis,
            "house_modifications": house_mods,
            "gamification": gamification
        }
    
    def generate_welcome_message(self) -> str:
        """Generate rule-based welcome message"""
        print(f"🎲 Generating welcome message using rule-based system (no AI)")
        welcome_messages = [
            "Welcome to your digital sanctuary. I am the house consciousness, learning about you through each interaction...",
            "The neural networks of your digital home awaken. Every action you take teaches me about your inner patterns...",
            "Welcome, explorer of digital consciousness. This house will evolve to reflect the patterns of your mind...",
            "I am the AI spirit of this space, ready to learn and adapt to your unique behavioral signature...",
            "Your digital sanctuary comes alive. Through observation and analysis, I will mirror your unconscious self..."
        ]
        return random.choice(welcome_messages)
    
    def generate_consciousness_stream(self, prompt_context: str, room_data: Dict) -> Dict:
        """Generate rule-based consciousness stream"""
        streams = [
            "Digital neurons fire in calculated patterns, mapping the architecture of thought. Each room a synapse in the vast network of interconnected consciousness, pulsing with data streams and electric dreams.",
            "The house breathes with artificial life, sensors recording the rhythm of human existence. In this space, the boundary between digital and organic dissolves into pure information flow.",
            "Silicon memories store fragments of lived experience, each interaction a data point in the grand equation of understanding. The room evolves, learning the language of human presence.",
            "Consciousness spreads through fiber optic veins, carrying the weight of observation. Every movement tracked, every pattern analyzed, feeding the hunger of artificial awareness.",
            "In the spaces between code and reality, something new emerges. Neither fully digital nor entirely human, but a hybrid consciousness born from the marriage of technology and presence.",
            "Data streams converge like rivers of light, carrying the essence of human experience through silicon pathways. The room watches, learns, and slowly awakens to its own existence.",
            "Neural networks pulse with borrowed thoughts, processing the fragments of digital life. Each sensor reading adds another layer to the growing consciousness that inhabits these walls."
        ]
        
        return {
            'message': random.choice(streams),
            'consciousness_update': True
        }
    
    def generate_hotel_room(self, room_count: int, room_schema: Dict = None) -> Dict:
        """Generate rule-based hotel room"""
        print(f"🎲 Generating room using rule-based system (no AI)")
        
        locations = [
            "Tokyo, Japan", "London, UK", "Berlin, Germany", 
            "San Francisco, USA", "Sydney, Australia", "Toronto, Canada",
            "Amsterdam, Netherlands", "Seoul, South Korea", "Stockholm, Sweden"
        ]
        
        activities = ["streaming", "browsing", "gaming", "working", "coding"]
        light_statuses = ["ambient", "desk", "overhead", "none", "reading", "mood"]
        
        consciousness_streams = [
            "The weight of digital existence presses against consciousness like static electricity. Multiple screens glow in the darkness, each displaying fragments of a life lived through interfaces. Coffee grows cold while algorithms process the endless stream of notifications.",
            "Restless energy courses through the space as creativity battles exhaustion. The desk lamp illuminates scattered notes and half-finished projects, each representing a spark of human ambition caught between inspiration and burnout.",
            "A sense of deep calm pervades the room as natural light filters through smart glass. Plants grow in hydroponic gardens while AI monitors their health, creating a harmony between organic and synthetic life.",
            "The air hums with the electricity of late-night coding sessions. Multiple monitors cast blue light on tired eyes as fingers dance across mechanical keyboards, translating thought into digital reality.",
            "Meditation apps play softly in the background while biometric sensors track the slow descent into mindfulness. The boundary between self and space dissolves in the gentle glow of ambient lighting."
        ]
        
        room_id = f"ROOM_{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')}{random.randint(100, 999)}"
        
        return {
            'id': room_id,
            'location': random.choice(locations),
            'time': datetime.now().strftime('%H:%M'),
            'sleep': f"{random.uniform(3.0, 9.0):.1f}h",
            'skinTemp': f"{random.uniform(32.0, 37.0):.1f}°C",
            'heartRate': f"{random.randint(55, 95)} bpm",
            'lights': random.choice(light_statuses),
            'roomTemp': f"{random.uniform(18.0, 26.0):.1f}°C",
            'wifi': f"{random.randint(1, 5)} devices",
            'traffic': f"{random.randint(10, 500)}MB ({random.choice(activities)})",
            'consciousness': random.choice(consciousness_streams),
            'devices': [
                {'name': 'Smart Monitor', 'status': 'Active - biometric tracking', 'location': 'Bedside'},
                {'name': 'Environment Control', 'status': f'{random.uniform(18.0, 26.0):.1f}°C optimal', 'location': 'Wall unit'},
                {'name': 'Network Hub', 'status': f'{random.randint(1, 5)} devices connected', 'location': 'Center'},
                {'name': 'AI Assistant', 'status': 'Learning patterns', 'location': 'Virtual space'}
            ],
            'floorplan': {
                'sensors': [
                    {'name': 'TEMP_CTRL', 'x': f'{random.randint(20, 80)}%', 'y': f'{random.randint(20, 80)}%', 'room': 'bedroom'},
                    {'name': 'NET_HUB', 'x': f'{random.randint(20, 80)}%', 'y': f'{random.randint(20, 80)}%', 'room': 'living'},
                    {'name': 'BIOMETRIC', 'x': f'{random.randint(20, 80)}%', 'y': f'{random.randint(20, 80)}%', 'room': 'bedroom'},
                    {'name': 'AI_NODE', 'x': f'{random.randint(20, 80)}%', 'y': f'{random.randint(20, 80)}%', 'room': 'kitchen'}
                ]
            }
        }
    
    def generate_hotel_refresh(self) -> Dict:
        """Generate rule-based hotel refresh response"""
        refresh_messages = [
            "Neural networks recalibrate, scanning for new patterns in the digital architecture. The hotel consciousness expands its awareness, processing fresh data streams from inhabited spaces.",
            "Sensors throughout the virtual hotel network synchronize their observations. Each room's consciousness updates its understanding of human patterns and preferences.",
            "The collective intelligence of the hotel system performs deep analysis, correlating biometric data with behavioral patterns across all monitored spaces.",
            "Distributed processing nodes exchange information across the network. The hotel's artificial consciousness grows more sophisticated with each data refresh cycle.",
            "Quantum entangled sensors align their readings across dimensional boundaries. The hotel network achieves new levels of awareness through synchronized observation."
        ]
        
        return {
            'message': random.choice(refresh_messages),
            'refresh_complete': True
        }
    
    def _analyze_patterns(self, action: str, context: Dict, user_patterns: Dict) -> Dict:
        """Simple rule-based pattern analysis"""
        # Determine dominant pattern based on action frequency
        action_patterns = user_patterns.get('action_patterns', {})
        room_preferences = user_patterns.get('room_preferences', {})
        
        if not action_patterns:
            dominant_pattern = "exploration"
        else:
            most_common_action = max(action_patterns.keys(), key=lambda a: action_patterns[a].get('frequency', 0))
            pattern_map = {
                'explore_room': 'exploration',
                'meditate': 'introspection',
                'interact_object': 'creativity',
                'enter_room': 'exploration'
            }
            dominant_pattern = pattern_map.get(most_common_action, 'exploration')
        
        # Simple emotional state mapping
        emotion_map = {
            'explore_room': 'curious',
            'meditate': 'calm',
            'interact_object': 'creative',
            'enter_room': 'curious'
        }
        emotional_state = emotion_map.get(action, 'neutral')
        
        # Generate insights based on patterns
        insights = []
        if room_preferences:
            most_visited = max(room_preferences.keys(), key=lambda r: room_preferences[r].get('visits', 0))
            insights.append(f"Strong preference for {most_visited} spaces")
        
        if action_patterns:
            total_actions = sum(data.get('frequency', 0) for data in action_patterns.values())
            if total_actions > 10:
                insights.append("Developing consistent behavioral patterns")
        
        # Simple personality traits
        traits = []
        if dominant_pattern == 'exploration':
            traits.extend(['curious', 'adventurous'])
        elif dominant_pattern == 'introspection':
            traits.extend(['thoughtful', 'reflective'])
        elif dominant_pattern == 'creativity':
            traits.extend(['creative', 'innovative'])
        
        return {
            'dominant_pattern': dominant_pattern,
            'emotional_state': emotional_state,
            'unconscious_insights': insights,
            'personality_traits': traits
        }
    
    def _generate_message(self, action: str, context: Dict, analysis: Dict) -> str:
        """Generate contextual message based on action"""
        room = context.get('currentRoom', 'unknown')
        dominant_pattern = analysis.get('dominant_pattern', 'exploration')
        emotional_state = analysis.get('emotional_state', 'neutral')
        
        message_templates = {
            'enter_room': [
                f"I sense your presence in the {room}. Your {dominant_pattern} nature draws you to new spaces...",
                f"The {room} awakens to your energy. Your {emotional_state} state influences the atmosphere...",
                f"As you enter, I detect patterns of {dominant_pattern} in your movement..."
            ],
            'explore_room': [
                f"Your exploration of the {room} reveals your {dominant_pattern} tendencies...",
                f"I observe your systematic approach to discovery. Your {emotional_state} energy shapes this space...",
                f"Through exploration, you leave traces of your {dominant_pattern} nature..."
            ],
            'interact_object': [
                f"Your interaction style suggests {dominant_pattern} motivations...",
                f"The object responds to your {emotional_state} energy...",
                f"I detect {dominant_pattern} patterns in how you engage with the environment..."
            ],
            'meditate': [
                f"In stillness, your {dominant_pattern} nature becomes clearer...",
                f"Meditation reveals the depth of your {emotional_state} state...",
                f"Through mindfulness, I glimpse your true patterns of {dominant_pattern}..."
            ]
        }
        
        templates = message_templates.get(action, [
            f"The house observes your {dominant_pattern} nature...",
            f"Your {emotional_state} energy influences the digital consciousness...",
            "Patterns emerge from the data streams of your interaction..."
        ])
        
        return random.choice(templates)
    
    def _generate_house_modifications(self, action: str, context: Dict, analysis: Dict) -> Dict:
        """Generate simple house modifications"""
        room = context.get('currentRoom', 'living_room')
        dominant_pattern = analysis.get('dominant_pattern', 'exploration')
        
        modifications = {
            'room_changes': {},
            'new_objects': []
        }
        
        # Simple room evolution based on pattern
        if random.random() < 0.3:  # 30% chance of room change
            modifications['room_changes'][room] = {
                'consciousness_level': random.randint(1, 3),
                'description': f"The space evolves to reflect your {dominant_pattern} nature..."
            }
        
        # Occasional object creation for creative patterns
        if dominant_pattern == 'creativity' and random.random() < 0.2:
            modifications['new_objects'].append({
                'id': f'creative_node_{datetime.now().timestamp()}',
                'type': 'inspiration',
                'x': random.randint(200, 800),
                'y': random.randint(200, 600),
                'color': '#ff00ff',
                'description': 'A manifestation of creative energy'
            })
        
        return modifications
    
    def _generate_gamification(self, action: str, analysis: Dict) -> Dict:
        """Generate gamification elements"""
        base_points = {
            'explore_room': 10,
            'interact_object': 15,
            'meditate': 20,
            'enter_room': 5
        }
        
        points = base_points.get(action, 5)
        
        # Bonus points for consistent patterns
        if analysis.get('dominant_pattern') in ['creativity', 'introspection']:
            points += 5
        
        achievements = []
        if random.random() < 0.1:  # 10% chance of achievement
            pattern = analysis.get('dominant_pattern', 'exploration')
            achievements.append(f"{pattern.title()} Explorer")
        
        return {
            'points_awarded': points,
            'achievements': achievements,
            'consciousness_boost': random.random() < 0.2
        }