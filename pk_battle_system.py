"""
PK Battle System - TikTok Style Battle Mode
Handles scoring, timer, rounds, and win detection
"""

from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from datetime import datetime, timedelta


class PKBattleSystem(QObject):
    """
    PK Battle System - Soccer-style round scoring
    """

    # Signals
    points_updated = pyqtSignal(str, int)  # team ('A' or 'B'), new_points
    score_updated = pyqtSignal(int, int)  # team_a_score, team_b_score
    timer_updated = pyqtSignal(int)  # seconds_remaining
    round_won = pyqtSignal(str)  # winning_team ('A' or 'B')
    round_reset = pyqtSignal()

    def __init__(self, round_duration_minutes=60):
        super().__init__()

        # Score tracking (like soccer score: 2-1)
        self.team_a_score = 0  # How many rounds Team A won
        self.team_b_score = 0  # How many rounds Team B won

        # Points tracking (current round)
        self.team_a_points = 0
        self.team_b_points = 0

        # Timer settings
        self.round_duration_minutes = round_duration_minutes
        self.round_duration_seconds = round_duration_minutes * 60
        self.seconds_remaining = self.round_duration_seconds

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self._on_timer_tick)
        self.is_running = False

        # Point multiplier (1 coin = 5 points)
        self.point_multiplier = 5

    def start_battle(self):
        """Start the PK battle timer"""
        if not self.is_running:
            self.is_running = True
            self.timer.start(1000)  # Tick every second

    def pause_battle(self):
        """Pause the battle timer"""
        if self.is_running:
            self.is_running = False
            self.timer.stop()

    def resume_battle(self):
        """Resume the battle timer"""
        if not self.is_running:
            self.is_running = True
            self.timer.start(1000)

    def _on_timer_tick(self):
        """Called every second"""
        if self.seconds_remaining > 0:
            self.seconds_remaining -= 1
            self.timer_updated.emit(self.seconds_remaining)

            # Warning at 10 seconds
            if self.seconds_remaining == 10:
                # Could emit a warning signal here for sound effect
                pass
        else:
            # Time's up! Determine winner
            self._round_ended()

    def _round_ended(self):
        """Called when round timer reaches 0"""
        self.timer.stop()
        self.is_running = False

        # Determine winner based on points
        if self.team_a_points > self.team_b_points:
            winner = 'A'
            self.team_a_score += 1
        elif self.team_b_points > self.team_a_points:
            winner = 'B'
            self.team_b_score += 1
        else:
            # Draw - no score change
            winner = 'DRAW'

        # Emit signals
        if winner != 'DRAW':
            self.round_won.emit(winner)
            self.score_updated.emit(self.team_a_score, self.team_b_score)

        # Wait 5 seconds before auto-reset (show win effects)
        QTimer.singleShot(5000, self._reset_round)

    def _reset_round(self):
        """Reset points and timer for next round"""
        # Reset points to 0
        self.team_a_points = 0
        self.team_b_points = 0
        self.points_updated.emit('A', 0)
        self.points_updated.emit('B', 0)

        # Reset timer
        self.seconds_remaining = self.round_duration_seconds
        self.timer_updated.emit(self.seconds_remaining)

        # Emit reset signal
        self.round_reset.emit()

        # Auto-start next round
        self.start_battle()

    def add_gift_points(self, team, gift_coins):
        """
        Add points to a team based on gift value

        Args:
            team: 'A' or 'B'
            gift_coins: Coin value of the gift
        """
        points = gift_coins * self.point_multiplier

        if team == 'A':
            self.team_a_points += points
            self.points_updated.emit('A', self.team_a_points)
        elif team == 'B':
            self.team_b_points += points
            self.points_updated.emit('B', self.team_b_points)

    def add_interaction_points(self, team, count=1, points_per_interaction=1):
        """
        Add points for like/comment interactions

        Args:
            team: 'A' or 'B'
            count: Number of likes/comments (default 1)
            points_per_interaction: How many points per interaction (default 1)
        """
        points = count * points_per_interaction

        if team == 'A':
            self.team_a_points += points
            self.points_updated.emit('A', self.team_a_points)
        elif team == 'B':
            self.team_b_points += points
            self.points_updated.emit('B', self.team_b_points)

    def get_points_percentage(self):
        """
        Get percentage for bar visualization

        Returns:
            tuple: (team_a_percentage, team_b_percentage)
        """
        total = self.team_a_points + self.team_b_points

        if total == 0:
            return (50, 50)  # Equal when no points

        team_a_pct = (self.team_a_points / total) * 100
        team_b_pct = (self.team_b_points / total) * 100

        return (team_a_pct, team_b_pct)

    def get_timer_display(self):
        """
        Get formatted timer string

        Returns:
            str: "MM:SS" format
        """
        minutes = self.seconds_remaining // 60
        seconds = self.seconds_remaining % 60
        return f"{minutes:02d}:{seconds:02d}"

    def set_round_duration(self, minutes):
        """
        Set round duration

        Args:
            minutes: Duration in minutes
        """
        self.round_duration_minutes = minutes
        self.round_duration_seconds = minutes * 60

        # Reset timer if not running
        if not self.is_running:
            self.seconds_remaining = self.round_duration_seconds
            self.timer_updated.emit(self.seconds_remaining)

    def reset_all(self):
        """Reset everything (scores, points, timer)"""
        self.timer.stop()
        self.is_running = False

        # Reset scores
        self.team_a_score = 0
        self.team_b_score = 0
        self.score_updated.emit(0, 0)

        # Reset points
        self.team_a_points = 0
        self.team_b_points = 0
        self.points_updated.emit('A', 0)
        self.points_updated.emit('B', 0)

        # Reset timer
        self.seconds_remaining = self.round_duration_seconds
        self.timer_updated.emit(self.seconds_remaining)

    def get_current_state(self):
        """
        Get current battle state

        Returns:
            dict: Current state info
        """
        return {
            'team_a_score': self.team_a_score,
            'team_b_score': self.team_b_score,
            'team_a_points': self.team_a_points,
            'team_b_points': self.team_b_points,
            'seconds_remaining': self.seconds_remaining,
            'is_running': self.is_running,
            'timer_display': self.get_timer_display(),
            'percentages': self.get_points_percentage()
        }
