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

# Set up request logging callback
def broadcast_request_log(log_entry):
    """Broadcast AI request logs to connected clients via WebSocket"""
    print(f"📡 Broadcasting AI request log: {log_entry.get('method', 'unknown')} - {log_entry.get('success', 'unknown')}")
    try:
        socketio.emit('ai_request_log', log_entry)
        print(f"✅ Successfully broadcast log to clients")
    except Exception as e:
        print(f"❌ Error broadcasting log: {e}")

ai_agent.ai_provider.set_request_log_callback(broadcast_request_log)

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
    c.execute('''CREATE TABLE IF NOT EXISTS hotel_rooms
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  room_id TEXT UNIQUE,
                  room_data TEXT,
                  created_timestamp TEXT,
                  updated_timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS room_variables
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  variable_name TEXT UNIQUE,
                  variable_type TEXT,
                  variable_config TEXT,
                  created_timestamp TEXT,
                  updated_timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS room_templates
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  template_name TEXT UNIQUE,
                  template_config TEXT,
                  is_active INTEGER DEFAULT 1,
                  created_timestamp TEXT,
                  updated_timestamp TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('hotel.html')


@app.route('/api/models')
def get_available_models():
    """Get available AI models and current selection"""
    try:
        current_provider_info = ai_agent.ai_provider.get_current_provider_info()
        available_providers = ai_agent.ai_provider.get_available_providers()
        
        # Add debug info
        print(f"🔍 Current provider: {current_provider_info['type']}")
        print(f"🔍 Provider available: {current_provider_info['available']}")
        current_provider = ai_agent.ai_provider.current_provider
        if hasattr(current_provider, 'api_key'):
            print(f"🔍 API key present: {'Yes' if current_provider.api_key else 'No'}")
        
        return jsonify({
            'current': {
                'provider': current_provider_info['type'],
                'model': getattr(ai_agent.ai_provider.current_provider, 'model', 'unknown'),
                'available': current_provider_info['available']
            },
            'providers': available_providers,
            'templates': ai_agent.room_config.get_available_templates()
        })
    except Exception as e:
        print(f"❌ Error getting model info: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/models/switch', methods=['POST'])
def switch_model():
    """Switch to a different AI provider/model"""
    try:
        data = request.get_json()
        provider_type = data.get('provider')
        model_name = data.get('model')
        
        if not provider_type:
            return jsonify({'error': 'Provider type required'}), 400
        
        success = ai_agent.ai_provider.switch_provider(provider_type, model=model_name)
        
        if success:
            current_info = ai_agent.ai_provider.get_current_provider_info()
            return jsonify({
                'success': True,
                'current': {
                    'provider': current_info['type'],
                    'model': getattr(ai_agent.ai_provider.current_provider, 'model', 'unknown'),
                    'available': current_info['available']
                }
            })
        else:
            return jsonify({'error': 'Failed to switch provider'}), 500
            
    except Exception as e:
        print(f"❌ Error switching model: {e}")
        return jsonify({'error': str(e)}), 500

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
    
    # Handle hotel-specific actions
    if context.get('interface_type') == 'hotel':
        handle_hotel_action(action, location, context)
        return
    
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

def handle_hotel_action(action, location, context):
    """Handle hotel interface specific actions"""
    print(f"🏨 Processing hotel action: {action}")
    
    if action == 'inspect_room':
        room_id = location.get('room_id')
        room_data = context.get('room_data', {})
        
        # Generate AI response for consciousness stream
        prompt_context = f"User is inspecting room {room_id}. Current consciousness: {room_data.get('consciousness', '')}"
        ai_response = ai_agent.generate_consciousness_stream(prompt_context, room_data)
        
        emit('ai_response', ai_response)
        
    elif action == 'generate_new_room':
        # Generate a new room directly (no threading to avoid SocketIO context issues)
        try:
            import time
            
            print(f"🏗️ Starting room generation for room #{context.get('current_room_count', 1)}")
            generation_start = time.time()
            
            try:
                print(f"🔄 Starting direct AI generation...")
                # Force AI generation to show requests in panel (not cached)
                new_room = ai_agent.generate_hotel_room(
                    context.get('current_room_count', 1), 
                    force_ai=True
                )
                print(f"✅ AI generation completed: {new_room.get('id', 'unknown') if new_room else 'no room'}")
                
            except Exception as e:
                print(f"❌ AI generation failed: {e}")
                new_room = ai_agent.generate_fallback_room(context.get('current_room_count', 1))
                print(f"🔄 Using fallback room: {new_room.get('id', 'unknown') if new_room else 'no room'}")
            
            generation_duration = time.time() - generation_start
            
            if not new_room:
                print(f"❌ No room generated, creating emergency fallback...")
                new_room = ai_agent.generate_fallback_room(context.get('current_room_count', 1))
            
            # Test emit first to ensure WebSocket is working
            print(f"🧪 Testing WebSocket emit...")
            socketio.emit('test_message', {'status': 'about_to_send_room'})
            
            print(f"📤 Emitting new_room_generated in {generation_duration:.1f}s: {new_room.get('id', 'unknown')}")
            socketio.emit('new_room_generated', {'room': new_room})
            print(f"✅ Room generation and emit complete")
            
        except Exception as e:
            print(f"Error in room generation: {e}")
            new_room = ai_agent.generate_fallback_room(context.get('current_room_count', 1))
            emit('new_room_generated', {'room': new_room})
        
    elif action == 'refresh_hotel':
        # Refresh all room data
        ai_response = ai_agent.generate_hotel_refresh()
        emit('ai_response', ai_response)
        
    elif action == 'save_rooms':
        # Save rooms to database
        rooms_data = context.get('rooms', [])
        save_hotel_rooms(rooms_data)
        
    elif action == 'load_rooms':
        # Load rooms from database
        rooms_data = load_hotel_rooms()
        emit('rooms_loaded', {'rooms': rooms_data})

def check_gamification(action, context=None):
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

def save_hotel_rooms(rooms_data):
    """Save hotel rooms to database"""
    conn = sqlite3.connect('house_data.db')
    c = conn.cursor()
    
    # Clear existing rooms
    c.execute("DELETE FROM hotel_rooms")
    
    # Save each room
    for room in rooms_data:
        c.execute("""INSERT OR REPLACE INTO hotel_rooms 
                     (room_id, room_data, created_timestamp, updated_timestamp) 
                     VALUES (?, ?, ?, ?)""",
                  (room.get('id'), json.dumps(room), 
                   datetime.now().isoformat(), datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    print(f"💾 Saved {len(rooms_data)} rooms to database")

def load_hotel_rooms():
    """Load hotel rooms from database"""
    conn = sqlite3.connect('house_data.db')
    c = conn.cursor()
    
    try:
        c.execute("SELECT room_data FROM hotel_rooms ORDER BY created_timestamp")
        rows = c.fetchall()
        
        rooms = []
        for row in rows:
            try:
                room_data = json.loads(row[0])
                rooms.append(room_data)
            except json.JSONDecodeError:
                continue
        
        conn.close()
        print(f"📥 Loaded {len(rooms)} rooms from database")
        return rooms
        
    except sqlite3.OperationalError:
        # Table doesn't exist yet
        conn.close()
        print("📥 No rooms found in database")
        return []

if __name__ == '__main__':
    init_db()
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)