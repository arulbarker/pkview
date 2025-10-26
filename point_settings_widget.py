"""
Point Settings Widget
Allows user to customize points for Like and Comment
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QSpinBox, QGroupBox)
from PyQt6.QtCore import pyqtSignal
import json
import os


class PointSettingsWidget(QWidget):
    """
    UI for configuring custom points for interactions
    """

    point_settings_changed = pyqtSignal(dict)  # {interaction: points}

    def __init__(self, parent=None):
        super().__init__(parent)

        # Point settings: {'like': 1, 'comment': 1}
        self.point_values = {
            'like': 1,      # Default
            'comment': 1    # Default
        }

        self._setup_ui()
        self._load_settings()

    def _setup_ui(self):
        """Setup the point settings UI"""
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("🎯 Custom Point Settings")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        layout.addWidget(title)

        # Info
        info = QLabel("Atur berapa poin untuk setiap Like dan Comment.\nDefault: 1 Like = 1 poin, 1 Comment = 1 poin")
        info.setStyleSheet("color: #aaa; font-size: 11px;")
        info.setWordWrap(True)
        layout.addWidget(info)

        layout.addSpacing(10)

        # Like Points
        like_group = QGroupBox("❤️ LIKE - Custom Points")
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
        like_layout = QHBoxLayout()

        like_label = QLabel("1 Like =")
        like_label.setStyleSheet("color: white; font-size: 13px;")
        like_layout.addWidget(like_label)

        self.like_spinbox = QSpinBox()
        self.like_spinbox.setMinimum(1)
        self.like_spinbox.setMaximum(1000)
        self.like_spinbox.setValue(1)
        self.like_spinbox.setSuffix(" poin")
        self.like_spinbox.setStyleSheet("""
            QSpinBox {
                background-color: #2b2b2b;
                color: white;
                border: 2px solid #FF6B6B;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #FF6B6B;
                border-radius: 3px;
            }
        """)
        self.like_spinbox.valueChanged.connect(lambda val: self._on_like_changed(val))
        like_layout.addWidget(self.like_spinbox)

        like_layout.addStretch()
        like_group.setLayout(like_layout)
        layout.addWidget(like_group)

        layout.addSpacing(10)

        # Comment Points
        comment_group = QGroupBox("💬 COMMENT - Custom Points")
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
        comment_layout = QHBoxLayout()

        comment_label = QLabel("1 Comment =")
        comment_label.setStyleSheet("color: white; font-size: 13px;")
        comment_layout.addWidget(comment_label)

        self.comment_spinbox = QSpinBox()
        self.comment_spinbox.setMinimum(1)
        self.comment_spinbox.setMaximum(1000)
        self.comment_spinbox.setValue(1)
        self.comment_spinbox.setSuffix(" poin")
        self.comment_spinbox.setStyleSheet("""
            QSpinBox {
                background-color: #2b2b2b;
                color: white;
                border: 2px solid #4ECDC4;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #4ECDC4;
                border-radius: 3px;
            }
        """)
        self.comment_spinbox.valueChanged.connect(lambda val: self._on_comment_changed(val))
        comment_layout.addWidget(self.comment_spinbox)

        comment_layout.addStretch()
        comment_group.setLayout(comment_layout)
        layout.addWidget(comment_group)

        layout.addSpacing(10)

        # Quick presets
        preset_label = QLabel("⚡ Quick Presets:")
        preset_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        layout.addWidget(preset_label)

        preset_layout = QHBoxLayout()

        # Preset 1:1
        preset_1_btn = QPushButton("1:1 (Default)")
        preset_1_btn.clicked.connect(lambda: self._apply_preset(1, 1))
        preset_1_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-size: 11px;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        preset_layout.addWidget(preset_1_btn)

        # Preset 5:10
        preset_2_btn = QPushButton("5:10 (Like x5, Comment x10)")
        preset_2_btn.clicked.connect(lambda: self._apply_preset(5, 10))
        preset_2_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-size: 11px;
            }
            QPushButton:hover { background-color: #0b7dda; }
        """)
        preset_layout.addWidget(preset_2_btn)

        # Preset 10:50
        preset_3_btn = QPushButton("10:50 (Like x10, Comment x50)")
        preset_3_btn.clicked.connect(lambda: self._apply_preset(10, 50))
        preset_3_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-size: 11px;
            }
            QPushButton:hover { background-color: #e68900; }
        """)
        preset_layout.addWidget(preset_3_btn)

        layout.addLayout(preset_layout)

        # Save button
        save_btn = QPushButton("💾 Simpan Point Settings")
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

        layout.addStretch()

    def _on_like_changed(self, value):
        """Handle like points change"""
        self.point_values['like'] = value

    def _on_comment_changed(self, value):
        """Handle comment points change"""
        self.point_values['comment'] = value

    def _apply_preset(self, like_points, comment_points):
        """Apply a preset configuration"""
        self.like_spinbox.setValue(like_points)
        self.comment_spinbox.setValue(comment_points)

    def _save_settings(self):
        """Save point settings to file"""
        try:
            filepath = 'point_settings.json'
            with open(filepath, 'w') as f:
                json.dump(self.point_values, f, indent=2)

            # Emit signal
            self.point_settings_changed.emit(self.point_values)

            print(f"[OK] Point settings saved!")
            print(f"  1 Like = {self.point_values['like']} poin")
            print(f"  1 Comment = {self.point_values['comment']} poin")

        except Exception as e:
            print(f"Error saving point settings: {e}")

    def _load_settings(self):
        """Load point settings from file"""
        try:
            filepath = 'point_settings.json'
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    saved_settings = json.load(f)

                # Apply saved settings
                if 'like' in saved_settings:
                    self.like_spinbox.setValue(saved_settings['like'])

                if 'comment' in saved_settings:
                    self.comment_spinbox.setValue(saved_settings['comment'])

                self.point_values = saved_settings
                print(f"[OK] Loaded point settings")
                print(f"  1 Like = {self.point_values['like']} poin")
                print(f"  1 Comment = {self.point_values['comment']} poin")

                # Note: Do NOT emit here - main window will manually trigger after signal connected

        except Exception as e:
            print(f"Error loading point settings: {e}")

    def get_points_for_interaction(self, interaction_type):
        """
        Get point value for an interaction

        Args:
            interaction_type: 'like' or 'comment'

        Returns:
            int: Point value (default 1)
        """
        return self.point_values.get(interaction_type, 1)
