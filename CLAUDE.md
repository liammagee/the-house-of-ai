# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

"The House of AI" is a Python Flask web application featuring a 2D smart house simulation with AI-driven interactions. Users navigate a retrofuturist virtual house where an AI agent generates novel behaviors and modifications based on their actions, creating a personalized, evolving digital environment that reflects their unconscious patterns.

## Development Setup

### Prerequisites
- Python 3.7+
- Virtual environment (recommended)

### Installation
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
# Edit .env with your OpenAI API key:
# OPENAI_API_KEY=sk-your-openai-api-key-here
```

### OpenAI Integration
The application now uses **OpenAI GPT-4** for intelligent AI responses:
- **With API Key**: Get sophisticated, contextual responses that analyze user behavior patterns
- **Without API Key**: Falls back to rule-based responses (still functional)
- **Setup**: Add your OpenAI API key to `.env` file for best experience

### Running the Application
```bash
# Start the Flask server
python app.py

# The app will be available at http://localhost:5000
```

### Development Commands
- `python app.py` - Start the development server
- `pip install -r requirements.txt` - Install/update dependencies
- `pip freeze > requirements.txt` - Update requirements file

## Architecture

### Backend Components
- **Flask Application** (`app.py`) - Main server with WebSocket support for real-time communication
- **AI Agent** (`ai_agent.py`) - Core AI system that analyzes user patterns and generates behaviors
- **House Simulation** (`house_simulation.py`) - Backend state management for the virtual house
- **Database** (`house_data.db`) - SQLite database storing user interactions and house state

### Frontend Components
- **HTML/CSS** - Retrofuturist UI with neon colors and cyber aesthetics
- **Canvas Simulation** (`house-simulation.js`) - 2D rendering and user interaction handling
- **Game Logic** (`game.js`) - Gamification, achievements, and visual effects
- **App Controller** (`app.js`) - WebSocket communication and UI state management

### Key Features
- **Real-time Communication**: WebSocket-based bidirectional communication between frontend and backend
- **AI Pattern Recognition**: Analyzes user behavior to infer unconscious patterns and motivations
- **Dynamic House Evolution**: House architecture and objects evolve based on user interactions
- **Gamification**: Points, achievements, and consciousness levels provide progression feedback
- **Unconscious Modeling**: AI agent builds a model of user's unconscious desires and adapts accordingly

### Room System
Each room has:
- Consciousness levels that evolve with interaction
- Personality traits that influence AI responses
- Interactive objects with their own evolution potential
- Visual effects that respond to user patterns

### AI Agent Behavior
- **Pattern Analysis**: Tracks room preferences, action frequencies, and temporal patterns
- **Unconscious Inference**: Models user's hidden motivations and emotional states
- **Dynamic Response Generation**: Creates contextual messages and house modifications
- **Consciousness Expansion**: Triggers house-wide evolutionary changes based on user growth

### WebSocket Events
- `user_action` - User interactions sent to backend
- `ai_response` - AI-generated responses and house changes
- `house_state` - Complete house state updates
- `gamification_update` - Points, achievements, and level changes

## File Structure
```
├── app.py                 # Main Flask application
├── ai_agent.py           # AI behavior generation system
├── house_simulation.py   # Backend house state management
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html       # Main application template
└── static/
    ├── css/
    │   └── style.css    # Retrofuturist styling
    └── js/
        ├── app.js       # Main application controller
        ├── house-simulation.js  # 2D canvas simulation
        └── game.js      # Game mechanics and utilities
```

## Development Notes
- The house evolves based on user patterns - rooms gain consciousness and objects transform
- All interactions are logged to SQLite for pattern analysis
- Visual effects use HTML5 Canvas with WebGL-style shaders for cyberpunk aesthetic
- AI responses are generated using rule-based pattern matching with potential for LLM integration
- Gamification elements encourage exploration and deeper engagement with the house