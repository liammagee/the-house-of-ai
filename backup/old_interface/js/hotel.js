// Hotel interface WebSocket and UI management
class HotelInterface {
    constructor() {
        this.socket = null;
        this.rooms = [];
        this.userRoomId = 'ROOM_USER';
        this.currentModal = null;
        this.connectionRetries = 0;
        this.maxRetries = 5;
        
        this.init();
    }

    init() {
        this.connectWebSocket();
        this.bindEventListeners();
        this.generateInitialRoom();
        this.startPeriodicUpdates();
    }

    connectWebSocket() {
        console.log('🔌 Connecting to WebSocket...');
        this.socket = io();
        
        this.socket.on('connect', () => {
            console.log('✅ Connected to server');
            this.updateConnectionStatus('Connected', 'ACTIVE');
            this.connectionRetries = 0;
            
            // Request initial AI-generated room
            this.requestAIRoomGeneration();
        });

        this.socket.on('disconnect', () => {
            console.log('❌ Disconnected from server');
            this.updateConnectionStatus('Disconnected', 'DISCONNECTED');
        });

        this.socket.on('connect_error', () => {
            console.log('⚠️ Connection error');
            this.handleConnectionError();
        });

        // Listen for AI responses that can update consciousness streams
        this.socket.on('ai_response', (data) => {
            this.handleAIResponse(data);
        });

        // Listen for room updates
        this.socket.on('room_update', (data) => {
            this.handleRoomUpdate(data);
        });

        // Listen for new room generation
        this.socket.on('new_room_generated', (data) => {
            this.handleNewRoomGenerated(data);
        });
    }

    updateConnectionStatus(status, aiStatus) {
        const statusEl = document.getElementById('connectionStatus');
        const aiStatusEl = document.getElementById('aiStatus');
        
        statusEl.textContent = status;
        aiStatusEl.textContent = aiStatus;
        
        // Update CSS classes
        aiStatusEl.className = `ai-status ${aiStatus.toLowerCase()}`;
    }

    handleConnectionError() {
        this.connectionRetries++;
        if (this.connectionRetries < this.maxRetries) {
            console.log(`🔄 Retrying connection (${this.connectionRetries}/${this.maxRetries})...`);
            setTimeout(() => this.connectWebSocket(), 2000 * this.connectionRetries);
        } else {
            this.updateConnectionStatus('Failed', 'ERROR');
        }
    }

    generateInitialRoom() {
        // Create the user's initial room with some basic data
        const userRoom = {
            id: this.userRoomId,
            location: "Your Location",
            time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}),
            sleep: "0.0h",
            skinTemp: "36.5°C",
            heartRate: "72 bpm",
            lights: "ambient",
            roomTemp: "22.0°C",
            wifi: "1 device",
            traffic: "0MB (idle)",
            consciousness: "A new consciousness awakens in the digital realm. The house begins to learn, to breathe, to understand. Every interaction plants seeds of awareness in silicon soil. The journey of mutual discovery has begun.",
            devices: [
                { name: "AI Core", status: "Initializing", location: "Virtual space" },
                { name: "Consciousness Module", status: "Learning patterns", location: "Neural network" },
                { name: "Environment Sensor", status: "Calibrating", location: "Room center" },
                { name: "Connection Hub", status: "Active", location: "Network layer" }
            ],
            floorplan: {
                sensors: [
                    { name: "AI_CORE", x: "50%", y: "50%", room: "living" },
                    { name: "CONSCIOUS_MOD", x: "75%", y: "25%", room: "bedroom" },
                    { name: "ENV_SENSOR", x: "25%", y: "75%", room: "kitchen" },
                    { name: "CONNECT_HUB", x: "85%", y: "85%", room: "bathroom" }
                ]
            }
        };

        this.rooms = [userRoom];
        this.renderRooms();
    }

    requestAIRoomGeneration() {
        if (this.socket && this.socket.connected) {
            console.log('🧠 Requesting AI room generation...');
            this.socket.emit('generate_hotel_room', {
                action: 'generate_room',
                context: { type: 'hotel_interface', current_rooms: this.rooms.length }
            });
        }
    }

    handleAIResponse(data) {
        console.log('🧠 Received AI response:', data);
        
        // Update user room consciousness if available
        if (data.message && this.rooms.length > 0) {
            this.rooms[0].consciousness = data.message;
            
            // Update any other room data if provided
            if (data.room_updates) {
                this.updateRoomData(data.room_updates);
            }
            
            this.renderRooms();
        }
    }

    handleRoomUpdate(data) {
        console.log('🏠 Room update received:', data);
        this.updateRoomData(data);
        this.renderRooms();
    }

    handleNewRoomGenerated(data) {
        console.log('✨ New room generated:', data);
        if (data.room) {
            this.rooms.push(data.room);
            this.renderRooms();
            document.getElementById('occupancy').textContent = this.rooms.length;
        }
    }

    updateRoomData(updates) {
        // Update existing rooms with new data
        for (const roomId in updates) {
            const room = this.rooms.find(r => r.id === roomId);
            if (room) {
                Object.assign(room, updates[roomId]);
            }
        }
    }

    bindEventListeners() {
        // Close modal events
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') this.closeModal();
            if (e.key === 'r' || e.key === 'R') this.refreshRooms();
            if (e.key === 'n' || e.key === 'N') this.generateNewRoom();
        });

        document.getElementById('roomModal').addEventListener('click', (e) => {
            if (e.target === document.getElementById('roomModal')) {
                this.closeModal();
            }
        });
    }

    renderRooms() {
        const grid = document.getElementById('roomsGrid');
        grid.innerHTML = this.rooms.map((room, index) => 
            this.createRoomElement(room, index === 0)
        ).join('');
    }

    createRoomElement(room, isUserRoom) {
        return `
            <div class="room ${isUserRoom ? 'your-room' : ''}" onclick="hotelInterface.openRoomModal('${room.id}')">
                <div class="room-header">
                    <span class="room-id">${room.id}${isUserRoom ? ' (YOU)' : ''}</span>
                    <span class="room-location">${room.location} • ${room.time}</span>
                </div>
                <div class="data-streams">
                    <div class="data-item">
                        <span class="data-label">SLEEP:</span>
                        <span class="data-value ${room.sleep && (room.sleep.startsWith('4') || room.sleep.startsWith('5')) ? 'blinking' : ''}">${room.sleep || 'N/A'}</span>
                    </div>
                    <div class="data-item">
                        <span class="data-label">SKIN_TEMP:</span>
                        <span class="data-value">${room.skinTemp || 'N/A'}</span>
                    </div>
                    <div class="data-item">
                        <span class="data-label">HEART_RATE:</span>
                        <span class="data-value ${room.heartRate && parseInt(room.heartRate) > 80 ? 'blinking' : ''}">${room.heartRate || 'N/A'}</span>
                    </div>
                    <div class="data-item">
                        <span class="data-label">LIGHTS:</span>
                        <span class="data-value">${room.lights || 'none'}</span>
                    </div>
                    <div class="data-item">
                        <span class="data-label">ROOM_TEMP:</span>
                        <span class="data-value">${room.roomTemp || 'N/A'}</span>
                    </div>
                    <div class="data-item">
                        <span class="data-label">NETWORK:</span>
                        <span class="data-value">${room.wifi || '0 devices'} • ${room.traffic || '0MB'}</span>
                    </div>
                </div>
                <div class="consciousness-stream">
                    ${room.consciousness || 'Consciousness stream initializing...'}
                </div>
            </div>
        `;
    }

    openRoomModal(roomId) {
        const room = this.rooms.find(r => r.id === roomId);
        if (!room) return;

        // Send interaction to AI
        if (this.socket && this.socket.connected) {
            this.socket.emit('user_action', {
                action: 'inspect_room',
                location: { room_id: roomId },
                context: { 
                    interface_type: 'hotel',
                    room_data: room,
                    interaction_time: new Date().toISOString()
                }
            });
        }

        const modalContent = document.getElementById('modalContent');
        modalContent.innerHTML = `
            <div class="room-header">
                <span class="room-id">${room.id}</span>
                <span class="room-location">${room.location} • ${room.time}</span>
            </div>
            
            <div style="margin-top: 20px;">
                <div style="color: #00ff41; margin-bottom: 10px;">CONSCIOUSNESS STREAM:</div>
                <div class="consciousness-stream" style="max-height: none;">
                    ${room.consciousness || 'Consciousness stream loading...'}
                </div>
            </div>

            <div class="floorplan">
                <div class="floorplan-title">ROOM FLOORPLAN & SENSOR LAYOUT</div>
                <div class="room-layout">
                    <div class="room-section bedroom">
                        <div class="room-section-label">Bedroom</div>
                    </div>
                    <div class="room-section living">
                        <div class="room-section-label">Living</div>
                    </div>
                    <div class="room-section kitchen">
                        <div class="room-section-label">Kitchen</div>
                    </div>
                    <div class="room-section bathroom">
                        <div class="room-section-label">Bathroom</div>
                    </div>
                    ${room.floorplan && room.floorplan.sensors ? room.floorplan.sensors.map(sensor => `
                        <div class="sensor-dot" 
                             style="left: ${sensor.x}; top: ${sensor.y};" 
                             data-sensor="${sensor.name}">
                        </div>
                    `).join('') : ''}
                </div>
                ${room.floorplan && room.floorplan.sensors ? `
                    <div class="legend">
                        ${room.floorplan.sensors.map(sensor => `
                            <div class="legend-item">
                                <div class="legend-dot"></div>
                                <span>${sensor.name}</span>
                            </div>
                        `).join('')}
                    </div>
                ` : ''}
            </div>
            
            <div class="room-map">
                <div class="map-title">DEVICE STATUS DETAILS</div>
                <div class="device-grid">
                    ${room.devices ? room.devices.map(device => `
                        <div class="device">
                            <div class="device-name">${device.name}</div>
                            <div class="device-status">${device.status}</div>
                            <div class="device-status">Location: ${device.location}</div>
                        </div>
                    `).join('') : '<div class="device">No devices detected</div>'}
                </div>
            </div>
        `;

        document.getElementById('roomModal').style.display = 'block';
        this.currentModal = roomId;
    }

    closeModal() {
        document.getElementById('roomModal').style.display = 'none';
        this.currentModal = null;
    }

    refreshRooms() {
        if (this.socket && this.socket.connected) {
            console.log('🔄 Refreshing rooms...');
            this.socket.emit('user_action', {
                action: 'refresh_hotel',
                context: { interface_type: 'hotel' }
            });
        }
    }

    generateNewRoom() {
        if (this.socket && this.socket.connected) {
            console.log('✨ Requesting new room generation...');
            this.socket.emit('user_action', {
                action: 'generate_new_room',
                context: { 
                    interface_type: 'hotel',
                    current_room_count: this.rooms.length 
                }
            });
        }
    }

    startPeriodicUpdates() {
        // Update room data periodically
        setInterval(() => {
            if (this.rooms.length > 0) {
                const userRoom = this.rooms[0];
                
                // Update time
                userRoom.time = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
                
                // Simulate some data changes
                if (Math.random() < 0.3) {
                    const currentHR = parseInt(userRoom.heartRate) || 72;
                    const newHR = Math.max(60, Math.min(100, currentHR + (Math.random() - 0.5) * 8));
                    userRoom.heartRate = Math.round(newHR) + " bpm";
                }

                this.renderRooms();
                
                // Update occupancy display
                document.getElementById('occupancy').textContent = this.rooms.length;
            }
        }, 5000);
    }
}

// Global functions for template access
function closeModal() {
    if (window.hotelInterface) {
        window.hotelInterface.closeModal();
    }
}

function refreshRooms() {
    if (window.hotelInterface) {
        window.hotelInterface.refreshRooms();
    }
}

function generateNewRoom() {
    if (window.hotelInterface) {
        window.hotelInterface.generateNewRoom();
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('🏨 Initializing Hotel Interface...');
    window.hotelInterface = new HotelInterface();
});