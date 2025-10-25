"""
Sound Manager - Win Effects and Audio
Handles sound playback for PK Battle events
"""

from PyQt6.QtCore import QObject, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import os


class SoundManager(QObject):
    """
    Manages sound effects for PK Battle
    """

    def __init__(self):
        super().__init__()

        # Sound enabled flag
        self.sound_enabled = True

        # Volume (0.0 to 1.0)
        self.volume = 0.8

        # Media players (one for each sound type to allow overlap)
        self.players = {}

        # Audio outputs
        self.audio_outputs = {}

        # Sound file paths
        self.sound_files = {
            'team_a_win': 'sounds/team_a_win.mp3',
            'team_b_win': 'sounds/team_b_win.mp3',
            'round_end_warning': 'sounds/round_end_warning.mp3',
            'final_win': 'sounds/final_win.mp3',
        }

        # Create sounds directory if it doesn't exist
        os.makedirs('sounds', exist_ok=True)

        # Initialize players
        self._init_players()

    def _init_players(self):
        """Initialize media players for each sound"""
        for sound_name in self.sound_files.keys():
            player = QMediaPlayer()
            audio_output = QAudioOutput()
            audio_output.setVolume(self.volume)

            player.setAudioOutput(audio_output)

            self.players[sound_name] = player
            self.audio_outputs[sound_name] = audio_output

    def play_team_win(self, team):
        """
        Play win sound for a team

        Args:
            team: 'A' or 'B'
        """
        if not self.sound_enabled:
            return

        sound_name = f'team_{team.lower()}_win'
        self._play_sound(sound_name)

    def play_round_end_warning(self):
        """Play warning sound at 10 seconds remaining"""
        if not self.sound_enabled:
            return

        self._play_sound('round_end_warning')

    def play_final_win(self):
        """Play final win celebration sound"""
        if not self.sound_enabled:
            return

        self._play_sound('final_win')

    def play_event_sound(self, event_type, sound_file):
        """
        Play sound for a specific event

        Args:
            event_type: Event type (like, comment, etc.)
            sound_file: Path to sound file
        """
        if not self.sound_enabled:
            return

        if not sound_file or not os.path.exists(sound_file):
            return

        # Create player if doesn't exist
        if event_type not in self.players:
            player = QMediaPlayer()
            audio_output = QAudioOutput()
            audio_output.setVolume(self.volume)
            player.setAudioOutput(audio_output)
            self.players[event_type] = player
            self.audio_outputs[event_type] = audio_output

        player = self.players[event_type]

        # Stop if already playing
        if player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            player.stop()

        # Set source and play
        url = QUrl.fromLocalFile(os.path.abspath(sound_file))
        player.setSource(url)
        player.play()

    def _play_sound(self, sound_name):
        """
        Play a specific sound

        Args:
            sound_name: Key in sound_files dict
        """
        if sound_name not in self.players:
            return

        filepath = self.sound_files.get(sound_name)
        if not filepath or not os.path.exists(filepath):
            # Sound file doesn't exist - create placeholder or skip
            print(f"Sound file not found: {filepath}")
            return

        player = self.players[sound_name]

        # Stop if already playing
        if player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            player.stop()

        # Set source and play
        url = QUrl.fromLocalFile(os.path.abspath(filepath))
        player.setSource(url)
        player.play()

    def set_volume(self, volume):
        """
        Set volume for all sounds

        Args:
            volume: Float 0.0 to 1.0
        """
        self.volume = max(0.0, min(1.0, volume))

        for audio_output in self.audio_outputs.values():
            audio_output.setVolume(self.volume)

    def set_enabled(self, enabled):
        """
        Enable or disable sound

        Args:
            enabled: Boolean
        """
        self.sound_enabled = enabled

    def stop_all(self):
        """Stop all playing sounds"""
        for player in self.players.values():
            if player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
                player.stop()

    def create_placeholder_sounds(self):
        """
        Create placeholder/beep sounds if actual sound files don't exist
        This is a helper for users who don't have sound files yet
        """
        # Note: Creating actual audio files would require additional libraries
        # For now, we'll just create empty files as placeholders

        for sound_name, filepath in self.sound_files.items():
            if not os.path.exists(filepath):
                # Create empty placeholder file
                with open(filepath, 'w') as f:
                    f.write('')  # Empty placeholder

                print(f"Created placeholder for: {filepath}")
                print(f"  → Replace with actual MP3 file for {sound_name}")
