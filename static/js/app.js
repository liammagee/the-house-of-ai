// Main application controller
class GameApp {
    constructor() {
        this.socket = io();
        this.houseSimulation = null;
        this.userStats = {
            points: 0,
            level: 1,
            achievements: []
        };
        
        this.init();
    }
    
    init() {
        // Initialize canvas and simulation
        const canvas = document.getElementById('houseCanvas');
        this.houseSimulation = new HouseSimulation(canvas);
        
        // Make this available globally for simulation callbacks
        window.gameApp = this;
        
        // Setup socket listeners
        this.setupSocketListeners();
        
        // Setup UI event listeners
        this.setupUIListeners();
        
        // Initialize tutorial system
        this.tutorial = new Tutorial(this);
        
        // Setup help system
        this.setupHelpSystem();
        
        // Initial UI update
        this.updateUI();
    }
    
    setupSocketListeners() {
        this.socket.on('connect', () => {
            console.log('Connected to server');
            this.updateAIStatus('ACTIVE');
            
            // Request intelligent welcome message from AI
            setTimeout(() => {
                this.socket.emit('get_welcome_message');
                
                // Show basic instructions after welcome
                setTimeout(() => {
                    this.addAIMessage("💫 Quick guide: Click anywhere to move • Click rooms to explore • Click glowing objects to interact • Use action buttons below");
                }, 3000);
            }, 500);
        });
        
        this.socket.on('disconnect', () => {
            console.log('Disconnected from server');
            this.updateAIStatus('OFFLINE');
        });
        
        this.socket.on('ai_response', (data) => {
            this.handleAIResponse(data);
        });
        
        this.socket.on('house_state', (data) => {
            this.handleHouseStateUpdate(data);
        });
        
        this.socket.on('gamification_update', (data) => {
            this.handleGamificationUpdate(data);
        });
        
        this.socket.on('welcome_message', (data) => {
            this.addAIMessage(data.message);
        });
    }
    
    setupUIListeners() {
        // Action buttons
        document.getElementById('exploreBtn').addEventListener('click', () => {
            this.performAction('explore_room');
        });
        
        document.getElementById('interactBtn').addEventListener('click', () => {
            this.performAction('interact_object');
        });
        
        document.getElementById('meditateBtn').addEventListener('click', () => {
            this.performAction('meditate');
        });
    }
    
    setupHelpSystem() {
        // Help button functionality
        const helpButton = document.getElementById('helpButton');
        const instructionsPanel = document.getElementById('instructionsPanel');
        const closeInstructions = document.getElementById('closeInstructions');
        
        helpButton.addEventListener('click', () => {
            instructionsPanel.classList.remove('hidden');
        });
        
        closeInstructions.addEventListener('click', () => {
            instructionsPanel.classList.add('hidden');
        });
        
        // Close instructions when clicking outside
        instructionsPanel.addEventListener('click', (e) => {
            if (e.target === instructionsPanel) {
                instructionsPanel.classList.add('hidden');
            }
        });
    }
    
    // Called by HouseSimulation when room changes
    onRoomChange(roomId, room) {
        this.updateRoomInfo(room);
        
        // Show thinking indicator for room analysis
        this.showThinkingIndicator(`Scanning ${room.name} consciousness`);
        
        this.sendUserAction('enter_room', { roomId: roomId, room: room });
        
        // Trigger room-specific behaviors
        this.triggerRoomBehavior(roomId, room);
    }
    
    // Called by HouseSimulation when object is interacted with
    onObjectInteraction(object) {
        // Show immediate feedback
        this.addAIMessage(`You interact with the ${object.id.replace('_', ' ')}. Analyzing your interaction patterns...`);
        
        // Show thinking indicator
        this.showThinkingIndicator("Analyzing interaction patterns");
        
        this.sendUserAction('interact_object', { 
            objectId: object.id, 
            objectType: object.type,
            room: this.houseSimulation.player.currentRoom
        });
    }
    
    performAction(action) {
        const context = {
            currentRoom: this.houseSimulation.player.currentRoom,
            playerPosition: {
                x: this.houseSimulation.player.x,
                y: this.houseSimulation.player.y
            },
            houseState: this.houseSimulation.getState()
        };
        
        // Show thinking indicator with context-specific message
        const thinkingMessages = {
            'explore_room': 'Analyzing exploration patterns',
            'interact_object': 'Processing object interaction',
            'meditate': 'Detecting consciousness shifts'
        };
        
        this.showThinkingIndicator(thinkingMessages[action] || 'Processing neural patterns');
        
        this.sendUserAction(action, context);
        
        // Visual feedback
        this.addActionFeedback(action);
    }
    
    sendUserAction(action, context) {
        this.socket.emit('user_action', {
            action: action,
            location: {
                room: this.houseSimulation.player.currentRoom,
                x: this.houseSimulation.player.x,
                y: this.houseSimulation.player.y
            },
            context: context,
            timestamp: Date.now()
        });
    }
    
    handleAIResponse(response) {
        // Display AI message
        this.addAIMessage(response.message || response.text);
        
        // Apply house changes
        if (response.houseChanges) {
            this.houseSimulation.updateFromAI(response.houseChanges);
        }
        
        // Handle special behaviors
        if (response.behaviors) {
            response.behaviors.forEach(behavior => {
                this.executeBehavior(behavior);
            });
        }
        
        // Update consciousness levels
        if (response.consciousness) {
            this.updateConsciousness(response.consciousness);
        }
    }
    
    handleHouseStateUpdate(state) {
        // Update simulation state
        if (this.houseSimulation) {
            this.houseSimulation.updateFromAI({ stateUpdate: state });
        }
    }
    
    handleGamificationUpdate(update) {
        if (update.points) {
            this.userStats.points += update.points;
            this.showPointsGain(update.points);
        }
        
        if (update.achievements && update.achievements.length > 0) {
            update.achievements.forEach(achievement => {
                this.unlockAchievement(achievement);
            });
        }
        
        if (update.level_up) {
            this.levelUp();
        }
        
        this.updateUI();
    }
    
    updateRoomInfo(room) {
        document.getElementById('roomName').textContent = room.name;
        document.getElementById('roomDescription').textContent = room.description;
        
        // Add room entry animation
        const roomInfo = document.getElementById('roomInfo');
        roomInfo.classList.add('pulse');
        setTimeout(() => roomInfo.classList.remove('pulse'), 1000);
    }
    
    addAIMessage(message) {
        // Remove thinking indicator if present
        this.hideThinkingIndicator();
        
        const messagesContainer = document.getElementById('aiMessages');
        const messageElement = document.createElement('div');
        messageElement.className = 'ai-message';
        messageElement.textContent = message;
        
        messagesContainer.appendChild(messageElement);
        
        // Multiple attempts to ensure scrolling works
        this.scrollToBottom(messagesContainer);
        
        // Limit message history
        while (messagesContainer.children.length > 20) {
            messagesContainer.removeChild(messagesContainer.firstChild);
        }
    }
    
    showThinkingIndicator(message = "AI consciousness processing") {
        // Remove any existing thinking indicator
        this.hideThinkingIndicator();
        
        const messagesContainer = document.getElementById('aiMessages');
        const thinkingElement = document.createElement('div');
        thinkingElement.className = 'ai-thinking';
        thinkingElement.id = 'aiThinking';
        thinkingElement.innerHTML = `
            <div class="thinking-text">${message}...</div>
            <div class="thinking-dots">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        `;
        
        messagesContainer.appendChild(thinkingElement);
        this.scrollToBottom(messagesContainer);
        
        // Update AI status
        this.updateAIStatus('THINKING');
    }
    
    hideThinkingIndicator() {
        const thinkingElement = document.getElementById('aiThinking');
        if (thinkingElement) {
            thinkingElement.remove();
        }
        
        // Reset AI status
        this.updateAIStatus('ACTIVE');
    }
    
    scrollToBottom(container) {
        console.log(`Scrolling - Height: ${container.scrollHeight}, Current: ${container.scrollTop}`);
        
        // Immediate scroll
        container.scrollTop = container.scrollHeight;
        
        // Delayed scroll to handle async rendering
        setTimeout(() => {
            container.scrollTop = container.scrollHeight;
            console.log(`After delay - Height: ${container.scrollHeight}, Current: ${container.scrollTop}`);
        }, 10);
        
        // Additional scroll for complex layouts
        requestAnimationFrame(() => {
            container.scrollTop = container.scrollHeight;
        });
        
        // Force scroll using scrollIntoView as backup
        setTimeout(() => {
            const lastMessage = container.lastElementChild;
            if (lastMessage) {
                lastMessage.scrollIntoView({ behavior: 'smooth', block: 'end' });
            }
        }, 50);
    }
    
    updateAIStatus(status) {
        const statusElement = document.getElementById('aiStatus');
        statusElement.textContent = status;
        statusElement.className = `ai-status ${status.toLowerCase()}`;
        
        // Add visual feedback in the header for different states
        const header = document.querySelector('.header');
        header.classList.remove('ai-thinking', 'ai-processing');
        
        if (status === 'THINKING') {
            header.classList.add('ai-thinking');
        } else if (status === 'PROCESSING') {
            header.classList.add('ai-processing');
        }
    }
    
    updateUI() {
        document.getElementById('points').textContent = this.userStats.points;
        document.getElementById('level').textContent = this.userStats.level;
    }
    
    showPointsGain(points) {
        // Create floating points animation
        const pointsElement = document.createElement('div');
        pointsElement.textContent = `+${points}`;
        pointsElement.style.cssText = `
            position: fixed;
            top: 100px;
            right: 150px;
            color: #00ff41;
            font-family: 'Courier New', monospace;
            font-size: 20px;
            font-weight: bold;
            pointer-events: none;
            z-index: 1000;
            text-shadow: 0 0 10px #00ff41;
        `;
        
        document.body.appendChild(pointsElement);
        
        // Animate upward
        let position = 100;
        const animate = () => {
            position -= 2;
            pointsElement.style.top = position + 'px';
            pointsElement.style.opacity = (position / 100);
            
            if (position > 50) {
                requestAnimationFrame(animate);
            } else {
                document.body.removeChild(pointsElement);
            }
        };
        
        animate();
    }
    
    unlockAchievement(achievement) {
        if (this.userStats.achievements.includes(achievement)) return;
        
        this.userStats.achievements.push(achievement);
        
        // Show achievement popup
        const popup = document.getElementById('achievementPopup');
        const text = document.getElementById('achievementText');
        text.textContent = achievement;
        
        popup.classList.add('show');
        
        setTimeout(() => {
            popup.classList.remove('show');
        }, 3000);
    }
    
    levelUp() {
        this.userStats.level += 1;
        
        // Level up effects
        const header = document.querySelector('.header');
        header.classList.add('glitch');
        setTimeout(() => header.classList.remove('glitch'), 300);
        
        this.addAIMessage(`Consciousness level increased to ${this.userStats.level}! New areas of the house are awakening...`);
    }
    
    addActionFeedback(action) {
        // Visual feedback for action buttons
        const buttons = document.querySelectorAll('.action-btn');
        buttons.forEach(btn => {
            if (btn.textContent.toLowerCase().includes(action.split('_')[0])) {
                btn.classList.add('pulse');
                setTimeout(() => btn.classList.remove('pulse'), 500);
            }
        });
    }
    
    triggerRoomBehavior(roomId, room) {
        // Room-specific behaviors and ambiance
        switch(roomId) {
            case 'bedroom':
                if (!room.visited) {
                    this.addAIMessage("You enter the Dream Chamber. The walls shimmer with memories you can't quite recall...");
                }
                break;
            case 'kitchen':
                this.addAIMessage("The Synthesis Lab hums with possibilities. What would you like to create?");
                break;
            case 'study':
                this.addAIMessage("The Thought Matrix recognizes your presence. Knowledge flows like liquid light...");
                break;
            case 'garden':
                this.addAIMessage("The Cyber Garden responds to your thoughts, digital flora blooming in impossible colors...");
                break;
        }
    }
    
    executeBehavior(behavior) {
        switch(behavior.type) {
            case 'room_transformation':
                this.transformRoom(behavior.roomId, behavior.changes);
                break;
            case 'spawn_object':
                this.spawnObject(behavior.object);
                break;
            case 'ambient_change':
                this.changeAmbiance(behavior.settings);
                break;
            case 'consciousness_shift':
                this.shiftConsciousness(behavior.level, behavior.description);
                break;
        }
    }
    
    transformRoom(roomId, changes) {
        // Apply visual room transformations
        const room = this.houseSimulation.rooms[roomId];
        if (room) {
            Object.assign(room, changes);
            this.addAIMessage(`The ${room.name} shifts and evolves, responding to your unconscious desires...`);
        }
    }
    
    spawnObject(objectData) {
        this.houseSimulation.interactableObjects.push(objectData);
        this.addAIMessage(`✨ Your creativity has manifested a new ${objectData.type} in the ${objectData.room.replace('_', ' ')}! It glows with potential...`);
        
        // Visual feedback
        if (this.houseSimulation.addParticles) {
            this.houseSimulation.addParticles(objectData.x, objectData.y, objectData.color, 15);
        }
    }
    
    changeAmbiance(settings) {
        // Modify visual effects, colors, etc.
        if (settings.particleColor) {
            // Change particle system colors
        }
        if (settings.glowIntensity) {
            // Modify glow effects
        }
    }
    
    updateConsciousness(consciousness) {
        // Handle consciousness level changes
        if (consciousness.detected) {
            const level = consciousness.level || 1;
            const description = consciousness.description || 'Consciousness shift detected';
            this.shiftConsciousness(level, description);
        }
    }
    
    shiftConsciousness(level, description) {
        this.addAIMessage(`Consciousness shift detected: ${description}`);
        
        // Visual effects for consciousness changes
        const canvas = document.getElementById('houseCanvas');
        canvas.style.filter = `hue-rotate(${level * 30}deg)`;
        setTimeout(() => {
            canvas.style.filter = 'none';
        }, 2000);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new GameApp();
});