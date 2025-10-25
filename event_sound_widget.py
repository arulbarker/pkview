"""
Event Sound Settings Widget
Allows configuring sounds for all TikTok events with on/off toggle
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QCheckBox, QGroupBox, QFileDialog,
                             QScrollArea, QFrame)
from PyQt6.QtCore import pyqtSignal
import json
import os


class EventSoundWidget(QWidget):
    """
    UI for configuring sounds for different events
    """

    sound_settings_changed = pyqtSignal(dict)  # sound settings

    def __init__(self, parent=None):
        super().__init__(parent)

        # Sound settings: {event_type: {enabled: bool, file: str}}
        self.sound_settings = {
            # Win sounds
            'team_a_win': {'enabled': True, 'file': 'sounds/team_a_win.mp3', 'label': '🏆 Team A Menang'},
            'team_b_win': {'enabled': True, 'file': 'sounds/team_b_win.mp3', 'label': '🏆 Team B Menang'},
            'round_end': {'enabled': True, 'file': 'sounds/round_end_warning.mp3', 'label': '⏱️ Round Habis (10 detik)'},

            # Event sounds
            'like': {'enabled': False, 'file': 'sounds/like.mp3', 'label': '❤️ Like'},
            'comment': {'enabled': False, 'file': 'sounds/comment.mp3', 'label': '💬 Comment'},
            'share': {'enabled': False, 'file': 'sounds/share.mp3', 'label': '📤 Share'},
            'follow': {'enabled': False, 'file': 'sounds/follow.mp3', 'label': '👤 Follow'},
            'join': {'enabled': False, 'file': 'sounds/join.mp3', 'label': '🚪 Join'},
            'gift': {'enabled': False, 'file': 'sounds/gift.mp3', 'label': '🎁 Gift'},
        }

        self.checkboxes = {}
        self.file_labels = {}

        self._setup_ui()
        self._load_settings()

    def _setup_ui(self):
        """Setup the sound settings UI"""
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("🔊 Pengaturan Suara Event")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        layout.addWidget(title)

        # Info
        info = QLabel("Atur suara untuk setiap event TikTok.\nOn/Off toggle dan pilih file MP3 kustom.")
        info.setStyleSheet("color: #aaa; font-size: 11px;")
        info.setWordWrap(True)
        layout.addWidget(info)

        layout.addSpacing(10)

        # Scroll area for all sound settings
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        # Win Sounds Group
        win_group = QGroupBox("🏆 Suara Kemenangan")
        win_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: white;
                border: 2px solid #555;
                border-radius: 8px;
                margin-top: 10px;
                padding: 15px;
            }
        """)
        win_layout = QVBoxLayout()

        for event_type in ['team_a_win', 'team_b_win', 'round_end']:
            sound_row = self._create_sound_row(event_type)
            win_layout.addWidget(sound_row)

        win_group.setLayout(win_layout)
        scroll_layout.addWidget(win_group)

        # Event Sounds Group
        event_group = QGroupBox("🎉 Suara Event")
        event_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: white;
                border: 2px solid #555;
                border-radius: 8px;
                margin-top: 10px;
                padding: 15px;
            }
        """)
        event_layout = QVBoxLayout()

        for event_type in ['like', 'comment', 'share', 'follow', 'join', 'gift']:
            sound_row = self._create_sound_row(event_type)
            event_layout.addWidget(sound_row)

        event_group.setLayout(event_layout)
        scroll_layout.addWidget(event_group)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

        # Save button
        save_btn = QPushButton("💾 Simpan Pengaturan")
        save_btn.clicked.connect(self._save_settings)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 12px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        layout.addWidget(save_btn)

    def _create_sound_row(self, event_type):
        """Create a row for sound settings"""
        row = QFrame()
        row.setFrameStyle(QFrame.Shape.StyledPanel)
        row.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 5px;
                padding: 5px;
                margin: 2px;
            }
        """)

        layout = QHBoxLayout(row)

        # Checkbox for on/off
        checkbox = QCheckBox(self.sound_settings[event_type]['label'])
        checkbox.setChecked(self.sound_settings[event_type]['enabled'])
        checkbox.setStyleSheet("color: white; font-size: 12px;")
        checkbox.toggled.connect(lambda checked, et=event_type: self._on_enabled_changed(et, checked))
        self.checkboxes[event_type] = checkbox
        layout.addWidget(checkbox, 2)

        # File label (shows file name)
        file_name = os.path.basename(self.sound_settings[event_type]['file'])
        file_label = QLabel(file_name)
        file_label.setStyleSheet("color: #aaa; font-size: 10px;")
        file_label.setWordWrap(False)
        self.file_labels[event_type] = file_label
        layout.addWidget(file_label, 3)

        # Browse button
        browse_btn = QPushButton("📁 Pilih")
        browse_btn.clicked.connect(lambda: self._browse_file(event_type))
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 10px;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        layout.addWidget(browse_btn, 1)

        return row

    def _on_enabled_changed(self, event_type, checked):
        """Handle enable/disable toggle"""
        self.sound_settings[event_type]['enabled'] = checked

    def _browse_file(self, event_type):
        """Browse for sound file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            f"Pilih File Suara untuk {self.sound_settings[event_type]['label']}",
            "sounds",
            "Audio Files (*.mp3 *.wav *.ogg);;All Files (*.*)"
        )

        if file_path:
            self.sound_settings[event_type]['file'] = file_path
            file_name = os.path.basename(file_path)
            self.file_labels[event_type].setText(file_name)
            print(f"✓ Suara dipilih untuk {event_type}: {file_name}")

    def _save_settings(self):
        """Save sound settings to file"""
        try:
            filepath = 'event_sounds.json'
            with open(filepath, 'w') as f:
                json.dump(self.sound_settings, f, indent=2)

            # Emit signal
            self.sound_settings_changed.emit(self.sound_settings)

            print(f"✓ Event sound settings saved!")
            enabled_count = sum(1 for s in self.sound_settings.values() if s['enabled'])
            print(f"  {enabled_count}/{len(self.sound_settings)} sounds enabled")

        except Exception as e:
            print(f"Error saving sound settings: {e}")

    def _load_settings(self):
        """Load sound settings from file"""
        try:
            filepath = 'event_sounds.json'
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    saved_settings = json.load(f)

                # Merge saved settings (preserve labels)
                for event_type, settings in saved_settings.items():
                    if event_type in self.sound_settings:
                        self.sound_settings[event_type]['enabled'] = settings.get('enabled', False)
                        self.sound_settings[event_type]['file'] = settings.get('file', self.sound_settings[event_type]['file'])

                # Update UI
                for event_type in self.sound_settings.keys():
                    if event_type in self.checkboxes:
                        self.checkboxes[event_type].setChecked(self.sound_settings[event_type]['enabled'])
                    if event_type in self.file_labels:
                        file_name = os.path.basename(self.sound_settings[event_type]['file'])
                        self.file_labels[event_type].setText(file_name)

                print(f"✓ Loaded event sound settings")
                enabled_count = sum(1 for s in self.sound_settings.values() if s['enabled'])
                print(f"  {enabled_count}/{len(self.sound_settings)} sounds enabled")

        except Exception as e:
            print(f"Error loading sound settings: {e}")

    def is_sound_enabled(self, event_type):
        """Check if sound is enabled for an event"""
        if event_type in self.sound_settings:
            return self.sound_settings[event_type]['enabled']
        return False

    def get_sound_file(self, event_type):
        """Get sound file path for an event"""
        if event_type in self.sound_settings:
            return self.sound_settings[event_type]['file']
        return None
