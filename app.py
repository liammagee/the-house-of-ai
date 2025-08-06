from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import json
import sqlite3
import os
from datetime import datetime
import random
from dotenv import load_dotenv
from ai_agent import AIAgent
from house_simulation import HouseSimulation

# Load environment variables from .env file
load_dotenv()

# Debug environment loading
print("🔧 Flask App Initialization:")
print(f"   OPENAI_API_KEY present: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")
if os.getenv('OPENAI_API_KEY'):
    print(f"   OPENAI_API_KEY length: {len(os.getenv('OPENAI_API_KEY'))} characters")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize core systems
print("🧠 Initializing AI Agent...")
ai_agent = AIAgent()
print("🏠 Initializing House Simulation...")
house_sim = HouseSimulation()

# Database setup
def init_db():
    conn = sqlite3.connect('house_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_interactions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  action TEXT,
                  location TEXT,
                  context TEXT,
                  user_state TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS house_state
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  state_data TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    # Send initial house state
    emit('house_state', house_sim.get_state())

@socketio.on('get_welcome_message')
def handle_welcome_message():
    """Generate and send an intelligent welcome message"""
    try:
        print("🎬 Client requested welcome message")
        welcome_msg = ai_agent.generate_welcome_message()
        print(f"📤 Sending welcome message to client")
        emit('welcome_message', {'message': welcome_msg})
    except Exception as e:
        print(f"❌ Error generating welcome message: {e}")
        emit('welcome_message', {'message': 'Welcome to your digital sanctuary. I am learning about you...'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('user_action')
def handle_user_action(data):
    """Handle user interactions and generate AI responses"""
    action = data.get('action')
    location = data.get('location', {})
    context = data.get('context', {})
    
    print(f"🎮 User action received: {action}")
    print(f"   📍 Location: {location}")
    print(f"   🎯 Context keys: {list(context.keys())}")
    
    # Log interaction
    log_interaction(action, location, context)
    
    # Process with AI agent (this will trigger OpenAI if available)
    print(f"🧠 Processing with AI agent...")
    ai_response = ai_agent.process_action(action, location, context, house_sim.get_state())
    
    # Update house state based on AI response
    house_sim.update_from_ai_response(ai_response)
    
    print(f"📤 Sending AI response to client")
    print(f"   💬 Message preview: {ai_response.get('message', '')[:100]}...")
    
    # Emit updates to client
    emit('ai_response', ai_response)
    emit('house_state', house_sim.get_state())
    
    # Check for gamification updates
    gamification_update = check_gamification(action, context)
    if gamification_update:
        print(f"🎮 Sending gamification update: +{gamification_update.get('points', 0)} points")
        emit('gamification_update', gamification_update)

def log_interaction(action, location, context):
    """Log user interaction to database"""
    conn = sqlite3.connect('house_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO user_interactions (timestamp, action, location, context, user_state) VALUES (?, ?, ?, ?, ?)",
              (datetime.now().isoformat(), action, json.dumps(location), json.dumps(context), ""))
    conn.commit()
    conn.close()

def check_gamification(action, context):
    """Check if action triggers gamification elements"""
    # Simple gamification logic - expand based on requirements
    points = 0
    achievements = []
    
    if action == 'explore_room':
        points = 10
    elif action == 'interact_object':
        points = 15
    elif action == 'discover_secret':
        points = 50
        achievements.append("Explorer")
    
    return {
        'points': points,
        'achievements': achievements,
        'level_up': False  # Logic for level progression
    }

if __name__ == '__main__':
    init_db()
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)