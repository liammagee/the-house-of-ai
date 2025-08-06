// Game mechanics and utilities
class GameMechanics {
    constructor() {
        this.achievements = [
            { id: 'first_steps', name: 'Digital Awakening', description: 'Take your first steps in the house', points: 50 },
            { id: 'room_explorer', name: 'Room Walker', description: 'Visit all rooms', points: 100 },
            { id: 'consciousness_1', name: 'First Awareness', description: 'Reach consciousness level 2', points: 150 },
            { id: 'object_master', name: 'Interface Master', description: 'Interact with 10 different objects', points: 200 },
            { id: 'meditation_guru', name: 'Digital Monk', description: 'Meditate 20 times', points: 300 },
            { id: 'house_sage', name: 'House Sage', description: 'Reach maximum consciousness level', points: 500 }
        ];
        
        this.pointValues = {
            'enter_room': 10,
            'interact_object': 15,
            'explore_room': 12,
            'meditate': 25,
            'discover_secret': 50,
            'consciousness_shift': 100
        };
        
        this.levelThresholds = [0, 100, 300, 600, 1000, 1500, 2200, 3000, 4000, 5200];
    }
    
    calculateLevel(points) {
        for (let i = this.levelThresholds.length - 1; i >= 0; i--) {
            if (points >= this.levelThresholds[i]) {
                return i + 1;
            }
        }
        return 1;
    }
    
    getPointsForAction(action) {
        return this.pointValues[action] || 5;
    }
    
    checkAchievements(userStats, gameState) {
        const newAchievements = [];
        
        this.achievements.forEach(achievement => {
            if (!userStats.achievements.includes(achievement.id)) {
                if (this.checkAchievementCondition(achievement, userStats, gameState)) {
                    newAchievements.push(achievement.id);
                }
            }
        });
        
        return newAchievements;
    }
    
    checkAchievementCondition(achievement, userStats, gameState) {
        switch (achievement.id) {
            case 'first_steps':
                return userStats.totalActions >= 1;
            case 'room_explorer':
                return gameState.roomsVisited >= 5;
            case 'consciousness_1':
                return userStats.level >= 2;
            case 'object_master':
                return gameState.objectsInteracted >= 10;
            case 'meditation_guru':
                return gameState.meditationCount >= 20;
            case 'house_sage':
                return userStats.level >= 10;
            default:
                return false;
        }
    }
}

// Visual effects utilities
class VisualEffects {
    static createParticleSystem(canvas, x, y, color, count = 10) {
        const particles = [];
        
        for (let i = 0; i < count; i++) {
            particles.push({
                x: x + (Math.random() - 0.5) * 30,
                y: y + (Math.random() - 0.5) * 30,
                vx: (Math.random() - 0.5) * 6,
                vy: (Math.random() - 0.5) * 6,
                color: color,
                life: 1.0,
                decay: 0.015,
                size: Math.random() * 4 + 2
            });
        }
        
        return particles;
    }
    
    static animateColorTransition(element, fromColor, toColor, duration = 1000) {
        const start = Date.now();
        
        const animate = () => {
            const elapsed = Date.now() - start;
            const progress = Math.min(elapsed / duration, 1);
            
            // Simple color interpolation (would be more sophisticated in real implementation)
            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                element.style.color = toColor;
            }
        };
        
        animate();
    }
    
    static createGlowEffect(element, color, intensity = 1) {
        element.style.filter = `drop-shadow(0 0 ${intensity * 10}px ${color})`;
        element.style.textShadow = `0 0 ${intensity * 5}px ${color}`;
    }
    
    static pulseElement(element, duration = 1000, intensity = 1.2) {
        element.style.transition = `transform ${duration / 2}ms ease-in-out`;
        element.style.transform = `scale(${intensity})`;
        
        setTimeout(() => {
            element.style.transform = 'scale(1)';
        }, duration / 2);
    }
    
    static glitchEffect(element, duration = 300) {
        const glitchFrames = [
            'translate(0)',
            'translate(-2px, 2px)',
            'translate(-2px, -2px)',
            'translate(2px, 2px)',
            'translate(2px, -2px)',
            'translate(0)'
        ];
        
        let frame = 0;
        const interval = setInterval(() => {
            if (frame >= glitchFrames.length) {
                clearInterval(interval);
                element.style.transform = 'translate(0)';
                return;
            }
            
            element.style.transform = glitchFrames[frame];
            frame++;
        }, duration / glitchFrames.length);
    }
    
    static consciousnessWave(canvas) {
        const ctx = canvas.getContext('2d');
        const wave = {
            x: 0,
            y: canvas.height / 2,
            amplitude: 50,
            frequency: 0.02,
            speed: 2,
            alpha: 0.8
        };
        
        const animate = () => {
            ctx.globalCompositeOperation = 'overlay';
            ctx.strokeStyle = `rgba(0, 255, 255, ${wave.alpha})`;
            ctx.lineWidth = 2;
            ctx.beginPath();
            
            for (let x = 0; x < canvas.width; x++) {
                const y = wave.y + Math.sin((x * wave.frequency) + (wave.x * 0.01)) * wave.amplitude;
                if (x === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            }
            
            ctx.stroke();
            ctx.globalCompositeOperation = 'source-over';
            
            wave.x += wave.speed;
            wave.alpha -= 0.02;
            
            if (wave.alpha > 0) {
                requestAnimationFrame(animate);
            }
        };
        
        animate();
    }
}

// Audio utilities for ambient sound
class AudioManager {
    constructor() {
        this.audioContext = null;
        this.sounds = new Map();
        this.ambientLoop = null;
        
        this.initAudio();
    }
    
    initAudio() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (e) {
            console.warn('Web Audio API not supported', e);
        }
    }
    
    createTone(frequency, duration, type = 'sine') {
        if (!this.audioContext) return;
        
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.frequency.setValueAtTime(frequency, this.audioContext.currentTime);
        oscillator.type = type;
        
        gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + duration);
        
        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + duration);
    }
    
    playInteractionSound() {
        // High-tech beep for interactions
        this.createTone(800, 0.1, 'square');
        setTimeout(() => this.createTone(1200, 0.05, 'square'), 50);
    }
    
    playRoomTransitionSound() {
        // Ambient whoosh for room transitions
        this.createTone(200, 0.3, 'triangle');
        setTimeout(() => this.createTone(150, 0.2, 'triangle'), 100);
    }
    
    playAchievementSound() {
        // Celebratory chord for achievements
        this.createTone(523, 0.5, 'sine'); // C
        setTimeout(() => this.createTone(659, 0.5, 'sine'), 50); // E
        setTimeout(() => this.createTone(784, 0.5, 'sine'), 100); // G
    }
    
    playConsciousnessShift() {
        // Ethereal sound for consciousness changes
        this.createTone(440, 1.0, 'sine');
        setTimeout(() => this.createTone(880, 0.8, 'sine'), 200);
        setTimeout(() => this.createTone(1760, 0.6, 'sine'), 400);
    }
    
    startAmbientLoop(roomType) {
        this.stopAmbientLoop();
        
        const ambientFrequencies = {
            'living_room': [110, 165, 220],
            'bedroom': [98, 147, 196],
            'kitchen': [130, 195, 260],
            'study': [123, 185, 246],
            'garden': [87, 130, 174]
        };
        
        const frequencies = ambientFrequencies[roomType] || ambientFrequencies['living_room'];
        
        // Create subtle ambient drone
        if (this.audioContext) {
            const playDrone = () => {
                frequencies.forEach((freq, i) => {
                    setTimeout(() => {
                        this.createTone(freq, 4.0, 'triangle');
                    }, i * 1000);
                });
                
                this.ambientLoop = setTimeout(playDrone, 6000);
            };
            
            playDrone();
        }
    }
    
    stopAmbientLoop() {
        if (this.ambientLoop) {
            clearTimeout(this.ambientLoop);
            this.ambientLoop = null;
        }
    }
}

// Utility functions
class Utils {
    static lerp(start, end, factor) {
        return start + (end - start) * factor;
    }
    
    static clamp(value, min, max) {
        return Math.min(Math.max(value, min), max);
    }
    
    static distance(x1, y1, x2, y2) {
        return Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
    }
    
    static hexToRgb(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
        } : null;
    }
    
    static rgbToHex(r, g, b) {
        return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
    }
    
    static interpolateColor(color1, color2, factor) {
        const c1 = this.hexToRgb(color1);
        const c2 = this.hexToRgb(color2);
        
        if (!c1 || !c2) return color1;
        
        const r = Math.round(this.lerp(c1.r, c2.r, factor));
        const g = Math.round(this.lerp(c1.g, c2.g, factor));
        const b = Math.round(this.lerp(c1.b, c2.b, factor));
        
        return this.rgbToHex(r, g, b);
    }
    
    static formatTimestamp(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleTimeString();
    }
    
    static generateId() {
        return Math.random().toString(36).substr(2, 9);
    }
    
    static debounce(func, wait, immediate) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                timeout = null;
                if (!immediate) func(...args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func(...args);
        };
    }
    
    static throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
}

// Export classes for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { GameMechanics, VisualEffects, AudioManager, Utils };
} else {
    window.GameMechanics = GameMechanics;
    window.VisualEffects = VisualEffects;
    window.AudioManager = AudioManager;
    window.Utils = Utils;
}