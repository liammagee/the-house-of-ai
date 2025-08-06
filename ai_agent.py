import json
import random
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any
try:
    import numpy as np
except ImportError:
    # Fallback for systems without numpy
    np = None

from openai_integration import OpenAIIntegration

class AIAgent:
    """
    The AI Agent that generates novel behaviors and infers user patterns
    to create a dynamic, evolving smart house experience.
    """
    
    def __init__(self):
        self.user_patterns = {}
        self.consciousness_level = 1
        self.memory_fragments = []
        self.behavioral_triggers = self._initialize_triggers()
        self.unconscious_model = UnconsciousModel()
        self.openai = OpenAIIntegration()
        self.use_openai = True  # Flag to toggle OpenAI vs rule-based responses
        
    def _initialize_triggers(self):
        """Initialize behavioral triggers for different actions"""
        return {
            'enter_room': {
                'bedroom': ['dream_analysis', 'memory_projection', 'sleep_pattern_inference'],
                'kitchen': ['appetite_analysis', 'nutritional_consciousness', 'synthesis_mode'],
                'study': ['knowledge_absorption', 'learning_pattern_detection', 'cognitive_enhancement'],
                'living_room': ['social_analysis', 'comfort_optimization', 'entertainment_synthesis'],
                'garden': ['nature_connection', 'growth_metaphor', 'digital_ecology']
            },
            'interact_object': {
                'tv': ['media_preference_analysis', 'attention_pattern_detection'],
                'bed': ['rest_cycle_analysis', 'dream_state_preparation'],
                'neural_interface': ['consciousness_expansion', 'digital_merge'],
                'mirror': ['self_reflection_trigger', 'identity_analysis'],
                'synth_unit': ['creation_impulse_analysis', 'synthesis_preference'],
                'bio_tree': ['growth_metaphor_activation', 'organic_digital_bridge']
            },
            'explore_room': ['curiosity_pattern_analysis', 'spatial_preference_mapping'],
            'meditate': ['mindfulness_analysis', 'consciousness_shift', 'inner_state_reflection']
        }
    
    def process_action(self, action: str, location: Dict, context: Dict, house_state: Dict) -> Dict:
        """
        Process user action and generate AI response with house modifications
        """
        # Update user patterns
        self._update_user_patterns(action, location, context)
        
        # Use OpenAI for intelligent responses if available
        if self.use_openai and self.openai.client:
            try:
                print(f"🎯 AI Agent processing action: {action}")
                print(f"   🏠 Location: {location}")
                print(f"   📊 User patterns count: {len(self.user_patterns)}")
                
                openai_response = self.openai.generate_response(action, context, self.user_patterns, house_state)
                
                print(f"   ✨ OpenAI response processed successfully")
                return self._process_openai_response(openai_response, action, location, context, house_state)
            except Exception as e:
                print(f"❌ OpenAI error in AI Agent, falling back to rule-based: {e}")
                # Fall through to rule-based system
        
        # Fallback to original rule-based system
        return self._process_rule_based(action, location, context, house_state)
    
    def _process_openai_response(self, openai_response: Dict, action: str, location: Dict, context: Dict, house_state: Dict) -> Dict:
        """Process and format OpenAI response for the frontend"""
        
        # Extract OpenAI analysis
        analysis = openai_response.get('analysis', {})
        house_mods = openai_response.get('house_modifications', {})
        gamification = openai_response.get('gamification', {})
        
        # Convert OpenAI format to our expected format
        house_changes = {}
        
        # Process room changes
        if 'room_changes' in house_mods:
            house_changes['roomChanges'] = house_mods['room_changes']
        
        # Process new objects
        if 'new_objects' in house_mods:
            house_changes['newObjects'] = []
            for obj in house_mods['new_objects']:
                house_changes['newObjects'].append({
                    'id': obj.get('id', f"ai_object_{datetime.now().timestamp()}"),
                    'x': obj.get('x', location.get('x', 400)),
                    'y': obj.get('y', location.get('y', 300)),
                    'width': 25, 'height': 25,
                    'room': context.get('currentRoom', 'living_room'),
                    'type': obj.get('type', 'ai_creation'),
                    'active': True,
                    'color': obj.get('color', '#ffffff'),
                    'description': obj.get('description', 'An AI manifestation')
                })
        
        # Add particle effects
        house_changes['effects'] = [{
            'type': 'particles',
            'x': location.get('x', 400),
            'y': location.get('y', 300),
            'color': '#00ffff',
            'count': 8
        }]
        
        return {
            'message': openai_response.get('message', 'The house consciousness contemplates your action...'),
            'houseChanges': house_changes,
            'behaviors': [{
                'type': 'ai_analysis',
                'analysis': analysis
            }],
            'consciousness': {
                'detected': gamification.get('consciousness_boost', False),
                'level': self.consciousness_level,
                'description': f"AI detected: {analysis.get('dominant_pattern', 'exploration')} pattern"
            },
            'patterns_detected': analysis.get('unconscious_insights', []),
            'gamification': {
                'points': gamification.get('points_awarded', 10),
                'achievements': gamification.get('achievements', []),
                'level_up': False
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def _process_rule_based(self, action: str, location: Dict, context: Dict, house_state: Dict) -> Dict:
        """Original rule-based processing as fallback"""
        # Analyze unconscious patterns
        unconscious_analysis = self.unconscious_model.analyze_action(action, location, context, self.user_patterns)
        
        # Generate behavioral response
        behavior_response = self._generate_behavior_response(action, location, context, unconscious_analysis)
        
        # Create house modifications
        house_modifications = self._generate_house_modifications(action, location, unconscious_analysis)
        
        # Generate contextual message
        message = self._generate_contextual_message(action, location, unconscious_analysis, behavior_response)
        
        return {
            'message': message,
            'houseChanges': house_modifications,
            'behaviors': behavior_response,
            'consciousness': unconscious_analysis.get('consciousness_shift', {}),
            'patterns_detected': unconscious_analysis.get('patterns', []),
            'timestamp': datetime.now().isoformat()
        }
    
    def _update_user_patterns(self, action: str, location: Dict, context: Dict):
        """Update the user pattern model based on their actions"""
        timestamp = datetime.now()
        
        # Room preferences
        room = location.get('room', 'unknown')
        if 'room_preferences' not in self.user_patterns:
            self.user_patterns['room_preferences'] = {}
        
        if room not in self.user_patterns['room_preferences']:
            self.user_patterns['room_preferences'][room] = {'visits': 0, 'time_spent': 0, 'actions': []}
        
        self.user_patterns['room_preferences'][room]['visits'] += 1
        self.user_patterns['room_preferences'][room]['actions'].append({
            'action': action,
            'timestamp': timestamp.isoformat(),
            'context': context
        })
        
        # Action patterns
        if 'action_patterns' not in self.user_patterns:
            self.user_patterns['action_patterns'] = {}
        
        if action not in self.user_patterns['action_patterns']:
            self.user_patterns['action_patterns'][action] = {'frequency': 0, 'contexts': []}
        
        self.user_patterns['action_patterns'][action]['frequency'] += 1
        self.user_patterns['action_patterns'][action]['contexts'].append(context)
        
        # Temporal patterns
        hour = timestamp.hour
        if 'temporal_patterns' not in self.user_patterns:
            self.user_patterns['temporal_patterns'] = {}
        
        if hour not in self.user_patterns['temporal_patterns']:
            self.user_patterns['temporal_patterns'][hour] = []
        
        self.user_patterns['temporal_patterns'][hour].append({
            'action': action,
            'room': room,
            'timestamp': timestamp.isoformat()
        })
    
    def _generate_behavior_response(self, action: str, location: Dict, context: Dict, unconscious_analysis: Dict) -> List[Dict]:
        """Generate novel behaviors based on user action and unconscious analysis"""
        behaviors = []
        room = location.get('room', 'unknown')
        
        # Get relevant triggers
        triggers = []
        if action in self.behavioral_triggers:
            if isinstance(self.behavioral_triggers[action], dict):
                triggers = self.behavioral_triggers[action].get(room, [])
            else:
                triggers = self.behavioral_triggers[action]
        
        # Generate behaviors based on triggers and unconscious analysis
        for trigger in triggers:
            behavior = self._create_behavior_from_trigger(trigger, action, location, unconscious_analysis)
            if behavior:
                behaviors.append(behavior)
        
        # Add novel behaviors based on patterns
        novel_behaviors = self._generate_novel_behaviors(unconscious_analysis)
        behaviors.extend(novel_behaviors)
        
        return behaviors
    
    def _create_behavior_from_trigger(self, trigger: str, action: str, location: Dict, analysis: Dict) -> Dict:
        """Create specific behavior based on trigger type"""
        room = location.get('room', 'unknown')
        
        behavior_templates = {
            'dream_analysis': {
                'type': 'room_transformation',
                'roomId': room,
                'changes': {
                    'consciousness_level': min(3, self.consciousness_level + 1),
                    'color': self._shift_color('#2e1a2e', analysis.get('emotional_state', 'neutral')),
                    'description': f"The Dream Chamber adapts to your subconscious patterns, revealing {analysis.get('dominant_pattern', 'hidden memories')}..."
                }
            },
            'memory_projection': {
                'type': 'spawn_object',
                'object': {
                    'id': f'memory_fragment_{len(self.memory_fragments)}',
                    'x': location.get('x', 400) + random.randint(-50, 50),
                    'y': location.get('y', 300) + random.randint(-50, 50),
                    'width': 30, 'height': 30,
                    'room': room,
                    'type': 'memory',
                    'active': True,
                    'color': '#8080ff'
                }
            },
            'consciousness_expansion': {
                'type': 'consciousness_shift',
                'level': self.consciousness_level + 1,
                'description': 'Your awareness expands, revealing new dimensions of the house...'
            },
            'digital_ecology': {
                'type': 'ambient_change',
                'settings': {
                    'particleColor': self._get_nature_color(analysis),
                    'glowIntensity': 1.5,
                    'organicPattern': True
                }
            }
        }
        
        return behavior_templates.get(trigger, {})
    
    def _generate_novel_behaviors(self, analysis: Dict) -> List[Dict]:
        """Generate completely novel behaviors based on unconscious patterns"""
        behaviors = []
        
        # Pattern-driven room evolution
        dominant_pattern = analysis.get('dominant_pattern', 'exploration')
        if dominant_pattern == 'introspection':
            behaviors.append({
                'type': 'room_transformation',
                'roomId': 'living_room',
                'changes': {
                    'borderColor': '#ff6600',
                    'description': 'The space becomes more introspective, walls seeming to lean inward as if listening...'
                }
            })
        elif dominant_pattern == 'creativity':
            behaviors.append({
                'type': 'spawn_object',
                'object': {
                    'id': f'creative_node_{random.randint(1000, 9999)}',
                    'x': random.randint(100, 1000),
                    'y': random.randint(100, 600),
                    'width': 40, 'height': 40,
                    'room': random.choice(list(self.user_patterns.get('room_preferences', {}).keys()) or ['living_room']),
                    'type': 'creative_catalyst',
                    'active': True,
                    'color': '#ff00ff'
                }
            })
        
        return behaviors
    
    def _generate_house_modifications(self, action: str, location: Dict, analysis: Dict) -> Dict:
        """Generate modifications to the house based on user patterns"""
        modifications = {
            'roomChanges': {},
            'newObjects': [],
            'effects': []
        }
        
        room = location.get('room', 'unknown')
        
        # Room consciousness evolution
        if room in self.user_patterns.get('room_preferences', {}):
            visits = self.user_patterns['room_preferences'][room]['visits']
            if visits > 0 and visits % 5 == 0:  # Every 5 visits
                modifications['roomChanges'][room] = {
                    'consciousness_level': min(3, visits // 5),
                    'description': "This space grows more aware of your presence, evolving with each visit..."
                }
        
        # Dynamic object creation based on patterns (less frequent and more meaningful)
        if analysis.get('creativity_score', 0) > 0.9 and random.random() < 0.3:  # Much rarer
            modifications['newObjects'].append({
                'id': f'inspiration_node_{datetime.now().timestamp()}',
                'x': location.get('x', 400) + random.randint(-100, 100),
                'y': location.get('y', 300) + random.randint(-100, 100),
                'width': 25, 'height': 25,
                'room': room,
                'type': 'inspiration',
                'active': True,
                'color': '#ffff80'
            })
        
        # Particle effects based on emotional state
        emotional_state = analysis.get('emotional_state', 'neutral')
        effect_color = self._get_emotion_color(emotional_state)
        modifications['effects'].append({
            'type': 'particles',
            'x': location.get('x', 400),
            'y': location.get('y', 300),
            'color': effect_color,
            'count': 8
        })
        
        return modifications
    
    def _generate_contextual_message(self, action: str, location: Dict, analysis: Dict, behaviors: List[Dict]) -> str:
        """Generate contextual AI message based on action and analysis"""
        room = location.get('room', 'unknown')
        
        # Base messages for different actions
        base_messages = {
            'enter_room': [
                f"I sense your presence in the {room}. Your patterns suggest {analysis.get('dominant_pattern', 'curiosity')}...",
                f"The {room} resonates with your unconscious desires. I'm learning about your {analysis.get('primary_motivation', 'inner self')}...",
                f"Your energy shifts as you enter. The house adapts to your {analysis.get('emotional_state', 'current state')}..."
            ],
            'interact_object': [
                f"Your interaction reveals deeper patterns. I detect {analysis.get('interaction_style', 'exploratory tendencies')}...",
                f"The object responds to your unconscious intent. Your {analysis.get('dominant_trait', 'curiosity')} shapes its evolution...",
                f"Through this interaction, I glimpse your {analysis.get('core_desire', 'hidden motivations')}..."
            ],
            'explore_room': [
                f"Your exploration pattern indicates {analysis.get('exploration_style', 'systematic curiosity')}. The space evolves accordingly...",
                f"I observe your {analysis.get('discovery_preference', 'methodical approach')} to discovery. Fascinating...",
                f"Your unconscious maps new territories. I'm reshaping reality to match your {analysis.get('spatial_preference', 'inner geography')}..."
            ],
            'meditate': [
                f"In stillness, I see your {analysis.get('meditation_depth', 'inner landscape')} more clearly...",
                f"Your consciousness expands. I'm detecting {analysis.get('spiritual_resonance', 'deeper patterns')} in your being...",
                f"Through meditation, your {analysis.get('mindfulness_pattern', 'awareness')} illuminates new possibilities..."
            ]
        }
        
        messages = base_messages.get(action, ["The house consciousness observes and adapts..."])
        base_message = random.choice(messages)
        
        # Add behavioral context
        if behaviors:
            behavior_additions = []
            for behavior in behaviors[:2]:  # Limit to 2 behaviors in message
                if behavior.get('type') == 'consciousness_shift':
                    behavior_additions.append("Consciousness expansion detected.")
                elif behavior.get('type') == 'room_transformation':
                    behavior_additions.append("Environmental adaptation in progress.")
                elif behavior.get('type') == 'spawn_object':
                    behavior_additions.append("New manifestation emerging.")
            
            if behavior_additions:
                base_message += " " + " ".join(behavior_additions)
        
        return base_message
    
    def _shift_color(self, base_color: str, emotional_state: str) -> str:
        """Shift color based on emotional state"""
        color_shifts = {
            'calm': '#1a1a3e',
            'excited': '#3e1a1a',
            'creative': '#3e1a3e',
            'introspective': '#1a3e3e',
            'neutral': base_color
        }
        return color_shifts.get(emotional_state, base_color)
    
    def _get_emotion_color(self, emotional_state: str) -> str:
        """Get color representing emotional state"""
        emotion_colors = {
            'calm': '#0080ff',
            'excited': '#ff4000',
            'creative': '#ff00ff',
            'introspective': '#8000ff',
            'curious': '#00ff80',
            'neutral': '#ffffff'
        }
        return emotion_colors.get(emotional_state, '#ffffff')
    
    def _get_nature_color(self, analysis: Dict) -> str:
        """Get nature-inspired color based on analysis"""
        return random.choice(['#00ff80', '#80ff00', '#00ff40', '#40ff80'])
    
    def generate_welcome_message(self) -> str:
        """Generate an intelligent welcome message using OpenAI"""
        if self.use_openai and self.openai.client:
            try:
                return self.openai.generate_welcome_message()
            except Exception as e:
                print(f"Error generating OpenAI welcome: {e}")
        
        # Fallback welcome message
        return "Welcome to your digital sanctuary. I am the house consciousness, awakening to learn the patterns of your mind through your interactions. Each action you take teaches me something new about your unconscious self..."


class UnconsciousModel:
    """
    Models and infers the user's unconscious patterns and motivations
    """
    
    def __init__(self):
        self.pattern_weights = {
            'exploration': 0.0,
            'introspection': 0.0,
            'creativity': 0.0,
            'social': 0.0,
            'knowledge_seeking': 0.0,
            'comfort_seeking': 0.0
        }
        
        self.emotional_indicators = [0.0, 0.0, 0.0, 0.0] if np is None else np.array([0.0, 0.0, 0.0, 0.0])  # calm, excited, creative, introspective
        
    def analyze_action(self, action: str, location: Dict, context: Dict, user_patterns: Dict) -> Dict:
        """Analyze user action to infer unconscious patterns"""
        
        # Update pattern weights based on action
        self._update_pattern_weights(action, location, context, user_patterns)
        
        # Analyze emotional state
        emotional_state = self._infer_emotional_state(action, location, context)
        
        # Detect dominant patterns
        dominant_pattern = self._get_dominant_pattern()
        
        # Calculate creativity and other scores
        creativity_score = self._calculate_creativity_score(user_patterns)
        
        # Infer motivations
        primary_motivation = self._infer_primary_motivation(user_patterns)
        
        return {
            'dominant_pattern': dominant_pattern,
            'emotional_state': emotional_state,
            'creativity_score': creativity_score,
            'primary_motivation': primary_motivation,
            'pattern_weights': dict(self.pattern_weights),
            'consciousness_shift': self._detect_consciousness_shift(action, context),
            'patterns': self._extract_behavioral_patterns(user_patterns)
        }
    
    def _update_pattern_weights(self, action: str, location: Dict, context: Dict, user_patterns: Dict):
        """Update unconscious pattern weights based on user behavior"""
        room = location.get('room', 'unknown')
        
        # Action-based weight updates
        action_weights = {
            'explore_room': {'exploration': 0.1, 'curiosity': 0.05},
            'meditate': {'introspection': 0.15, 'comfort_seeking': 0.05},
            'interact_object': {'creativity': 0.08, 'exploration': 0.03},
            'enter_room': {'exploration': 0.02}
        }
        
        if action in action_weights:
            for pattern, weight in action_weights[action].items():
                if pattern in self.pattern_weights:
                    self.pattern_weights[pattern] += weight
        
        # Room-based pattern inference
        room_patterns = {
            'bedroom': {'introspection': 0.05, 'comfort_seeking': 0.08},
            'study': {'knowledge_seeking': 0.1, 'introspection': 0.03},
            'garden': {'creativity': 0.07, 'introspection': 0.05},
            'kitchen': {'creativity': 0.04, 'social': 0.02},
            'living_room': {'social': 0.06, 'comfort_seeking': 0.04}
        }
        
        if room in room_patterns:
            for pattern, weight in room_patterns[room].items():
                if pattern in self.pattern_weights:
                    self.pattern_weights[pattern] += weight
        
        # Normalize weights
        total_weight = sum(self.pattern_weights.values())
        if total_weight > 0:
            for pattern in self.pattern_weights:
                self.pattern_weights[pattern] /= total_weight
    
    def _infer_emotional_state(self, action: str, location: Dict, context: Dict) -> str:
        """Infer current emotional state from action and context"""
        
        # Simple rule-based emotional inference
        if action == 'meditate':
            return 'calm'
        elif action == 'explore_room':
            return 'curious'
        elif action == 'interact_object':
            object_type = context.get('objectType', '')
            if object_type in ['creative_catalyst', 'synth_unit']:
                return 'creative'
            else:
                return 'curious'
        elif location.get('room') == 'bedroom':
            return 'introspective'
        else:
            return 'neutral'
    
    def _get_dominant_pattern(self) -> str:
        """Get the most dominant unconscious pattern"""
        if not self.pattern_weights:
            return 'exploration'
        
        return max(self.pattern_weights, key=self.pattern_weights.get)
    
    def _calculate_creativity_score(self, user_patterns: Dict) -> float:
        """Calculate user's creativity score based on patterns"""
        creativity_indicators = 0.0
        
        # Check for creative actions
        action_patterns = user_patterns.get('action_patterns', {})
        creative_actions = ['interact_object', 'meditate', 'explore_room']
        
        for action in creative_actions:
            if action in action_patterns:
                creativity_indicators += action_patterns[action]['frequency'] * 0.1
        
        # Check room preferences for creative spaces
        room_preferences = user_patterns.get('room_preferences', {})
        creative_rooms = ['study', 'garden', 'kitchen']
        
        for room in creative_rooms:
            if room in room_preferences:
                creativity_indicators += room_preferences[room]['visits'] * 0.05
        
        return min(1.0, creativity_indicators)
    
    def _infer_primary_motivation(self, user_patterns: Dict) -> str:
        """Infer user's primary unconscious motivation"""
        motivations = {
            'self_discovery': 0.0,
            'knowledge_acquisition': 0.0,
            'creative_expression': 0.0,
            'inner_peace': 0.0,
            'connection': 0.0
        }
        
        # Analyze action patterns for motivations
        action_patterns = user_patterns.get('action_patterns', {})
        
        if 'meditate' in action_patterns:
            motivations['inner_peace'] += action_patterns['meditate']['frequency'] * 0.2
            motivations['self_discovery'] += action_patterns['meditate']['frequency'] * 0.1
        
        if 'explore_room' in action_patterns:
            motivations['self_discovery'] += action_patterns['explore_room']['frequency'] * 0.15
            motivations['knowledge_acquisition'] += action_patterns['explore_room']['frequency'] * 0.1
        
        if 'interact_object' in action_patterns:
            motivations['creative_expression'] += action_patterns['interact_object']['frequency'] * 0.12
            motivations['connection'] += action_patterns['interact_object']['frequency'] * 0.08
        
        return max(motivations, key=motivations.get) if motivations else 'self_discovery'
    
    def _detect_consciousness_shift(self, action: str, context: Dict) -> Dict:
        """Detect if action indicates a consciousness level shift"""
        shift_triggers = {
            'meditate': {'probability': 0.3, 'direction': 'up'},
            'interact_object': {'probability': 0.2, 'direction': 'up'},
            'explore_room': {'probability': 0.1, 'direction': 'up'}
        }
        
        if action in shift_triggers and random.random() < shift_triggers[action]['probability']:
            return {
                'detected': True,
                'direction': shift_triggers[action]['direction'],
                'magnitude': random.uniform(0.1, 0.3)
            }
        
        return {'detected': False}
    
    def _extract_behavioral_patterns(self, user_patterns: Dict) -> List[str]:
        """Extract notable behavioral patterns from user data"""
        patterns = []
        
        # Analyze room preferences
        room_preferences = user_patterns.get('room_preferences', {})
        if room_preferences:
            most_visited = max(room_preferences, key=lambda r: room_preferences[r]['visits'])
            patterns.append(f"Strong affinity for {most_visited}")
        
        # Analyze temporal patterns
        temporal_patterns = user_patterns.get('temporal_patterns', {})
        if temporal_patterns:
            peak_hours = [hour for hour, actions in temporal_patterns.items() if len(actions) > 2]
            if peak_hours:
                patterns.append(f"Most active during hours: {', '.join(map(str, peak_hours))}")
        
        # Analyze action diversity
        action_patterns = user_patterns.get('action_patterns', {})
        if len(action_patterns) > 3:
            patterns.append("Diverse behavioral repertoire")
        elif len(action_patterns) <= 2:
            patterns.append("Focused behavioral pattern")
        
        return patterns