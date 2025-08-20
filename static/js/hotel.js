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
        this.startPeriodicUpdates();
    }

    connectWebSocket() {
        console.log('🔌 Connecting to WebSocket...');
        this.socket = io({
            transports: ['websocket', 'polling'],
            upgrade: true,
            rememberUpgrade: true,
            timeout: 20000,
            forceNew: true
        });
        
        this.socket.on('connect', () => {
            console.log('✅ Connected to server');
            this.updateConnectionStatus('Connected', 'ACTIVE');
            this.connectionRetries = 0;
            
            // Load persisted rooms first
            this.loadPersistedRooms();
        });

        this.socket.on('disconnect', () => {
            console.log('❌ Disconnected from server');
            this.updateConnectionStatus('Disconnected', 'DISCONNECTED');
        });
        
        // Listen for AI request logs
        this.socket.on('ai_request_log', (logEntry) => {
            console.log('📥 Received AI request log via WebSocket:', logEntry);
            console.log('   Method:', logEntry.method, '| Provider:', logEntry.provider, '| Success:', logEntry.success);
            this.addRequestLog(logEntry);
        });
        
        // Load current model info for AI panel
        this.loadCurrentModelForPanel();

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

        // Test WebSocket communication
        this.socket.on('test_message', (data) => {
            console.log('🧪 Test WebSocket event received:', data);
        });

        // Listen for new room generation
        this.socket.on('new_room_generated', (data) => {
            console.log('📨 WebSocket event received: new_room_generated');
            this.handleNewRoomGenerated(data);
        });

        // Listen for loaded rooms
        this.socket.on('rooms_loaded', (data) => {
            this.handleRoomsLoaded(data);
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

    loadPersistedRooms() {
        // Load rooms from server on startup
        if (this.socket && this.socket.connected) {
            console.log('📥 Loading persisted rooms...');
            this.socket.emit('user_action', {
                action: 'load_rooms',
                context: { interface_type: 'hotel' }
            });
        } else {
            // If not connected yet, generate initial room
            this.generateInitialRoom();
        }
    }

    persistRooms() {
        // Save rooms to server
        if (this.socket && this.socket.connected) {
            this.socket.emit('user_action', {
                action: 'save_rooms',
                context: { 
                    interface_type: 'hotel',
                    rooms: this.rooms
                }
            });
        }
    }

    clearRooms() {
        if (confirm('Are you sure you want to clear all rooms? This will reset the hotel to just your room.')) {
            console.log('🧹 Clearing all rooms...');
            this.showLoading('Clearing rooms...');
            
            // Keep only the user's room (first room)
            this.rooms = this.rooms.slice(0, 1);
            this.persistRooms();
            this.renderRooms();
            
            // Update occupancy
            document.getElementById('occupancy').textContent = this.rooms.length;
            
            this.hideLoading();
            console.log('✅ Rooms cleared');
        }
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
        this.hideLoading();
    }

    handleRoomUpdate(data) {
        console.log('🏠 Room update received:', data);
        this.updateRoomData(data);
        this.renderRooms();
    }

    handleNewRoomGenerated(data) {
        console.log('✨ New room generated via WebSocket:', data);
        console.log('   Room data present:', !!data.room);
        console.log('   Room ID:', data.room ? data.room.id : 'N/A');
        console.log('   Current rooms count before:', this.rooms.length);
        
        if (data.room) {
            this.rooms.push(data.room);
            this.persistRooms(); // Save to database
            this.renderRooms();
            document.getElementById('occupancy').textContent = this.rooms.length;
            console.log('   Rooms count after:', this.rooms.length);
            console.log('✅ Room added and UI updated');
        } else {
            console.warn('⚠️ No room data in response');
        }
        
        this.hideLoading();
        console.log('✅ Loading hidden, room generation complete');
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

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'c' || e.key === 'C') this.clearRooms();
            if (e.key === 'm' || e.key === 'M') this.showModelSettings();
        });

        document.getElementById('modelModal').addEventListener('click', (e) => {
            if (e.target === document.getElementById('modelModal')) {
                this.closeModelModal();
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
            this.showLoading('Analyzing room consciousness...');
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
        this.hideLoading();
    }

    closeModal() {
        document.getElementById('roomModal').style.display = 'none';
        this.currentModal = null;
    }

    handleRoomsLoaded(data) {
        console.log('📥 Rooms loaded from database:', data);
        if (data.rooms && data.rooms.length > 0) {
            this.rooms = data.rooms;
            this.renderRooms();
            document.getElementById('occupancy').textContent = this.rooms.length;
        } else {
            // No rooms found, generate initial room
            this.generateInitialRoom();
        }
        this.hideLoading();
    }

    refreshRooms() {
        if (this.socket && this.socket.connected) {
            console.log('🔄 Refreshing rooms...');
            this.showLoading('Refreshing data...');
            this.socket.emit('user_action', {
                action: 'refresh_hotel',
                context: { interface_type: 'hotel' }
            });
        }
    }

    generateNewRoom() {
        if (this.socket && this.socket.connected) {
            console.log('✨ Requesting new room generation...');
            this.showLoading('Generating new room...');
            this.socket.emit('user_action', {
                action: 'generate_new_room',
                context: { 
                    interface_type: 'hotel',
                    current_room_count: this.rooms.length 
                }
            });
        }
    }

    showLoading(message = 'Processing...') {
        const loadingEl = document.getElementById('loadingNotification');
        const textEl = document.getElementById('loadingText');
        const gridEl = document.getElementById('roomsGrid');
        
        textEl.textContent = message;
        loadingEl.style.display = 'block';
        gridEl.classList.add('processing');
    }

    hideLoading() {
        const loadingEl = document.getElementById('loadingNotification');
        const gridEl = document.getElementById('roomsGrid');
        
        loadingEl.style.display = 'none';
        gridEl.classList.remove('processing');
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

    showModelSettings() {
        console.log('📋 Opening model settings...');
        this.loadModelInfo();
        document.getElementById('modelModal').style.display = 'block';
    }

    closeModelModal() {
        document.getElementById('modelModal').style.display = 'none';
    }

    async loadModelInfo() {
        try {
            console.log('🔍 Loading model information...');
            const response = await fetch('/api/models');
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            this.displayModelInfo(data);
            
        } catch (error) {
            console.error('❌ Error loading model info:', error);
            document.getElementById('currentModelInfo').innerHTML = `
                <div style="color: #ff6666;">Error loading model information: ${error.message}</div>
            `;
        }
    }

    displayModelInfo(data) {
        // Display current model
        const currentInfo = document.getElementById('currentModelInfo');
        currentInfo.innerHTML = `
            <div style="color: #888; margin-bottom: 10px;">CURRENT MODEL:</div>
            <div style="color: #00ff41;">${data.current.provider} - ${data.current.model}</div>
            <div style="color: #ccc; font-size: 12px; margin-top: 5px;">
                Status: <span class="provider-status ${data.current.available ? 'available' : 'unavailable'}">
                    ${data.current.available ? 'AVAILABLE' : 'UNAVAILABLE'}
                </span>
            </div>
        `;

        // Display available providers
        const providerList = document.getElementById('providerList');
        providerList.innerHTML = '';
        
        // data.providers is an array, not an object
        data.providers.forEach(providerInfo => {
            const providerType = providerInfo.type;
            const isActive = providerType === data.current.provider;
            const providerElement = document.createElement('div');
            providerElement.className = `model-provider ${isActive ? 'active' : ''}`;
            providerElement.onclick = () => this.switchProvider(providerType, providerInfo.model);
            
            providerElement.innerHTML = `
                <div>
                    <div class="provider-name">${providerType}</div>
                    <div class="provider-model">${providerInfo.model || 'default'}</div>
                </div>
                <div class="provider-status ${providerInfo.available ? 'available' : 'unavailable'}">
                    ${providerInfo.available ? 'AVAILABLE' : 'UNAVAILABLE'}
                </div>
            `;
            
            providerList.appendChild(providerElement);
        });

        // Display room templates
        const templateList = document.getElementById('templateList');
        templateList.innerHTML = '';
        
        if (data.templates && data.templates.length > 0) {
            data.templates.forEach(template => {
                const templateElement = document.createElement('div');
                templateElement.className = 'template-item';
                templateElement.textContent = template;
                templateList.appendChild(templateElement);
            });
        } else {
            templateList.innerHTML = '<div style="color: #666;">No templates available</div>';
        }
    }

    async switchProvider(providerType, model) {
        try {
            console.log(`🔄 Switching to provider: ${providerType} with model: ${model}`);
            this.showLoading(`Switching to ${providerType}...`);
            
            const response = await fetch('/api/models/switch', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    provider: providerType,
                    model: model
                })
            });
            
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            if (data.success) {
                console.log('✅ Provider switched successfully');
                // Reload model info to update display
                await this.loadModelInfo();
                // Update AI panel heading with new model
                await this.loadCurrentModelForPanel();
                this.hideLoading();
                // Close the model modal after successful switch
                this.closeModelModal();
            }
            
        } catch (error) {
            console.error('❌ Error switching provider:', error);
            this.hideLoading();
            alert(`Failed to switch provider: ${error.message}`);
        }
    }
    
    async loadCurrentModelForPanel() {
        try {
            const response = await fetch('/api/models');
            const data = await response.json();
            
            if (data.current) {
                this.updateModelDisplay(data.current.provider, data.current.model);
            }
        } catch (error) {
            console.error('❌ Error loading current model for panel:', error);
            this.updateModelDisplay('unknown', 'unknown');
        }
    }
    
    updateModelDisplay(provider, model) {
        const modelDisplay = document.getElementById('currentModelDisplay');
        if (modelDisplay) {
            modelDisplay.textContent = `${provider.toUpperCase()}/${model}`;
        }
    }
    
    addRequestLog(logEntry) {
        console.log('📝 Adding request log to AI panel:', logEntry);
        const requestsContainer = document.getElementById('aiRequests');
        if (requestsContainer) {
            const logDiv = document.createElement('div');
            logDiv.style.cssText = 'margin-bottom: 10px; padding: 8px; border: 1px solid #333; background: #111; font-size: 10px;';
            
            const timestamp = new Date(logEntry.timestamp).toLocaleTimeString();
            const success = logEntry.success ? '✅' : '❌';
            
            logDiv.innerHTML = `
                <div style="color: #00ff41; margin-bottom: 4px;">
                    ${success} [${timestamp}] ${logEntry.provider} - ${logEntry.method}
                </div>
                <div style="color: #ccc; margin-bottom: 4px;">
                    Model: <span style="color: #ffaa00;">${logEntry.model}</span>
                </div>
                ${logEntry.args ? `<div style="color: #666; margin-bottom: 4px;">Args: ${logEntry.args}</div>` : ''}
                ${Object.keys(logEntry.kwargs || {}).length ? `<div style="color: #666; margin-bottom: 4px;">Kwargs: ${JSON.stringify(logEntry.kwargs)}</div>` : ''}
                ${logEntry.error ? `<div style="color: #ff6666;">Error: ${logEntry.error}</div>` : ''}
                ${logEntry.response_preview ? `<div style="color: #888; font-size: 9px; margin-top: 4px;">Response: ${logEntry.response_preview}</div>` : ''}
            `;
            
            requestsContainer.appendChild(logDiv);
            // Scroll to bottom to show latest log
            requestsContainer.scrollTop = requestsContainer.scrollHeight;
        } else {
            console.warn('⚠️ AI requests container not found');
        }
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


function switchAIMode(mode) {
    const messagesDiv = document.getElementById('aiMessages');
    const requestsDiv = document.getElementById('aiRequests');
    const messagesTab = document.getElementById('messagesTab');
    const requestsTab = document.getElementById('requestsTab');
    
    if (mode === 'messages') {
        messagesDiv.style.display = 'block';
        requestsDiv.style.display = 'none';
        messagesTab.style.borderColor = '#00ff41';
        messagesTab.style.color = '#00ff41';
        requestsTab.style.borderColor = '#666';
        requestsTab.style.color = '#666';
    } else if (mode === 'requests') {
        messagesDiv.style.display = 'none';
        requestsDiv.style.display = 'block';
        messagesTab.style.borderColor = '#666';
        messagesTab.style.color = '#666';
        requestsTab.style.borderColor = '#00ff41';
        requestsTab.style.color = '#00ff41';
    }
}

function clearRooms() {
    if (window.hotelInterface) {
        window.hotelInterface.clearRooms();
    }
}

function showModelSettings() {
    if (window.hotelInterface) {
        window.hotelInterface.showModelSettings();
    }
}

function closeModelModal() {
    if (window.hotelInterface) {
        window.hotelInterface.closeModelModal();
    }
}

// AI Panel Functions
let aiPanelVisible = false;

function toggleAIPanel() {
    console.log('Toggle AI Panel clicked');
    if (aiPanelVisible) {
        hideAIPanel();
    } else {
        showAIPanel();
    }
}

function showAIPanel() {
    console.log('Show AI Panel');
    const panel = document.getElementById('aiPanel');
    if (panel) {
        panel.style.transform = 'translateY(0)';
        aiPanelVisible = true;
    }
}

function hideAIPanel() {
    console.log('Hide AI Panel');
    const panel = document.getElementById('aiPanel');
    if (panel) {
        panel.style.transform = 'translateY(100%)';
        aiPanelVisible = false;
    }
}

function addAIMessage(message) {
    const messagesContainer = document.getElementById('aiMessages');
    if (messagesContainer) {
        const messageDiv = document.createElement('div');
        messageDiv.style.cssText = 'color: #ccc; margin-bottom: 8px; padding: 4px 0; border-bottom: 1px solid #222;';
        messageDiv.textContent = message;
        messagesContainer.appendChild(messageDiv);
        
        // Auto-scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // Show panel if not visible
        if (!aiPanelVisible) {
            showAIPanel();
        }
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('🏨 Initializing Hotel Interface...');
    window.hotelInterface = new HotelInterface();
    
    // Test AI panel after a short delay
    setTimeout(() => {
        console.log('Adding test AI message');
        addAIMessage('Hotel AI consciousness online. Ready to assist with room generation and management.');
    }, 2000);
});