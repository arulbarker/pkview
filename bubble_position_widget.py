"""
Bubble Position Settings Widget
Allows configuring where like/comment bubbles appear
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QRadioButton, QButtonGroup, QGroupBox)
from PyQt6.QtCore import pyqtSignal
import json
import os


class BubblePositionWidget(QWidget):
    """
    UI for setting bubble positions for like/comment
    """

    position_changed = pyqtSignal(dict)  # {event_type: position}

    def __init__(self, parent=None):
        super().__init__(parent)

        # Positions: {'like': 'left', 'comment': 'right'}
        # Options: 'left', 'right', 'top', 'bottom'
        self.positions = {
            'like': 'top',      # Default
            'comment': 'top'    # Default
        }

        self._setup_ui()
        self._load_positions()

    def _setup_ui(self):
        """Setup the position settings UI"""
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("🫧 Posisi Bubble Like & Comment")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        layout.addWidget(title)

        # Info
        info = QLabel("Pilih dimana bubble like dan comment muncul.\n(Tidak akan muncul di tengah)")
        info.setStyleSheet("color: #aaa; font-size: 11px;")
        info.setWordWrap(True)
        layout.addWidget(info)

        layout.addSpacing(10)

        # Like Position
        like_group = QGroupBox("❤️ LIKE - Posisi Bubble")
        like_group.setStyleSheet("""
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
        like_layout = QVBoxLayout()

        self.like_button_group = QButtonGroup()

        positions = [
            ('top', '⬆️ Atas (Random horizontal)'),
            ('bottom', '⬇️ Bawah (Random horizontal)'),
            ('left', '⬅️ Kiri (Random vertical)'),
            ('right', '➡️ Kanan (Random vertical)')
        ]

        self.like_position_radios = {}
        for pos_key, pos_label in positions:
            radio = QRadioButton(pos_label)
            radio.setStyleSheet("color: white; font-size: 13px;")
            if pos_key == 'top':
                radio.setChecked(True)
            radio.toggled.connect(lambda checked, p=pos_key: self._on_like_position_changed(p, checked))
            self.like_button_group.addButton(radio)
            like_layout.addWidget(radio)
            self.like_position_radios[pos_key] = radio

        like_group.setLayout(like_layout)
        layout.addWidget(like_group)

        layout.addSpacing(10)

        # Comment Position
        comment_group = QGroupBox("💬 COMMENT - Posisi Bubble")
        comment_group.setStyleSheet("""
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
        comment_layout = QVBoxLayout()

        self.comment_button_group = QButtonGroup()

        self.comment_position_radios = {}
        for pos_key, pos_label in positions:
            radio = QRadioButton(pos_label)
            radio.setStyleSheet("color: white; font-size: 13px;")
            if pos_key == 'top':
                radio.setChecked(True)
            radio.toggled.connect(lambda checked, p=pos_key: self._on_comment_position_changed(p, checked))
            self.comment_button_group.addButton(radio)
            comment_layout.addWidget(radio)
            self.comment_position_radios[pos_key] = radio

        comment_group.setLayout(comment_layout)
        layout.addWidget(comment_group)

        layout.addSpacing(10)

        # Save button
        save_btn = QPushButton("💾 Simpan Posisi")
        save_btn.clicked.connect(self._save_positions)
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

        layout.addStretch()

    def _on_like_position_changed(self, position, checked):
        """Handle like position change"""
        if checked:
            self.positions['like'] = position

    def _on_comment_position_changed(self, position, checked):
        """Handle comment position change"""
        if checked:
            self.positions['comment'] = position

    def _save_positions(self):
        """Save positions to file"""
        try:
            filepath = 'bubble_positions.json'
            with open(filepath, 'w') as f:
                json.dump(self.positions, f, indent=2)

            # Emit signal
            self.position_changed.emit(self.positions)

            print(f"✓ Bubble positions saved!")
            print(f"  Like → {self.positions['like']}")
            print(f"  Comment → {self.positions['comment']}")

        except Exception as e:
            print(f"Error saving positions: {e}")

    def _load_positions(self):
        """Load positions from file"""
        try:
            filepath = 'bubble_positions.json'
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    saved_positions = json.load(f)

                # Apply saved positions
                if 'like' in saved_positions:
                    pos = saved_positions['like']
                    if pos in self.like_position_radios:
                        self.like_position_radios[pos].setChecked(True)

                if 'comment' in saved_positions:
                    pos = saved_positions['comment']
                    if pos in self.comment_position_radios:
                        self.comment_position_radios[pos].setChecked(True)

                self.positions = saved_positions
                print(f"✓ Loaded bubble positions")
                print(f"  Like → {self.positions['like']}")
                print(f"  Comment → {self.positions['comment']}")

        except Exception as e:
            print(f"Error loading positions: {e}")

    def get_position_for_event(self, event_type):
        """
        Get position for an event type

        Args:
            event_type: 'like' or 'comment'

        Returns:
            str: 'left', 'right', 'top', or 'bottom'
        """
        return self.positions.get(event_type, 'top')
