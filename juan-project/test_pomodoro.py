import unittest
from unittest.mock import Mock
from pomodoro import PomodoroTimer, PomodoroState

class TestPomodoroTimer(unittest.TestCase):
    
    def setUp(self):
        self.timer = PomodoroTimer(work_duration=10, short_break=5, long_break=15)
        
    def test_initial_state(self):
        """Teste unitário: estado inicial"""
        self.assertEqual(self.timer.current_state, PomodoroState.STOPPED)
        self.assertEqual(self.timer.cycles_completed, 0)
        self.assertEqual(self.timer.time_remaining, 0)
        
    def test_start_work_session(self):
        """Teste unitário: iniciar sessão de trabalho"""
        self.timer.start_work_session()
        self.assertEqual(self.timer.current_state, PomodoroState.WORK)
        self.assertEqual(self.timer.time_remaining, 10)
        
    def test_complete_work_cycle(self):
        """Teste de integração: ciclo completo de trabalho"""
        callback_mock = Mock()
        self.timer.set_state_change_callback(callback_mock)
        
        self.timer.start_work_session()
        
        # Simular passagem do tempo
        for _ in range(10):
            self.timer.tick()
            
        self.assertEqual(self.timer.current_state, PomodoroState.SHORT_BREAK)
        self.assertEqual(self.timer.cycles_completed, 1)
        self.assertTrue(callback_mock.called)
        
    def test_long_break_after_4_cycles(self):
        """Teste de integração: pausa longa após 4 ciclos"""
        self.timer.cycles_completed = 4
        self.timer.start_break()
        
        self.assertEqual(self.timer.current_state, PomodoroState.LONG_BREAK)
        self.assertEqual(self.timer.time_remaining, 15)
        
    def test_stop_timer(self):
        """Teste unitário: parar timer"""
        self.timer.start_work_session()
        self.timer.stop()
        
        self.assertEqual(self.timer.current_state, PomodoroState.STOPPED)
        self.assertEqual(self.timer.time_remaining, 0)
        
    def test_get_status(self):
        """Teste unitário: obter status"""
        self.timer.start_work_session()
        status = self.timer.get_status()
        
        expected = {
            'state': 'work',
            'time_remaining': 10,
            'cycles_completed': 0
        }
        self.assertEqual(status, expected)

class TestPomodoroE2E(unittest.TestCase):
    """Testes End-to-End: fluxo completo do usuário"""
    
    def test_complete_pomodoro_workflow(self):
        """Teste E2E: fluxo completo de 2 ciclos Pomodoro"""
        timer = PomodoroTimer(work_duration=3, short_break=2, long_break=5)
        states_history = []
        
        def track_states(state, time_remaining):
            states_history.append(state.value)
            
        timer.set_state_change_callback(track_states)
        
        # Primeiro ciclo
        timer.start_work_session()
        for _ in range(3):
            timer.tick()
            
        # Pausa curta
        for _ in range(2):
            timer.tick()
            
        # Segundo ciclo
        timer.start_work_session()
        for _ in range(3):
            timer.tick()
            
        # Completar a segunda pausa
        for _ in range(2):
            timer.tick()
            
        expected_states = ['work', 'short_break', 'stopped', 'work', 'short_break', 'stopped']
        self.assertEqual(states_history, expected_states)
        self.assertEqual(timer.cycles_completed, 2)

if __name__ == '__main__':
    unittest.main()