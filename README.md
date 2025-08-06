# The House of AI

A Python Flask web application featuring a 2D smart house simulation with AI-driven interactions. Users navigate a retrofuturist virtual house where an AI agent generates novel behaviors and modifications based on their actions, creating a personalized, evolving digital environment that reflects their unconscious patterns.

## Features

- **Real-time AI Communication**: WebSocket-based bidirectional communication with multiple AI providers
- **Configurable Room System**: JSON-based room variables and templates for easy customization
- **AI Pattern Recognition**: Analyzes user behavior to infer unconscious patterns and motivations
- **Dynamic House Evolution**: House architecture and objects evolve based on user interactions
- **Multi-Provider AI Support**: OpenAI, Anthropic, Groq, OpenRouter, and rule-based fallback
- **Model Selection Interface**: Easy switching between AI providers and models
- **Gamification**: Points, achievements, and consciousness levels provide progression feedback
- **Room Persistence**: SQLite database for storing rooms and configuration data

## Quick Start

### Prerequisites
- Python 3.7+
- Virtual environment (recommended)

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd the-house-of-ai

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
# Edit .env with your API keys (optional - works without API keys using rule-based fallback)
```

### Running the Application
```bash
# Start the Flask server
python app.py

# The app will be available at http://localhost:5001
```

## Room Configuration System

### Overview
The room logic has been abstracted into a configurable system using JSON files and database storage. This allows for easy modification of room variables, templates, and AI behavior without code changes.

### Configuration Files

#### `config/room_schema.json`
Defines all room variables with their types, ranges, and defaults:

```json
{
  "room_variables": {
    "sleep": {
      "type": "string",
      "format": "duration",
      "range": {"min": 3.0, "max": 9.0},
      "unit": "h",
      "default": "7.2h"
    },
    "skinTemp": {
      "type": "string",
      "format": "temperature", 
      "range": {"min": 32.0, "max": 37.0},
      "unit": "°C",
      "default": "36.1°C"
    },
    // ... more variables
  },
  "consciousness_templates": [...],
  "device_templates": [...],
  "sensor_types": [...]
}
```

#### `config/room_templates.json`
Defines room templates with different characteristics:

```json
{
  "templates": {
    "cyberpunk_standard": {
      "name": "Cyberpunk Standard Room",
      "variables": {
        "lights": ["neon", "holographic", "laser"],
        "sleep": {"min": 6.0, "max": 8.5},
        "heartRate": {"min": 60, "max": 85}
      },
      "devices": [
        {"template": "Neural Interface", "required": true},
        {"template": "Biometric Scanner", "required": true}
      ],
      "consciousness_style": "cyberpunk_tech"
    }
  }
}
```

### Room Variables

All room variables are now configurable through JSON:

| Variable | Description | Example Range | Unit |
|----------|-------------|---------------|------|
| `location` | Geographic location | Predefined cyberpunk cities | - |
| `sleep` | Sleep duration | 3.0 - 9.0 | hours |
| `skinTemp` | Skin temperature | 32.0 - 37.0 | °C |
| `heartRate` | Heart rate | 55 - 95 | bpm |
| `lights` | Lighting system | neon, holographic, laser, plasma | - |
| `roomTemp` | Room temperature | 18.0 - 26.0 | °C |
| `wifi` | Network devices | 1 - 5 | devices |
| `traffic` | Network activity | 10 - 500MB + activity type | MB |

### Room Templates

Three built-in templates with different characteristics:

#### **Cyberpunk Standard**
- Standard neural interface rooms
- Moderate biometric ranges
- Basic device set
- Cyberpunk tech consciousness style

#### **Neural Enhanced** 
- Advanced consciousness monitoring
- Higher biometric stability
- Enhanced device suite including dream synthesizers
- Enhanced awareness consciousness style

#### **Basic Digital**
- Entry-level digital accommodation
- Wider biometric ranges
- Minimal device set
- Basic digital consciousness style

### Database Storage

Room configuration is stored in SQLite tables:

```sql
-- Room variable definitions
room_variables (variable_name, variable_type, variable_config, timestamps)

-- Room template configurations  
room_templates (template_name, template_config, is_active, timestamps)

-- Generated room instances
hotel_rooms (room_id, room_data, timestamps)
```

## AI Provider System

### Supported Providers

- **OpenAI**: GPT-4 and GPT-3.5-turbo models
- **Anthropic**: Claude models (Claude-3-sonnet, etc.)
- **Groq**: Fast Llama models (llama-3.1-8b-instant)
- **OpenRouter**: Multi-model access
- **Rule-based**: Intelligent fallback system

### Model Selection Interface

#### Access Model Settings
- Click **"MODELS"** in the navigation bar
- Press **M** keyboard shortcut
- View current provider and available alternatives

#### Switch Models
1. Open model settings
2. Click any available provider
3. Instant switching with feedback
4. Automatic fallback if provider fails

#### API Endpoints
```bash
# Get available models and current selection
GET /api/models

# Switch to different provider/model
POST /api/models/switch
{
  "provider": "GROQ",
  "model": "llama-3.1-8b-instant"
}
```

## Performance Optimizations

### Room Generation Cache
- **Pre-generation**: 3 rooms cached for instant responses
- **Background Refill**: Automatic cache maintenance
- **15-second Timeout**: Prevents hanging requests
- **Fallback Layers**: Multiple fallback strategies

### Generation Flow
1. **Cache Hit**: Instant response (⚡ ~0ms)
2. **AI Generation**: Schema-aware generation (~2-10s)
3. **Config Fallback**: RoomConfigManager generation (~50ms)
4. **Ultimate Fallback**: Hardcoded basic room (~1ms)

## Development

### Architecture

```
├── app.py                 # Main Flask application with API endpoints
├── ai_agent.py           # AI behavior and room generation system
├── room_config.py        # Room configuration management
├── house_simulation.py   # Backend house state management
├── config/
│   ├── room_schema.json  # Room variable definitions
│   └── room_templates.json # Room template configurations
├── ai_providers/         # AI provider implementations
│   ├── openai_provider.py
│   ├── anthropic_provider.py
│   ├── groq_provider.py
│   └── provider_factory.py
├── templates/
│   └── hotel.html        # Main hotel interface
└── static/
    ├── css/style.css     # Retrofuturist styling
    └── js/hotel.js       # Hotel interface JavaScript
```

### Adding New Room Variables

1. **Edit Schema**: Add variable to `config/room_schema.json`
```json
"newVariable": {
  "type": "string",
  "range": {"min": 0, "max": 100},
  "unit": "units",
  "default": "50 units"
}
```

2. **Update Templates**: Add variable ranges to relevant templates in `config/room_templates.json`

3. **Restart Application**: Configuration is loaded on startup

### Adding New Room Templates

1. **Edit Templates**: Add new template to `config/room_templates.json`
```json
"my_custom_template": {
  "name": "My Custom Room Type",
  "description": "Custom room description",
  "variables": {
    "lights": ["custom_lights"],
    "heartRate": {"min": 70, "max": 90}
  },
  "devices": [
    {"template": "Neural Interface", "required": true}
  ],
  "consciousness_style": "custom_style"
}
```

2. **Add Consciousness Style**: Define consciousness text patterns for the template

3. **Restart Application**: Templates are loaded on startup

### Adding New AI Providers

1. **Create Provider Class**: Inherit from `AIProvider` base class
2. **Implement Required Methods**: `generate_response`, `generate_hotel_room`, etc.
3. **Register Provider**: Add to `provider_factory.py`
4. **Add Environment Variables**: Configure API keys in `.env`

## Interface Controls

### Keyboard Shortcuts
- **R**: Refresh rooms
- **N**: Generate new room  
- **C**: Clear all rooms
- **M**: Open model settings
- **ESC**: Close modal

### Navigation
- **REFRESH**: Update all room data
- **REQUEST NEW ROOM**: Generate additional room
- **CLEAR ROOMS**: Reset to single user room
- **MODELS**: Open AI model selection interface

### Room Interaction
- **Click Room**: Open detailed modal with consciousness stream
- **Inspect Devices**: View all connected IoT devices
- **View Floorplan**: Interactive sensor layout
- **Consciousness Stream**: AI-generated room awareness text

## Environment Variables

Create a `.env` file with your API keys (all optional):

```bash
# OpenAI (GPT models)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Anthropic (Claude models)  
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# Groq (Fast Llama models)
GROQ_API_KEY=gsk_your-groq-api-key-here

# OpenRouter (Multi-model access)
OPENROUTER_API_KEY=sk-or-your-openrouter-key-here

# Provider Selection (optional)
# DEFAULT_AI_PROVIDER=GROQ
```

**Note**: The application works without API keys using the intelligent rule-based fallback system.

## Troubleshooting

### Common Issues

1. **Module Import Errors**
   ```bash
   # Ensure virtual environment is activated
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Database Issues**  
   ```bash
   # Delete database to reset
   rm house_data.db
   # Restart application to recreate tables
   python app.py
   ```

3. **AI Provider Errors**
   - Check API keys in `.env` file
   - Verify API key format and validity
   - Use model settings to switch providers
   - Rule-based fallback always available

4. **Room Generation Slow**
   - Cache system provides instant responses after first generation
   - 15-second timeout prevents hanging
   - Multiple fallback layers ensure responses

### Development Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Update requirements
pip freeze > requirements.txt

# Run with debug mode
export FLASK_DEBUG=1
python app.py

# Check database contents
sqlite3 house_data.db ".tables"
sqlite3 house_data.db "SELECT * FROM room_templates;"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with different AI providers
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Flask and Socket.IO for real-time communication
- Supports multiple AI providers for diverse experiences  
- Retrofuturist cyberpunk aesthetic inspired by classic sci-fi
- Room configuration system designed for easy customization