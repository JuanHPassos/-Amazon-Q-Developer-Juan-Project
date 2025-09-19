class PomodoroTimer {
    constructor() {
        this.currentState = 'stopped';
        this.cyclesCompleted = 0;
        this.timeRemaining = 0;
        this.intervalId = null;
        
        this.initElements();
        this.bindEvents();
        this.updateDisplay();
    }
    
    initElements() {
        this.timeEl = document.getElementById('time');
        this.stateEl = document.getElementById('state');
        this.cyclesEl = document.getElementById('cycles');
        this.startBtn = document.getElementById('startBtn');
        this.stopBtn = document.getElementById('stopBtn');
        this.workTimeInput = document.getElementById('workTime');
        this.shortBreakInput = document.getElementById('shortBreak');
        this.longBreakInput = document.getElementById('longBreak');
    }
    
    bindEvents() {
        this.startBtn.addEventListener('click', () => this.start());
        this.stopBtn.addEventListener('click', () => this.stop());
        
        [this.workTimeInput, this.shortBreakInput, this.longBreakInput].forEach(input => {
            input.addEventListener('change', () => this.updateDisplay());
        });
    }
    
    start() {
        if (this.currentState === 'stopped') {
            this.startWorkSession();
        }
    }
    
    startWorkSession() {
        this.currentState = 'work';
        this.timeRemaining = this.workTimeInput.value * 60;
        this.startTimer();
        this.updateDisplay();
    }
    
    startBreak() {
        if (this.cyclesCompleted > 0 && this.cyclesCompleted % 4 === 0) {
            this.currentState = 'long-break';
            this.timeRemaining = this.longBreakInput.value * 60;
        } else {
            this.currentState = 'short-break';
            this.timeRemaining = this.shortBreakInput.value * 60;
        }
        this.startTimer();
        this.updateDisplay();
    }
    
    completeSession() {
        if (this.currentState === 'work') {
            this.cyclesCompleted++;
            this.startBreak();
        } else {
            this.stop();
        }
    }
    
    stop() {
        this.currentState = 'stopped';
        this.timeRemaining = 0;
        this.stopTimer();
        this.updateDisplay();
    }
    
    startTimer() {
        this.stopTimer();
        this.intervalId = setInterval(() => {
            this.timeRemaining--;
            this.updateDisplay();
            
            if (this.timeRemaining <= 0) {
                this.completeSession();
            }
        }, 1000);
    }
    
    stopTimer() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }
    
    formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    
    updateDisplay() {
        const stateMessages = {
            'work': '🍅 Trabalhando',
            'short-break': '☕ Pausa curta',
            'long-break': '🛋️ Pausa longa',
            'stopped': 'Pronto para começar'
        };
        
        if (this.currentState === 'stopped') {
            this.timeEl.textContent = this.formatTime(this.workTimeInput.value * 60);
        } else {
            this.timeEl.textContent = this.formatTime(this.timeRemaining);
        }
        
        this.stateEl.textContent = stateMessages[this.currentState];
        this.stateEl.className = `state ${this.currentState}`;
        this.cyclesEl.textContent = this.cyclesCompleted;
        
        this.startBtn.disabled = this.currentState !== 'stopped';
        this.stopBtn.disabled = this.currentState === 'stopped';
        
        // Desabilitar inputs durante execução
        const isRunning = this.currentState !== 'stopped';
        this.workTimeInput.disabled = isRunning;
        this.shortBreakInput.disabled = isRunning;
        this.longBreakInput.disabled = isRunning;
    }
}

// Inicializar o timer quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    new PomodoroTimer();
});