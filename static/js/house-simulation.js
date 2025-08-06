class HouseSimulation {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.width = canvas.width;
        this.height = canvas.height;
        
        // House state
        this.rooms = this.initializeRooms();
        this.player = {
            x: 600,  // Start in center
            y: 400,
            size: 20,
            color: '#00ffff',
            currentRoom: 'living_room'
        };
        
        this.interactableObjects = this.initializeObjects();
        this.particles = [];
        this.lastTime = 0;
        
        // Mouse interaction
        this.mouseX = 0;
        this.mouseY = 0;
        this.setupEventListeners();
        
        // Start render loop
        this.render();
    }
    
    initializeRooms() {
        return {
            living_room: {
                name: "Neural Living Room",
                x: 400, y: 200, width: 400, height: 300,
                color: '#1a1a2e',
                borderColor: '#00ffff',
                description: "A space that pulses with digital consciousness, adapting to your presence.",
                consciousness_level: 1,
                visited: true
            },
            bedroom: {
                name: "Dream Chamber",
                x: 100, y: 100, width: 250, height: 200,
                color: '#2e1a2e',
                borderColor: '#ff0080',
                description: "Where your unconscious mind interfaces with the digital realm.",
                consciousness_level: 0,
                visited: false
            },
            kitchen: {
                name: "Synthesis Lab",
                x: 850, y: 150, width: 300, height: 250,
                color: '#1a2e1a',
                borderColor: '#00ff41',
                description: "A space where digital and organic merge in perfect harmony.",
                consciousness_level: 0,
                visited: false
            },
            study: {
                name: "Thought Matrix",
                x: 200, y: 450, width: 350, height: 280,
                color: '#2e2e1a',
                borderColor: '#ffff00',
                description: "The nexus of learning and digital enlightenment.",
                consciousness_level: 0,
                visited: false
            },
            garden: {
                name: "Cyber Garden",
                x: 650, y: 550, width: 400, height: 200,
                color: '#1a2e2e',
                borderColor: '#00ff80',
                description: "Where digital nature grows and evolves with your thoughts.",
                consciousness_level: 0,
                visited: false
            }
        };
    }
    
    initializeObjects() {
        return [
            // Living room objects
            { id: 'tv', x: 500, y: 220, width: 80, height: 50, room: 'living_room', 
              type: 'screen', active: true, color: '#00ffff' },
            { id: 'couch', x: 450, y: 350, width: 120, height: 60, room: 'living_room', 
              type: 'furniture', active: false, color: '#404040' },
            
            // Bedroom objects
            { id: 'bed', x: 150, y: 200, width: 100, height: 80, room: 'bedroom', 
              type: 'furniture', active: false, color: '#404040' },
            { id: 'mirror', x: 300, y: 120, width: 30, height: 60, room: 'bedroom', 
              type: 'reflective', active: true, color: '#ffffff' },
            
            // Kitchen objects
            { id: 'synth_unit', x: 900, y: 180, width: 60, height: 40, room: 'kitchen', 
              type: 'machine', active: true, color: '#00ff41' },
            
            // Study objects
            { id: 'neural_interface', x: 350, y: 500, width: 80, height: 60, room: 'study', 
              type: 'computer', active: true, color: '#ffff00' },
            { id: 'books', x: 250, y: 480, width: 60, height: 80, room: 'study', 
              type: 'knowledge', active: false, color: '#8080ff' },
            
            // Garden objects
            { id: 'bio_tree', x: 800, y: 600, width: 50, height: 80, room: 'garden', 
              type: 'living', active: true, color: '#00ff80' }
        ];
    }
    
    setupEventListeners() {
        this.canvas.addEventListener('mousemove', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            this.mouseX = e.clientX - rect.left;
            this.mouseY = e.clientY - rect.top;
        });
        
        this.canvas.addEventListener('click', (e) => {
            this.handleClick(this.mouseX, this.mouseY);
        });
        
        // Keyboard controls
        document.addEventListener('keydown', (e) => {
            this.handleKeyPress(e.key);
        });
    }
    
    handleClick(x, y) {
        // Check if clicking on an object first (highest priority)
        const object = this.getObjectAt(x, y);
        if (object) {
            this.interactWithObject(object);
            return;
        }
        
        // Always move player to clicked location
        this.movePlayerTo(x, y);
        
        // After moving, check if we entered a new room
        setTimeout(() => {
            this.updatePlayerRoom();
        }, 100);
    }
    
    handleKeyPress(key) {
        const speed = 10;
        switch(key.toLowerCase()) {
            case 'w':
            case 'arrowup':
                this.player.y = Math.max(0, this.player.y - speed);
                break;
            case 's':
            case 'arrowdown':
                this.player.y = Math.min(this.height - this.player.size, this.player.y + speed);
                break;
            case 'a':
            case 'arrowleft':
                this.player.x = Math.max(0, this.player.x - speed);
                break;
            case 'd':
            case 'arrowright':
                this.player.x = Math.min(this.width - this.player.size, this.player.x + speed);
                break;
            case 'e':
                this.interactWithNearbyObject();
                break;
        }
        
        this.updatePlayerRoom();
    }
    
    movePlayerTo(x, y) {
        // Make sure coordinates are within canvas bounds
        x = Math.max(this.player.size/2, Math.min(this.width - this.player.size/2, x));
        y = Math.max(this.player.size/2, Math.min(this.height - this.player.size/2, y));
        
        // Animate player movement
        const startX = this.player.x;
        const startY = this.player.y;
        const duration = 300; // ms - shorter for better responsiveness
        const startTime = Date.now();
        
        console.log(`Moving player from (${startX}, ${startY}) to (${x}, ${y})`); // Debug log
        
        const animate = () => {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Ease out animation
            const easeProgress = 1 - Math.pow(1 - progress, 3);
            
            this.player.x = startX + (x - startX) * easeProgress;
            this.player.y = startY + (y - startY) * easeProgress;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                // Ensure final position is exact
                this.player.x = x;
                this.player.y = y;
            }
        };
        
        animate();
    }
    
    updatePlayerRoom() {
        for (let roomId in this.rooms) {
            const room = this.rooms[roomId];
            if (this.player.x >= room.x && this.player.x <= room.x + room.width &&
                this.player.y >= room.y && this.player.y <= room.y + room.height) {
                if (this.player.currentRoom !== roomId) {
                    this.enterRoom(roomId);
                }
                break;
            }
        }
    }
    
    enterRoom(roomId) {
        const room = this.rooms[roomId];
        if (!room) return;
        
        this.player.currentRoom = roomId;
        room.visited = true;
        
        // Emit room change event
        if (window.gameApp) {
            window.gameApp.onRoomChange(roomId, room);
        }
        
        // Add particles for room entry effect
        this.addParticles(this.player.x, this.player.y, room.borderColor, 10);
    }
    
    getObjectAt(x, y) {
        return this.interactableObjects.find(obj => 
            x >= obj.x && x <= obj.x + obj.width &&
            y >= obj.y && y <= obj.y + obj.height
        );
    }
    
    interactWithNearbyObject() {
        const nearbyObject = this.interactableObjects.find(obj => {
            const distance = Math.sqrt(
                Math.pow(this.player.x - (obj.x + obj.width/2), 2) +
                Math.pow(this.player.y - (obj.y + obj.height/2), 2)
            );
            return distance < 50 && obj.room === this.player.currentRoom;
        });
        
        if (nearbyObject) {
            this.interactWithObject(nearbyObject);
        }
    }
    
    interactWithObject(object) {
        // Emit interaction event
        if (window.gameApp) {
            window.gameApp.onObjectInteraction(object);
        }
        
        // Visual feedback
        this.addParticles(object.x + object.width/2, object.y + object.height/2, object.color, 5);
        
        // Object-specific behavior
        if (object.type === 'screen' && object.id === 'tv') {
            this.activateScreen(object);
        }
    }
    
    activateScreen(screen) {
        screen.active = !screen.active;
        if (screen.active) {
            // Add screen glow effect
            screen.glowIntensity = 1.0;
        }
    }
    
    addParticles(x, y, color, count) {
        for (let i = 0; i < count; i++) {
            this.particles.push({
                x: x + (Math.random() - 0.5) * 20,
                y: y + (Math.random() - 0.5) * 20,
                vx: (Math.random() - 0.5) * 4,
                vy: (Math.random() - 0.5) * 4,
                color: color,
                life: 1.0,
                decay: 0.02
            });
        }
    }
    
    updateParticles() {
        this.particles = this.particles.filter(particle => {
            particle.x += particle.vx;
            particle.y += particle.vy;
            particle.life -= particle.decay;
            return particle.life > 0;
        });
    }
    
    render() {
        this.ctx.fillStyle = '#0a0a0a';
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        // Draw rooms
        this.drawRooms();
        
        // Draw objects
        this.drawObjects();
        
        // Draw player
        this.drawPlayer();
        
        // Draw particles
        this.drawParticles();
        
        // Draw helpful hints for first-time users
        this.drawHints();
        
        // Update animations
        this.updateParticles();
        
        requestAnimationFrame(() => this.render());
    }
    
    drawRooms() {
        for (let roomId in this.rooms) {
            const room = this.rooms[roomId];
            
            // Room background
            this.ctx.fillStyle = room.color;
            this.ctx.fillRect(room.x, room.y, room.width, room.height);
            
            // Room border with glow effect
            this.ctx.strokeStyle = room.borderColor;
            this.ctx.lineWidth = 2;
            this.ctx.shadowColor = room.borderColor;
            this.ctx.shadowBlur = room.visited ? 10 : 5;
            this.ctx.strokeRect(room.x, room.y, room.width, room.height);
            this.ctx.shadowBlur = 0;
            
            // Room label
            this.ctx.fillStyle = room.borderColor;
            this.ctx.font = '14px Courier New';
            this.ctx.fillText(room.name, room.x + 10, room.y + 25);
            
            // Consciousness level indicator
            const level = room.consciousness_level;
            for (let i = 0; i < 3; i++) {
                this.ctx.fillStyle = i < level ? room.borderColor : '#333333';
                this.ctx.fillRect(room.x + room.width - 30 + i * 8, room.y + 10, 6, 6);
            }
        }
    }
    
    drawObjects() {
        this.interactableObjects.forEach(obj => {
            // Object glow effect for active objects
            if (obj.active) {
                this.ctx.shadowColor = obj.color;
                this.ctx.shadowBlur = 8;
            }
            
            this.ctx.fillStyle = obj.color;
            this.ctx.fillRect(obj.x, obj.y, obj.width, obj.height);
            
            // Object interaction hint
            const distance = Math.sqrt(
                Math.pow(this.player.x - (obj.x + obj.width/2), 2) +
                Math.pow(this.player.y - (obj.y + obj.height/2), 2)
            );
            
            if (distance < 50 && obj.room === this.player.currentRoom) {
                this.ctx.strokeStyle = '#ffffff';
                this.ctx.lineWidth = 1;
                this.ctx.strokeRect(obj.x - 2, obj.y - 2, obj.width + 4, obj.height + 4);
            }
            
            this.ctx.shadowBlur = 0;
        });
    }
    
    drawPlayer() {
        // Player glow
        this.ctx.shadowColor = this.player.color;
        this.ctx.shadowBlur = 15;
        
        // Player body
        this.ctx.fillStyle = this.player.color;
        this.ctx.beginPath();
        this.ctx.arc(this.player.x + this.player.size/2, this.player.y + this.player.size/2, 
                     this.player.size/2, 0, Math.PI * 2);
        this.ctx.fill();
        
        // Player direction indicator
        this.ctx.strokeStyle = this.player.color;
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.moveTo(this.player.x + this.player.size/2, this.player.y + this.player.size/2);
        this.ctx.lineTo(this.mouseX, this.mouseY);
        this.ctx.stroke();
        
        this.ctx.shadowBlur = 0;
    }
    
    drawParticles() {
        this.particles.forEach(particle => {
            this.ctx.fillStyle = particle.color + Math.floor(particle.life * 255).toString(16).padStart(2, '0');
            this.ctx.fillRect(particle.x, particle.y, 3, 3);
        });
    }
    
    drawHints() {
        // Only show hints for the first few seconds or if user hasn't moved much
        const showHints = !localStorage.getItem('hints_seen') || 
                         (Date.now() - (this.startTime || Date.now())) < 15000;
        
        if (!showHints) return;
        
        this.ctx.save();
        this.ctx.font = '16px Courier New';
        this.ctx.textAlign = 'center';
        
        // Pulsing alpha for attention
        const alpha = 0.7 + 0.3 * Math.sin(Date.now() / 1000);
        
        // Hint 1: Click to move
        this.ctx.fillStyle = `rgba(0, 255, 255, ${alpha})`;
        this.ctx.fillText('← Click anywhere to move your avatar', this.width / 2, 50);
        
        // Hint 2: Room exploration
        this.ctx.fillStyle = `rgba(255, 0, 128, ${alpha})`;
        this.ctx.fillText('Click colored room areas to explore ↓', this.width / 2, this.height - 100);
        
        // Hint 3: Object interaction
        if (this.interactableObjects.length > 0) {
            const tv = this.interactableObjects.find(obj => obj.id === 'tv');
            if (tv) {
                this.ctx.fillStyle = `rgba(0, 255, 65, ${alpha})`;
                this.ctx.fillText('↑ Click glowing objects', tv.x + tv.width/2, tv.y - 10);
            }
        }
        
        // Hint 4: Action buttons
        this.ctx.fillStyle = `rgba(255, 255, 0, ${alpha})`;
        this.ctx.fillText('Use action buttons below ↓', this.width / 2, this.height - 50);
        
        this.ctx.restore();
        
        // Auto-hide hints after user interacts
        if (this.player.x !== 600 || this.player.y !== 400) {
            localStorage.setItem('hints_seen', 'true');
        }
    }
    
    // API for external updates
    updateFromAI(aiResponse) {
        if (aiResponse.roomChanges) {
            for (let roomId in aiResponse.roomChanges) {
                if (this.rooms[roomId]) {
                    Object.assign(this.rooms[roomId], aiResponse.roomChanges[roomId]);
                }
            }
        }
        
        if (aiResponse.newObjects) {
            this.interactableObjects.push(...aiResponse.newObjects);
        }
        
        if (aiResponse.effects) {
            aiResponse.effects.forEach(effect => {
                this.applyEffect(effect);
            });
        }
    }
    
    applyEffect(effect) {
        switch(effect.type) {
            case 'particles':
                this.addParticles(effect.x, effect.y, effect.color, effect.count);
                break;
            case 'room_glow':
                if (this.rooms[effect.roomId]) {
                    this.rooms[effect.roomId].glowIntensity = effect.intensity;
                }
                break;
        }
    }
    
    getState() {
        return {
            player: this.player,
            rooms: this.rooms,
            objects: this.interactableObjects
        };
    }
}