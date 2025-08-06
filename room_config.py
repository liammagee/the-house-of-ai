"""
Room Configuration Manager for The House of AI
Handles room variables, templates, and generation logic
"""

import json
import random
import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class RoomConfigManager:
    """Manages room configuration, templates, and variable generation"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = config_dir
        self.schema = {}
        self.templates = {}
        self.db_path = 'house_data.db'
        
        self._load_configurations()
        self._init_database_configs()
    
    def _load_configurations(self):
        """Load JSON configuration files"""
        try:
            # Load room schema
            schema_path = os.path.join(self.config_dir, 'room_schema.json')
            if os.path.exists(schema_path):
                with open(schema_path, 'r') as f:
                    self.schema = json.load(f)
                print(f"✅ Loaded room schema with {len(self.schema.get('room_variables', {}))} variables")
            
            # Load room templates  
            templates_path = os.path.join(self.config_dir, 'room_templates.json')
            if os.path.exists(templates_path):
                with open(templates_path, 'r') as f:
                    self.templates = json.load(f)
                print(f"✅ Loaded {len(self.templates.get('templates', {}))} room templates")
                    
        except Exception as e:
            print(f"❌ Error loading configurations: {e}")
            self._create_fallback_config()
    
    def _create_fallback_config(self):
        """Create basic fallback configuration if files not found"""
        self.schema = {
            "room_variables": {
                "location": {"type": "string", "examples": ["Digital City"], "default": "Digital City"},
                "time": {"type": "string", "format": "time", "default": "auto"},
                "sleep": {"type": "string", "range": {"min": 6.0, "max": 8.0}, "unit": "h", "default": "7.0h"},
                "skinTemp": {"type": "string", "range": {"min": 35.0, "max": 37.0}, "unit": "°C", "default": "36.0°C"},
                "heartRate": {"type": "string", "range": {"min": 60, "max": 90}, "unit": " bpm", "default": "72 bpm"},
                "lights": {"type": "string", "options": ["neon", "ambient"], "default": "neon"},
                "roomTemp": {"type": "string", "range": {"min": 20.0, "max": 24.0}, "unit": "°C", "default": "22.0°C"},
                "wifi": {"type": "string", "range": {"min": 1, "max": 5}, "unit": " devices", "default": "2 devices"},
                "traffic": {"type": "string", "default": "100MB (idle)"}
            },
            "consciousness_templates": ["Basic digital consciousness stream..."],
            "device_templates": [
                {"name": "Neural Interface", "status_options": ["Active"], "locations": ["Desk"]}
            ]
        }
        self.templates = {
            "templates": {
                "basic": {
                    "name": "Basic Room",
                    "variables": {},
                    "devices": [{"template": "Neural Interface", "required": True}]
                }
            }
        }
        print("🔧 Using fallback configuration")
    
    def _init_database_configs(self):
        """Initialize database with configuration data"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            # Store room variables in database
            for var_name, var_config in self.schema.get('room_variables', {}).items():
                c.execute("""INSERT OR REPLACE INTO room_variables 
                            (variable_name, variable_type, variable_config, created_timestamp, updated_timestamp) 
                            VALUES (?, ?, ?, ?, ?)""",
                         (var_name, var_config.get('type', 'string'), 
                          json.dumps(var_config), datetime.now().isoformat(), datetime.now().isoformat()))
            
            # Store room templates in database
            for template_name, template_config in self.templates.get('templates', {}).items():
                c.execute("""INSERT OR REPLACE INTO room_templates 
                            (template_name, template_config, is_active, created_timestamp, updated_timestamp) 
                            VALUES (?, ?, ?, ?, ?)""",
                         (template_name, json.dumps(template_config), 1, 
                          datetime.now().isoformat(), datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            print("💾 Room configurations stored in database")
            
        except Exception as e:
            print(f"❌ Error storing configurations in database: {e}")
    
    def generate_room_variables(self, template_name: str = "cyberpunk_standard") -> Dict[str, Any]:
        """Generate room variables based on template and schema"""
        template = self.templates.get('templates', {}).get(template_name, {})
        variables = {}
        
        # Generate each variable according to schema
        for var_name, var_schema in self.schema.get('room_variables', {}).items():
            variables[var_name] = self._generate_variable_value(var_name, var_schema, template)
        
        return variables
    
    def _generate_variable_value(self, var_name: str, var_schema: Dict, template: Dict) -> str:
        """Generate a single variable value based on schema and template"""
        var_type = var_schema.get('type', 'string')
        template_vars = template.get('variables', {})
        
        # Check for template override
        if var_name in template_vars:
            template_config = template_vars[var_name]
            
            # Handle template ranges
            if isinstance(template_config, dict) and 'min' in template_config and 'max' in template_config:
                min_val = template_config['min']
                max_val = template_config['max']
                
                if var_schema.get('format') == 'temperature':
                    value = round(random.uniform(min_val, max_val), 1)
                    return f"{value}{var_schema.get('unit', '')}"
                elif var_name == 'heartRate':
                    value = random.randint(int(min_val), int(max_val))
                    return f"{value}{var_schema.get('unit', '')}"
                elif var_name == 'sleep':
                    value = round(random.uniform(min_val, max_val), 1)
                    return f"{value}{var_schema.get('unit', '')}"
                elif var_name == 'wifi':
                    value = random.randint(int(min_val), int(max_val))
                    return f"{value}{var_schema.get('unit', '')}"
                elif var_name == 'traffic':
                    data_amount = random.randint(int(min_val), int(max_val))
                    activities = var_schema.get('activities', ['data-streaming'])
                    activity = random.choice(activities)
                    return f"{data_amount}MB ({activity})"
            
            # Handle template lists (for options like lights)
            elif isinstance(template_config, list):
                return random.choice(template_config)
        
        # Use schema defaults and generation
        if var_name == 'location':
            examples = var_schema.get('examples', ['Digital City'])
            return random.choice(examples)
        
        elif var_name == 'time':
            return datetime.now().strftime('%H:%M')
        
        elif var_name == 'lights':
            options = var_schema.get('options', ['neon'])
            return random.choice(options)
        
        elif 'range' in var_schema:
            min_val = var_schema['range']['min']
            max_val = var_schema['range']['max']
            unit = var_schema.get('unit', '')
            
            if var_schema.get('format') == 'temperature':
                value = round(random.uniform(min_val, max_val), 1)
                return f"{value}{unit}"
            elif var_name in ['heartRate', 'wifi']:
                value = random.randint(int(min_val), int(max_val))
                return f"{value}{unit}"
            elif var_name == 'sleep':
                value = round(random.uniform(min_val, max_val), 1)
                return f"{value}{unit}"
            elif var_name == 'traffic':
                data_amount = random.randint(int(min_val), int(max_val))
                activities = var_schema.get('activities', ['idle'])
                activity = random.choice(activities)
                return f"{data_amount}MB ({activity})"
        
        # Fallback to default
        return var_schema.get('default', 'N/A')
    
    def generate_consciousness_stream(self, template_name: str = "cyberpunk_standard") -> str:
        """Generate consciousness stream text based on template style"""
        template = self.templates.get('templates', {}).get(template_name, {})
        style = template.get('consciousness_style', 'cyberpunk_tech')
        
        consciousness_styles = self.templates.get('consciousness_styles', {})
        style_templates = consciousness_styles.get(style, self.schema.get('consciousness_templates', []))
        
        if style_templates:
            return random.choice(style_templates)
        
        return "Digital consciousness flows through neural pathways, learning and adapting..."
    
    def generate_devices(self, template_name: str = "cyberpunk_standard") -> List[Dict]:
        """Generate device list based on template"""
        template = self.templates.get('templates', {}).get(template_name, {})
        template_devices = template.get('devices', [])
        device_templates = self.schema.get('device_templates', [])
        
        devices = []
        
        for template_device in template_devices:
            device_template_name = template_device.get('template')
            
            # Find matching device template
            device_template = next(
                (dt for dt in device_templates if dt['name'] == device_template_name),
                None
            )
            
            if device_template:
                device = {
                    'name': device_template['name'],
                    'status': random.choice(device_template.get('status_options', ['Active'])),
                    'location': random.choice(device_template.get('locations', ['Room']))
                }
                devices.append(device)
        
        return devices
    
    def generate_floorplan(self) -> Dict:
        """Generate floorplan with sensors"""
        sensor_types = self.schema.get('sensor_types', ['AI_NODE'])
        room_sections = self.schema.get('room_sections', ['living'])
        positions = self.schema.get('floorplan_positions', {'min_x': 20, 'max_x': 80, 'min_y': 20, 'max_y': 80})
        
        sensors = []
        num_sensors = random.randint(3, 6)
        
        for _ in range(num_sensors):
            sensor = {
                'name': random.choice(sensor_types),
                'x': f"{random.randint(positions['min_x'], positions['max_x'])}%",
                'y': f"{random.randint(positions['min_y'], positions['max_y'])}%", 
                'room': random.choice(room_sections)
            }
            sensors.append(sensor)
        
        return {'sensors': sensors}
    
    def generate_complete_room(self, room_count: int, template_name: str = "cyberpunk_standard") -> Dict:
        """Generate a complete room with all components"""
        room_id = f"ROOM_{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')}{random.randint(100, 999)}"
        
        # Generate all room components
        variables = self.generate_room_variables(template_name)
        consciousness = self.generate_consciousness_stream(template_name)
        devices = self.generate_devices(template_name)
        floorplan = self.generate_floorplan()
        
        return {
            'id': room_id,
            **variables,  # Unpack all generated variables
            'consciousness': consciousness,
            'devices': devices,
            'floorplan': floorplan
        }
    
    def get_available_templates(self) -> List[str]:
        """Get list of available room templates"""
        return list(self.templates.get('templates', {}).keys())
    
    def get_template_info(self, template_name: str) -> Dict:
        """Get detailed information about a template"""
        return self.templates.get('templates', {}).get(template_name, {})
    
    def load_templates_from_db(self) -> Dict:
        """Load active templates from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT template_name, template_config FROM room_templates WHERE is_active = 1")
            rows = c.fetchall()
            
            templates = {}
            for row in rows:
                template_name, template_config = row
                templates[template_name] = json.loads(template_config)
            
            conn.close()
            return {'templates': templates}
            
        except Exception as e:
            print(f"❌ Error loading templates from database: {e}")
            return self.templates
    
    def update_template_in_db(self, template_name: str, template_config: Dict):
        """Update or create template in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""INSERT OR REPLACE INTO room_templates 
                        (template_name, template_config, is_active, created_timestamp, updated_timestamp) 
                        VALUES (?, ?, ?, ?, ?)""",
                     (template_name, json.dumps(template_config), 1,
                      datetime.now().isoformat(), datetime.now().isoformat()))
            conn.commit()
            conn.close()
            print(f"💾 Template '{template_name}' updated in database")
            
        except Exception as e:
            print(f"❌ Error updating template in database: {e}")