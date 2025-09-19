import time
from enum import Enum
from typing import Callable, Optional

class PomodoroState(Enum):
    WORK = "work"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"
    STOPPED = "stopped"

class PomodoroTimer:
    def __init__(self, work_duration=25*60, short_break=5*60, long_break=15*60):
        self.work_duration = work_duration
        self.short_break_duration = short_break
        self.long_break_duration = long_break
        self.current_state = PomodoroState.STOPPED
        self.cycles_completed = 0
        self.time_remaining = 0
        self.on_state_change: Optional[Callable] = None
        
    def start_work_session(self):
        self.current_state = PomodoroState.WORK
        self.time_remaining = self.work_duration
        self._notify_state_change()
        
    def start_break(self):
        if self.cycles_completed > 0 and self.cycles_completed % 4 == 0:
            self.current_state = PomodoroState.LONG_BREAK
            self.time_remaining = self.long_break_duration
        else:
            self.current_state = PomodoroState.SHORT_BREAK
            self.time_remaining = self.short_break_duration
        self._notify_state_change()
        
    def complete_session(self):
        if self.current_state == PomodoroState.WORK:
            self.cycles_completed += 1
            self.start_break()
        else:
            self.current_state = PomodoroState.STOPPED
            self._notify_state_change()
            
    def stop(self):
        self.current_state = PomodoroState.STOPPED
        self.time_remaining = 0
        self._notify_state_change()
        
    def tick(self):
        if self.current_state != PomodoroState.STOPPED and self.time_remaining > 0:
            self.time_remaining -= 1
            if self.time_remaining == 0:
                self.complete_session()
                
    def set_state_change_callback(self, callback: Callable):
        self.on_state_change = callback
        
    def _notify_state_change(self):
        if self.on_state_change:
            self.on_state_change(self.current_state, self.time_remaining)
            
    def get_status(self):
        return {
            'state': self.current_state.value,
            'time_remaining': self.time_remaining,
            'cycles_completed': self.cycles_completed
        }