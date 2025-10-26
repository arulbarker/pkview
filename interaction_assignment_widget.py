"""
Interaction Assignment Widget
Allows user to assign Like and Comment to Team A or Team B
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QRadioButton, QButtonGroup, QGroupBox)
from PyQt6.QtCore import Qt, pyqtSignal
import json
import os


class InteractionAssignmentWidget(QWidget):
    """
    UI for assigning likes and comments to teams
    """

    assignment_changed = pyqtSignal(dict)  # {interaction: team}

    def __init__(self, parent=None):
        super().__init__(parent)

        # Assignments: {'like': 'A', 'comment': 'B'}
        self.assignments = {
            'like': 'A',  # Default
            'comment': 'A'  # Default
        }

        self._setup_ui()
        self._load_assignments()

    def _setup_ui(self):
        """Setup the assignment UI"""
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("👍💬 Like & Comment Assignment")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        layout.addWidget(title)

        # Info
        info = QLabel("1 Like = 1 poin  |  1 Comment = 1 poin\nPilih tim mana yang dapat poin dari like dan comment.")
        info.setStyleSheet("color: #aaa; font-size: 11px;")
        info.setWordWrap(True)
        layout.addWidget(info)

        layout.addSpacing(10)

        # Like Assignment
        like_group = QGroupBox("❤️ LIKE")
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

        self.like_a_radio = QRadioButton("Team A (Merah)")
        self.like_a_radio.setStyleSheet("color: #FF6B6B; font-size: 13px;")
        self.like_a_radio.setChecked(True)
        self.like_a_radio.toggled.connect(lambda checked: self._on_like_changed('A', checked))
        self.like_button_group.addButton(self.like_a_radio)
        like_layout.addWidget(self.like_a_radio)

        self.like_b_radio = QRadioButton("Team B (Teal)")
        self.like_b_radio.setStyleSheet("color: #4ECDC4; font-size: 13px;")
        self.like_b_radio.toggled.connect(lambda checked: self._on_like_changed('B', checked))
        self.like_button_group.addButton(self.like_b_radio)
        like_layout.addWidget(self.like_b_radio)

        like_group.setLayout(like_layout)
        layout.addWidget(like_group)

        layout.addSpacing(10)

        # Comment Assignment
        comment_group = QGroupBox("💬 COMMENT")
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

        self.comment_a_radio = QRadioButton("Team A (Merah)")
        self.comment_a_radio.setStyleSheet("color: #FF6B6B; font-size: 13px;")
        self.comment_a_radio.setChecked(True)
        self.comment_a_radio.toggled.connect(lambda checked: self._on_comment_changed('A', checked))
        self.comment_button_group.addButton(self.comment_a_radio)
        comment_layout.addWidget(self.comment_a_radio)

        self.comment_b_radio = QRadioButton("Team B (Teal)")
        self.comment_b_radio.setStyleSheet("color: #4ECDC4; font-size: 13px;")
        self.comment_b_radio.toggled.connect(lambda checked: self._on_comment_changed('B', checked))
        self.comment_button_group.addButton(self.comment_b_radio)
        comment_layout.addWidget(self.comment_b_radio)

        comment_group.setLayout(comment_layout)
        layout.addWidget(comment_group)

        layout.addSpacing(10)

        # Quick buttons
        quick_layout = QHBoxLayout()

        all_a_btn = QPushButton("Semua → Team A")
        all_a_btn.clicked.connect(lambda: self._set_all('A'))
        all_a_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF6B6B;
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #FF5252; }
        """)
        quick_layout.addWidget(all_a_btn)

        all_b_btn = QPushButton("Semua → Team B")
        all_b_btn.clicked.connect(lambda: self._set_all('B'))
        all_b_btn.setStyleSheet("""
            QPushButton {
                background-color: #4ECDC4;
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #3DBDB3; }
        """)
        quick_layout.addWidget(all_b_btn)

        layout.addLayout(quick_layout)

        # Save button
        save_btn = QPushButton("💾 Simpan Assignment")
        save_btn.clicked.connect(self._save_assignments)
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

    def _on_like_changed(self, team, checked):
        """Handle like assignment change"""
        if checked:
            self.assignments['like'] = team

    def _on_comment_changed(self, team, checked):
        """Handle comment assignment change"""
        if checked:
            self.assignments['comment'] = team

    def _set_all(self, team):
        """Set all interactions to one team"""
        if team == 'A':
            self.like_a_radio.setChecked(True)
            self.comment_a_radio.setChecked(True)
        else:
            self.like_b_radio.setChecked(True)
            self.comment_b_radio.setChecked(True)

    def _save_assignments(self):
        """Save assignments to file"""
        try:
            filepath = 'interaction_assignment.json'
            with open(filepath, 'w') as f:
                json.dump(self.assignments, f, indent=2)

            # Emit signal
            self.assignment_changed.emit(self.assignments)

            print(f"[OK] Interaction assignments saved!")
            print(f"  Like -> Team {self.assignments['like']}")
            print(f"  Comment -> Team {self.assignments['comment']}")

        except Exception as e:
            print(f"Error saving assignments: {e}")

    def _load_assignments(self):
        """Load assignments from file"""
        try:
            filepath = 'interaction_assignment.json'
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    saved_assignments = json.load(f)

                # Apply saved assignments
                if 'like' in saved_assignments:
                    if saved_assignments['like'] == 'A':
                        self.like_a_radio.setChecked(True)
                    else:
                        self.like_b_radio.setChecked(True)

                if 'comment' in saved_assignments:
                    if saved_assignments['comment'] == 'A':
                        self.comment_a_radio.setChecked(True)
                    else:
                        self.comment_b_radio.setChecked(True)

                self.assignments = saved_assignments
                print(f"[OK] Loaded interaction assignments")
                print(f"  Like -> Team {self.assignments['like']}")
                print(f"  Comment -> Team {self.assignments['comment']}")

                # Note: Do NOT emit here - main window will manually trigger after signal connected
                # This prevents race condition where signal is emitted before anyone is listening

        except Exception as e:
            print(f"Error loading assignments: {e}")

    def get_team_for_interaction(self, interaction_type):
        """
        Get which team an interaction is assigned to

        Args:
            interaction_type: 'like' or 'comment'

        Returns:
            str: 'A' or 'B', defaults to 'A' if not found
        """
        return self.assignments.get(interaction_type, 'A')
