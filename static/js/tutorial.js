// Tutorial system for The House of AI
class Tutorial {
    constructor(gameApp) {
        this.gameApp = gameApp;
        this.currentStep = 0;
        this.isActive = false;
        this.steps = [
            {
                title: "Welcome to The House of AI",
                message: "This is your digital sanctuary that learns and evolves based on your actions. Let me show you around...",
                highlight: null,
                action: null
            },
            {
                title: "Navigate Your House",
                message: "Click anywhere on the canvas to move your avatar (the glowing cyan circle). Try moving around the living room.",
                highlight: "#houseCanvas",
                action: "move_player"
            },
            {
                title: "Explore Different Rooms",
                message: "Click on different colored room areas to enter them. Each room has its own personality and will react to your presence.",
                highlight: "#houseCanvas",
                action: "enter_room"
            },
            {
                title: "Interact with Objects",
                message: "Click on glowing objects (like the TV or other items) to interact with them. Objects evolve based on your interactions.",
                highlight: "#houseCanvas",
                action: "interact_object"
            },
            {
                title: "Use Action Buttons",
                message: "Try the action buttons to perform specific activities. Each action teaches the AI about your personality.",
                highlight: ".action-panel",
                action: "use_actions"
            },
            {
                title: "Watch the AI Respond",
                message: "The AI consciousness will respond to your actions in the right panel, offering insights about your behavior patterns.",
                highlight: ".ai-panel",
                action: null
            },
            {
                title: "Keyboard Controls",
                message: "You can also use WASD or arrow keys to move, and press 'E' to interact with nearby objects.",
                highlight: null,
                action: null
            },
            {
                title: "The House Evolves",
                message: "As you interact more, rooms gain consciousness, objects transform, and the house adapts to reflect your unconscious mind.",
                highlight: null,
                action: null
            }
        ];
        
        this.createTutorialUI();
    }
    
    createTutorialUI() {
        // Create tutorial overlay
        const tutorialOverlay = document.createElement('div');
        tutorialOverlay.id = 'tutorialOverlay';
        tutorialOverlay.className = 'tutorial-overlay hidden';
        tutorialOverlay.innerHTML = `
            <div class="tutorial-content">
                <div class="tutorial-header">
                    <h3 id="tutorialTitle">Tutorial</h3>
                    <button id="tutorialClose" class="tutorial-close">×</button>
                </div>
                <div class="tutorial-body">
                    <p id="tutorialMessage"></p>
                    <div class="tutorial-progress">
                        <span id="tutorialStep">1</span> / <span id="tutorialTotal">${this.steps.length}</span>
                    </div>
                </div>
                <div class="tutorial-footer">
                    <button id="tutorialPrev" class="tutorial-btn">Previous</button>
                    <button id="tutorialNext" class="tutorial-btn">Next</button>
                    <button id="tutorialSkip" class="tutorial-btn secondary">Skip Tutorial</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(tutorialOverlay);
        
        // Add event listeners
        document.getElementById('tutorialClose').addEventListener('click', () => this.hideTutorial());
        document.getElementById('tutorialNext').addEventListener('click', () => this.nextStep());
        document.getElementById('tutorialPrev').addEventListener('click', () => this.previousStep());
        document.getElementById('tutorialSkip').addEventListener('click', () => this.hideTutorial());
        
        // Auto-start tutorial on first visit
        if (!localStorage.getItem('tutorial_completed')) {
            setTimeout(() => this.startTutorial(), 1000);
        }
    }
    
    startTutorial() {
        this.isActive = true;
        this.currentStep = 0;
        document.getElementById('tutorialOverlay').classList.remove('hidden');
        this.showStep(0);
    }
    
    showStep(stepIndex) {
        if (stepIndex < 0 || stepIndex >= this.steps.length) return;
        
        const step = this.steps[stepIndex];
        
        // Update UI
        document.getElementById('tutorialTitle').textContent = step.title;
        document.getElementById('tutorialMessage').textContent = step.message;
        document.getElementById('tutorialStep').textContent = stepIndex + 1;
        
        // Update button states
        document.getElementById('tutorialPrev').disabled = stepIndex === 0;
        document.getElementById('tutorialNext').textContent = 
            stepIndex === this.steps.length - 1 ? 'Finish' : 'Next';
        
        // Highlight elements
        this.clearHighlights();
        if (step.highlight) {
            this.highlightElement(step.highlight);
        }
        
        // Set up action tracking
        if (step.action) {
            this.waitForAction(step.action);
        }
    }
    
    highlightElement(selector) {
        const element = document.querySelector(selector);
        if (element) {
            element.classList.add('tutorial-highlight');
            
            // Create pulsing glow effect
            const glowOverlay = document.createElement('div');
            glowOverlay.className = 'tutorial-glow';
            glowOverlay.style.position = 'absolute';
            glowOverlay.style.pointerEvents = 'none';
            glowOverlay.style.border = '3px solid #00ffff';
            glowOverlay.style.borderRadius = '5px';
            glowOverlay.style.boxShadow = '0 0 20px #00ffff';
            glowOverlay.style.animation = 'pulse 2s infinite';
            
            const rect = element.getBoundingClientRect();
            glowOverlay.style.left = (rect.left - 5) + 'px';
            glowOverlay.style.top = (rect.top - 5) + 'px';
            glowOverlay.style.width = (rect.width + 10) + 'px';
            glowOverlay.style.height = (rect.height + 10) + 'px';
            glowOverlay.style.zIndex = '999';
            
            document.body.appendChild(glowOverlay);
            glowOverlay.id = 'tutorialGlow';
        }
    }
    
    clearHighlights() {
        // Remove highlight classes
        document.querySelectorAll('.tutorial-highlight').forEach(el => {
            el.classList.remove('tutorial-highlight');
        });
        
        // Remove glow overlay
        const glow = document.getElementById('tutorialGlow');
        if (glow) {
            glow.remove();
        }
    }
    
    waitForAction(actionType) {
        // Set up listeners for specific actions
        switch (actionType) {
            case 'move_player':
                this.waitForPlayerMovement();
                break;
            case 'enter_room':
                this.waitForRoomEntry();
                break;
            case 'interact_object':
                this.waitForObjectInteraction();
                break;
            case 'use_actions':
                this.waitForActionButton();
                break;
        }
    }
    
    waitForPlayerMovement() {
        const canvas = document.getElementById('houseCanvas');
        const handler = () => {
            canvas.removeEventListener('click', handler);
            setTimeout(() => this.actionCompleted(), 1000);
        };
        canvas.addEventListener('click', handler);
    }
    
    waitForRoomEntry() {
        // Listen for room changes through the game app
        const originalRoomChange = this.gameApp.onRoomChange;
        this.gameApp.onRoomChange = (roomId, room) => {
            originalRoomChange.call(this.gameApp, roomId, room);
            this.gameApp.onRoomChange = originalRoomChange;
            setTimeout(() => this.actionCompleted(), 1000);
        };
    }
    
    waitForObjectInteraction() {
        const originalObjectInteraction = this.gameApp.onObjectInteraction;
        this.gameApp.onObjectInteraction = (object) => {
            originalObjectInteraction.call(this.gameApp, object);
            this.gameApp.onObjectInteraction = originalObjectInteraction;
            setTimeout(() => this.actionCompleted(), 1000);
        };
    }
    
    waitForActionButton() {
        const buttons = document.querySelectorAll('.action-btn');
        const handler = () => {
            buttons.forEach(btn => btn.removeEventListener('click', handler));
            setTimeout(() => this.actionCompleted(), 1000);
        };
        buttons.forEach(btn => btn.addEventListener('click', handler));
    }
    
    actionCompleted() {
        // Show success feedback
        const tutorialContent = document.querySelector('.tutorial-content');
        tutorialContent.classList.add('success-flash');
        setTimeout(() => {
            tutorialContent.classList.remove('success-flash');
            // Auto-advance to next step
            if (this.currentStep < this.steps.length - 1) {
                this.nextStep();
            }
        }, 500);
    }
    
    nextStep() {
        if (this.currentStep < this.steps.length - 1) {
            this.currentStep++;
            this.showStep(this.currentStep);
        } else {
            this.finishTutorial();
        }
    }
    
    previousStep() {
        if (this.currentStep > 0) {
            this.currentStep--;
            this.showStep(this.currentStep);
        }
    }
    
    finishTutorial() {
        localStorage.setItem('tutorial_completed', 'true');
        this.hideTutorial();
        
        // Show completion message
        this.gameApp.addAIMessage("Tutorial completed! I'm excited to learn about your unique patterns as you explore...");
    }
    
    hideTutorial() {
        this.isActive = false;
        this.clearHighlights();
        document.getElementById('tutorialOverlay').classList.add('hidden');
    }
    
    // Public method to restart tutorial
    restartTutorial() {
        localStorage.removeItem('tutorial_completed');
        this.startTutorial();
    }
}

// Make Tutorial available globally
window.Tutorial = Tutorial;