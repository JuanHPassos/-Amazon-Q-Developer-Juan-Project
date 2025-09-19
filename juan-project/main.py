#!/usr/bin/env python3
from pomodoro import PomodoroTimer, PomodoroState
import time

def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def on_state_change(state, time_remaining):
    state_messages = {
        PomodoroState.WORK: "🍅 Trabalhando",
        PomodoroState.SHORT_BREAK: "☕ Pausa curta",
        PomodoroState.LONG_BREAK: "🛋️ Pausa longa",
        PomodoroState.STOPPED: "⏹️ Parado"
    }
    print(f"\n{state_messages[state]} - {format_time(time_remaining)}")

def main():
    timer = PomodoroTimer()
    timer.set_state_change_callback(on_state_change)
    
    print("🍅 Pomodoro Timer")
    print("Comandos: start, stop, status, quit")
    
    while True:
        command = input("\n> ").strip().lower()
        
        if command == "start":
            timer.start_work_session()
        elif command == "stop":
            timer.stop()
        elif command == "status":
            status = timer.get_status()
            print(f"Estado: {status['state']}")
            print(f"Tempo restante: {format_time(status['time_remaining'])}")
            print(f"Ciclos completados: {status['cycles_completed']}")
        elif command == "quit":
            break
        else:
            print("Comando inválido")

if __name__ == "__main__":
    main()