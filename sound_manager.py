"""
Sound Manager - Win Effects and Audio
Handles sound playback for PK Battle events
One player per event type - no overlap within same type
"""

from PyQt6.QtCore import QObject, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import os


class SoundManager(QObject):
    """
    Manages sound effects for PK Battle
    One player per event type - plays to completion before accepting new trigger
    Different event types can play simultaneously
    """

    def __init__(self):
        super().__init__()

        # Sound enabled flag
        self.sound_enabled = True

        # Volume (0.0 to 1.0)
        self.volume = 0.8

        # Single player per event type
        self.players = {}
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

        # Initialize players for predefined sounds
        self._init_players()

    def _init_players(self):
        """Initialize media players for predefined sounds"""
        for sound_name in self.sound_files.keys():
            player = QMediaPlayer()
            audio_output = QAudioOutput()
            audio_output.setVolume(self.volume)
            player.setAudioOutput(audio_output)

            self.players[sound_name] = player
            self.audio_outputs[sound_name] = audio_output

    def _create_player_for_event(self, event_type):
        """
        Create player for event type if doesn't exist

        Args:
            event_type: Event type (like, comment, gift, etc.)
        """
        if event_type not in self.players:
            player = QMediaPlayer()
            audio_output = QAudioOutput()
            audio_output.setVolume(self.volume)
            player.setAudioOutput(audio_output)

            self.players[event_type] = player
            self.audio_outputs[event_type] = audio_output

    def set_win_sound_file(self, team, filepath):
        """
        Set custom win sound file for a team

        Args:
            team: 'A' or 'B'
            filepath: Path to the sound file
        """
        sound_name = f'team_{team.lower()}_win'
        if os.path.exists(filepath):
            self.sound_files[sound_name] = filepath
            print(f"[OK] Win sound for Team {team} set to: {os.path.basename(filepath)}")
        else:
            print(f"[WARNING] Sound file not found: {filepath}")

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
        ONLY plays if no sound is currently playing for this event type

        Args:
            event_type: Event type (like, comment, gift, etc.)
            sound_file: Path to sound file
        """
        if not self.sound_enabled:
            return

        if not sound_file or not os.path.exists(sound_file):
            return

        # Check file size
        if os.path.getsize(sound_file) < 100:  # Less than 100 bytes = invalid
            return

        # Create player if doesn't exist
        self._create_player_for_event(event_type)

        player = self.players[event_type]

        # CRITICAL: Skip if already playing
        # Sound must finish before accepting new trigger
        if player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            # Skip this sound - wait for current sound to finish
            return

        # Player is idle - safe to play new sound
        url = QUrl.fromLocalFile(os.path.abspath(sound_file))
        player.setSource(url)
        player.play()

    def _play_sound(self, sound_name):
        """
        Play a specific sound from sound_files

        Args:
            sound_name: Key in sound_files dict
        """
        filepath = self.sound_files.get(sound_name)
        if not filepath or not os.path.exists(filepath):
            # Sound file doesn't exist - skip silently
            return

        # Check if file is empty (placeholder file)
        if os.path.getsize(filepath) < 100:  # Less than 100 bytes = invalid MP3
            # Empty placeholder, skip silently
            return

        if sound_name not in self.players:
            return

        player = self.players[sound_name]

        # CRITICAL: Skip if already playing
        # Sound must finish before accepting new trigger
        if player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            return

        # Player is idle - safe to play
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
        Check for missing sound files and report them
        This is a helper for users who don't have sound files yet
        """
        # Don't create empty files - they cause FFmpeg errors
        # Just report missing files

        missing_files = []
        for sound_name, filepath in self.sound_files.items():
            if not os.path.exists(filepath):
                missing_files.append((sound_name, filepath))

        if missing_files:
            print("\n[WARNING] Missing sound files (sounds will be muted):")
            for sound_name, filepath in missing_files:
                print(f"  - {filepath} ({sound_name})")
            print("\n[TIP] To enable sounds:")
            print("  1. Add MP3 files to the 'sounds' folder")
            print("  2. Make sure files are valid MP3 format (not empty)\n")

    def is_playing(self, event_type):
        """
        Check if a sound is currently playing for an event type

        Args:
            event_type: Event type to check

        Returns:
            bool: True if playing, False otherwise
        """
        if event_type not in self.players:
            return False

        player = self.players[event_type]
        return player.playbackState() == QMediaPlayer.PlaybackState.PlayingState
