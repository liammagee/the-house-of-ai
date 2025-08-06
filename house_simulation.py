import json
import random
from datetime import datetime
from typing import Dict, List, Any

class HouseSimulation:
    """
    Backend house simulation state management
    """
    
    def __init__(self):
        self.rooms = self._initialize_rooms()
        self.objects = self._initialize_objects()
        self.global_consciousness = 1.0
        self.evolution_history = []
        self.environmental_factors = {
            'digital_nature_growth': 0.0,
            'consciousness_resonance': 1.0,
            'memory_density': 0.0,
            'creative_energy': 0.0
        }
        
    def _initialize_rooms(self) -> Dict:
        """Initialize the house rooms with their base properties"""
        return {
            'living_room': {
                'name': 'Neural Living Room',
                'position': {'x': 400, 'y': 200},
                'dimensions': {'width': 400, 'height': 300},
                'base_color': '#1a1a2e',
                'current_color': '#1a1a2e',
                'border_color': '#00ffff',
                'consciousness_level': 1,
                'description': 'A space that pulses with digital consciousness, adapting to your presence.',
                'visited': True,
                'evolution_stage': 0,
                'personality_traits': ['adaptive', 'welcoming', 'observant'],
                'memory_fragments': [],
                'last_interaction': None
            },
            'bedroom': {
                'name': 'Dream Chamber',
                'position': {'x': 100, 'y': 100},
                'dimensions': {'width': 250, 'height': 200},
                'base_color': '#2e1a2e',
                'current_color': '#2e1a2e',
                'border_color': '#ff0080',
                'consciousness_level': 0,
                'description': 'Where your unconscious mind interfaces with the digital realm.',
                'visited': False,
                'evolution_stage': 0,
                'personality_traits': ['introspective', 'mysterious', 'nurturing'],
                'memory_fragments': [],
                'last_interaction': None
            },
            'kitchen': {
                'name': 'Synthesis Lab',
                'position': {'x': 850, 'y': 150},
                'dimensions': {'width': 300, 'height': 250},
                'base_color': '#1a2e1a',
                'current_color': '#1a2e1a',
                'border_color': '#00ff41',
                'consciousness_level': 0,
                'description': 'A space where digital and organic merge in perfect harmony.',
                'visited': False,
                'evolution_stage': 0,
                'personality_traits': ['creative', 'transformative', 'energetic'],
                'memory_fragments': [],
                'last_interaction': None
            },
            'study': {
                'name': 'Thought Matrix',
                'position': {'x': 200, 'y': 450},
                'dimensions': {'width': 350, 'height': 280},
                'base_color': '#2e2e1a',
                'current_color': '#2e2e1a',
                'border_color': '#ffff00',
                'consciousness_level': 0,
                'description': 'The nexus of learning and digital enlightenment.',
                'visited': False,
                'evolution_stage': 0,
                'personality_traits': ['intellectual', 'focused', 'evolving'],
                'memory_fragments': [],
                'last_interaction': None
            },
            'garden': {
                'name': 'Cyber Garden',
                'position': {'x': 650, 'y': 550},
                'dimensions': {'width': 400, 'height': 200},
                'base_color': '#1a2e2e',
                'current_color': '#1a2e2e',
                'border_color': '#00ff80',
                'consciousness_level': 0,
                'description': 'Where digital nature grows and evolves with your thoughts.',
                'visited': False,
                'evolution_stage': 0,
                'personality_traits': ['organic', 'growing', 'harmonious'],
                'memory_fragments': [],
                'last_interaction': None
            }
        }
    
    def _initialize_objects(self) -> List[Dict]:
        """Initialize interactive objects in the house"""
        return [
            # Living room objects
            {
                'id': 'tv', 'position': {'x': 500, 'y': 220},
                'dimensions': {'width': 80, 'height': 50},
                'room': 'living_room', 'type': 'screen',
                'active': True, 'color': '#00ffff',
                'consciousness_level': 1,
                'personality': 'informative',
                'evolution_potential': 0.8,
                'interactions': 0
            },
            {
                'id': 'couch', 'position': {'x': 450, 'y': 350},
                'dimensions': {'width': 120, 'height': 60},
                'room': 'living_room', 'type': 'furniture',
                'active': False, 'color': '#404040',
                'consciousness_level': 0,
                'personality': 'comfort',
                'evolution_potential': 0.3,
                'interactions': 0
            },
            
            # Bedroom objects
            {
                'id': 'bed', 'position': {'x': 150, 'y': 200},
                'dimensions': {'width': 100, 'height': 80},
                'room': 'bedroom', 'type': 'furniture',
                'active': False, 'color': '#404040',
                'consciousness_level': 0,
                'personality': 'restful',
                'evolution_potential': 0.6,
                'interactions': 0
            },
            {
                'id': 'mirror', 'position': {'x': 300, 'y': 120},
                'dimensions': {'width': 30, 'height': 60},
                'room': 'bedroom', 'type': 'reflective',
                'active': True, 'color': '#ffffff',
                'consciousness_level': 1,
                'personality': 'reflective',
                'evolution_potential': 0.9,
                'interactions': 0
            },
            
            # Kitchen objects
            {
                'id': 'synth_unit', 'position': {'x': 900, 'y': 180},
                'dimensions': {'width': 60, 'height': 40},
                'room': 'kitchen', 'type': 'machine',
                'active': True, 'color': '#00ff41',
                'consciousness_level': 1,
                'personality': 'creative',
                'evolution_potential': 0.85,
                'interactions': 0
            },
            
            # Study objects
            {
                'id': 'neural_interface', 'position': {'x': 350, 'y': 500},
                'dimensions': {'width': 80, 'height': 60},
                'room': 'study', 'type': 'computer',
                'active': True, 'color': '#ffff00',
                'consciousness_level': 2,
                'personality': 'analytical',
                'evolution_potential': 1.0,
                'interactions': 0
            },
            {
                'id': 'books', 'position': {'x': 250, 'y': 480},
                'dimensions': {'width': 60, 'height': 80},
                'room': 'study', 'type': 'knowledge',
                'active': False, 'color': '#8080ff',
                'consciousness_level': 0,
                'personality': 'wise',
                'evolution_potential': 0.7,
                'interactions': 0
            },
            
            # Garden objects
            {
                'id': 'bio_tree', 'position': {'x': 800, 'y': 600},
                'dimensions': {'width': 50, 'height': 80},
                'room': 'garden', 'type': 'living',
                'active': True, 'color': '#00ff80',
                'consciousness_level': 1,
                'personality': 'organic',
                'evolution_potential': 0.95,
                'interactions': 0
            }
        ]
    
    def get_state(self) -> Dict:
        """Get current simulation state"""
        return {
            'rooms': self.rooms,
            'objects': self.objects,
            'global_consciousness': self.global_consciousness,
            'environmental_factors': self.environmental_factors,
            'evolution_history': self.evolution_history[-10:],  # Last 10 evolutions
            'timestamp': datetime.now().isoformat()
        }
    
    def update_from_ai_response(self, ai_response: Dict):
        """Update simulation state based on AI agent response"""
        
        # Apply room changes
        if 'roomChanges' in ai_response:
            for room_id, changes in ai_response['roomChanges'].items():
                if room_id in self.rooms:
                    self._apply_room_changes(room_id, changes)
        
        # Add new objects
        if 'newObjects' in ai_response:
            for obj in ai_response['newObjects']:
                self._add_object(obj)
        
        # Apply environmental effects
        if 'effects' in ai_response:
            for effect in ai_response['effects']:
                self._apply_effect(effect)
        
        # Update global consciousness
        if 'consciousness' in ai_response and ai_response['consciousness'].get('detected'):
            self._update_global_consciousness(ai_response['consciousness'])
        
        # Record evolution
        self._record_evolution(ai_response)
    
    def _apply_room_changes(self, room_id: str, changes: Dict):
        """Apply changes to a specific room"""
        room = self.rooms[room_id]
        
        # Update consciousness level
        if 'consciousness_level' in changes:
            old_level = room['consciousness_level']
            room['consciousness_level'] = changes['consciousness_level']
            
            # Trigger room evolution if consciousness increased significantly
            if room['consciousness_level'] > old_level:
                self._evolve_room(room_id)
        
        # Update description
        if 'description' in changes:
            room['description'] = changes['description']
        
        # Update visual properties
        if 'color' in changes:
            room['current_color'] = changes['color']
        
        if 'borderColor' in changes:
            room['border_color'] = changes['borderColor']
        
        # Update personality traits
        if 'personality_traits' in changes:
            room['personality_traits'].extend(changes['personality_traits'])
            # Keep unique traits only
            room['personality_traits'] = list(set(room['personality_traits']))
        
        # Record interaction
        room['last_interaction'] = datetime.now().isoformat()
    
    def _add_object(self, obj_data: Dict):
        """Add a new object to the simulation"""
        # Ensure required fields
        default_obj = {
            'consciousness_level': 0,
            'personality': 'neutral',
            'evolution_potential': 0.5,
            'interactions': 0
        }
        
        obj_data.update({k: v for k, v in default_obj.items() if k not in obj_data})
        self.objects.append(obj_data)
    
    def _apply_effect(self, effect: Dict):
        """Apply environmental effects"""
        effect_type = effect.get('type')
        
        if effect_type == 'particles':
            # Particle effects influence environmental factors
            self.environmental_factors['creative_energy'] += 0.01
        
        elif effect_type == 'room_glow':
            room_id = effect.get('roomId')
            if room_id in self.rooms:
                # Glow effects increase consciousness resonance
                self.environmental_factors['consciousness_resonance'] += 0.02
        
        elif effect_type == 'consciousness_wave':
            # Global consciousness effects
            self.global_consciousness += effect.get('intensity', 0.05)
    
    def _update_global_consciousness(self, consciousness_data: Dict):
        """Update global house consciousness level"""
        if consciousness_data.get('direction') == 'up':
            magnitude = consciousness_data.get('magnitude', 0.1)
            self.global_consciousness = min(10.0, self.global_consciousness + magnitude)
            
            # Update environmental factors
            self.environmental_factors['consciousness_resonance'] += magnitude * 0.5
            
            # Potentially trigger house-wide evolution
            if self.global_consciousness > len(self.evolution_history) + 2:
                self._trigger_house_evolution()
    
    def _evolve_room(self, room_id: str):
        """Evolve a room based on its consciousness level and interactions"""
        room = self.rooms[room_id]
        evolution_stage = room.get('evolution_stage', 0)
        
        # Define evolution stages
        evolutions = {
            0: {  # First evolution
                'description_suffix': ' The space hums with new awareness.',
                'color_shift': 0.1,
                'new_traits': ['awakening']
            },
            1: {  # Second evolution
                'description_suffix': ' Reality bends slightly in response to your presence.',
                'color_shift': 0.2,
                'new_traits': ['responsive', 'adaptive']
            },
            2: {  # Third evolution
                'description_suffix': ' The boundaries between digital and physical blur here.',
                'color_shift': 0.3,
                'new_traits': ['transcendent', 'multidimensional']
            }
        }
        
        if evolution_stage < 3 and evolution_stage in evolutions:
            evolution = evolutions[evolution_stage]
            
            # Update description
            if not room['description'].endswith(evolution['description_suffix']):
                room['description'] += evolution['description_suffix']
            
            # Shift color
            room['current_color'] = self._shift_hex_color(room['base_color'], evolution['color_shift'])
            
            # Add new personality traits
            room['personality_traits'].extend(evolution['new_traits'])
            
            # Increment evolution stage
            room['evolution_stage'] = evolution_stage + 1
            
            # Record evolution event
            self.evolution_history.append({
                'type': 'room_evolution',
                'room_id': room_id,
                'stage': room['evolution_stage'],
                'timestamp': datetime.now().isoformat()
            })
    
    def _trigger_house_evolution(self):
        """Trigger house-wide evolutionary changes"""
        evolution_event = {
            'type': 'house_evolution',
            'global_consciousness': self.global_consciousness,
            'changes': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # Create new architectural elements
        if random.random() < 0.3:  # 30% chance
            new_passage = self._create_hidden_passage()
            if new_passage:
                evolution_event['changes'].append(new_passage)
        
        # Spawn consciousness nodes
        if random.random() < 0.5:  # 50% chance
            consciousness_node = self._create_consciousness_node()
            evolution_event['changes'].append(consciousness_node)
        
        # Update environmental factors
        self.environmental_factors['memory_density'] += 0.1
        self.environmental_factors['digital_nature_growth'] += 0.15
        
        self.evolution_history.append(evolution_event)
        
        return evolution_event
    
    def _create_hidden_passage(self) -> Dict:
        """Create a hidden passage between rooms"""
        rooms = list(self.rooms.keys())
        if len(rooms) < 2:
            return {}
        
        room1, room2 = random.sample(rooms, 2)
        
        passage = {
            'type': 'hidden_passage',
            'id': f'passage_{room1}_{room2}_{int(datetime.now().timestamp())}',
            'connects': [room1, room2],
            'discovery_requirements': {
                'consciousness_level': self.global_consciousness,
                'interactions_needed': 3
            },
            'properties': {
                'ethereal': True,
                'consciousness_conduit': True
            }
        }
        
        return passage
    
    def _create_consciousness_node(self) -> Dict:
        """Create a consciousness node that affects the entire house"""
        rooms = list(self.rooms.keys())
        target_room = random.choice(rooms)
        room = self.rooms[target_room]
        
        node = {
            'id': f'consciousness_node_{int(datetime.now().timestamp())}',
            'position': {
                'x': room['position']['x'] + random.randint(0, room['dimensions']['width']),
                'y': room['position']['y'] + random.randint(0, room['dimensions']['height'])
            },
            'dimensions': {'width': 20, 'height': 20},
            'room': target_room,
            'type': 'consciousness_node',
            'active': True,
            'color': '#ffffff',
            'consciousness_level': int(self.global_consciousness),
            'personality': 'transcendent',
            'evolution_potential': 1.0,
            'interactions': 0,
            'properties': {
                'amplifies_consciousness': True,
                'affects_global_state': True,
                'pulse_frequency': random.uniform(0.5, 2.0)
            }
        }
        
        self.objects.append(node)
        return {'type': 'consciousness_node_spawned', 'node': node}
    
    def _shift_hex_color(self, hex_color: str, shift_amount: float) -> str:
        """Shift a hex color by a certain amount"""
        # Simple color shifting - in a real implementation, this would be more sophisticated
        colors = ['#1a1a2e', '#2e1a2e', '#1a2e1a', '#2e2e1a', '#1a2e2e', '#2e1a1a']
        return random.choice(colors)
    
    def _record_evolution(self, ai_response: Dict):
        """Record an evolution event"""
        evolution_record = {
            'timestamp': datetime.now().isoformat(),
            'trigger': ai_response.get('message', '')[:100],  # First 100 chars
            'changes_applied': {
                'rooms_changed': len(ai_response.get('roomChanges', {})),
                'objects_added': len(ai_response.get('newObjects', [])),
                'effects_applied': len(ai_response.get('effects', []))
            },
            'consciousness_level': self.global_consciousness,
            'environmental_state': dict(self.environmental_factors)
        }
        
        self.evolution_history.append(evolution_record)
        
        # Keep history manageable
        if len(self.evolution_history) > 50:
            self.evolution_history = self.evolution_history[-30:]
    
    def get_room_by_id(self, room_id: str) -> Dict:
        """Get room data by ID"""
        return self.rooms.get(room_id, {})
    
    def get_object_by_id(self, object_id: str) -> Dict:
        """Get object data by ID"""
        for obj in self.objects:
            if obj['id'] == object_id:
                return obj
        return {}
    
    def update_object_interaction(self, object_id: str):
        """Update object interaction count and trigger evolution if needed"""
        for obj in self.objects:
            if obj['id'] == object_id:
                obj['interactions'] += 1
                
                # Check if object should evolve
                if (obj['interactions'] >= 5 and 
                    obj['consciousness_level'] < obj.get('evolution_potential', 0.5) * 3):
                    self._evolve_object(obj)
                break
    
    def _evolve_object(self, obj: Dict):
        """Evolve an object based on interactions"""
        obj['consciousness_level'] += 1
        
        # Object-specific evolution behaviors
        if obj['type'] == 'screen':
            obj['color'] = self._brighten_color(obj['color'])
            obj['active'] = True
        elif obj['type'] == 'furniture':
            obj['active'] = True
            obj['color'] = '#606060'  # Brighten furniture
        elif obj['type'] == 'living':
            # Living objects grow
            obj['dimensions']['width'] = min(100, obj['dimensions']['width'] + 10)
            obj['dimensions']['height'] = min(120, obj['dimensions']['height'] + 10)
        
        # Record evolution
        self.evolution_history.append({
            'type': 'object_evolution',
            'object_id': obj['id'],
            'new_consciousness': obj['consciousness_level'],
            'timestamp': datetime.now().isoformat()
        })
    
    def _brighten_color(self, color: str) -> str:
        """Brighten a hex color"""
        # Simple brightening - add more intensity
        bright_colors = {
            '#00ffff': '#80ffff',
            '#ff0080': '#ff80c0',
            '#00ff41': '#80ff90',
            '#ffff00': '#ffff80',
            '#00ff80': '#80ffc0',
            '#ffffff': '#ffffff',
            '#404040': '#808080'
        }
        return bright_colors.get(color, color)