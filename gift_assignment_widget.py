"""
Gift Assignment Widget
Allows user to assign TikTok gifts to Team A or Team B
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QScrollArea, QLineEdit, QRadioButton,
                             QButtonGroup, QGroupBox)
from PyQt6.QtCore import Qt, pyqtSignal
import json
import os


class GiftAssignmentWidget(QWidget):
    """
    UI for assigning gifts to teams
    """

    assignment_changed = pyqtSignal(dict)  # gift_name -> team ('A' or 'B')

    def __init__(self, parent=None):
        super().__init__(parent)

        # Gift assignments: {gift_name: 'A' or 'B'}
        self.assignments = {}

        # Load all TikTok gifts from gift_tiers
        self._load_gifts()

        # Setup UI
        self._setup_ui()

        # Load saved assignments
        self._load_assignments()

    def _load_gifts(self):
        """Load all TikTok gifts from gift_tiers"""
        from gift_tiers import TIKTOK_GIFT_VALUES

        self.all_gifts = []
        for gift_name, coin_value in TIKTOK_GIFT_VALUES.items():
            self.all_gifts.append({
                'name': gift_name,
                'coins': coin_value
            })

        # Sort by coin value
        self.all_gifts.sort(key=lambda x: x['coins'])

    def _setup_ui(self):
        """Setup the assignment UI"""
        layout = QVBoxLayout(self)

        # Title
        title = QLabel(f"🎁 Gift Assignment ({len(self.all_gifts)} Gifts)")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        layout.addWidget(title)

        # Info
        info = QLabel("Assign each gift to Team A or Team B. Gifts add points based on coin value × 5.")
        info.setStyleSheet("color: #aaa; font-size: 11px;")
        info.setWordWrap(True)
        layout.addWidget(info)

        # Search box
        search_layout = QHBoxLayout()
        search_label = QLabel("🔍 Search:")
        search_layout.addWidget(search_label)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Filter gifts by name...")
        self.search_input.textChanged.connect(self._filter_gifts)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Quick assign buttons
        quick_layout = QHBoxLayout()

        assign_all_a_btn = QPushButton("Assign All → Team A")
        assign_all_a_btn.clicked.connect(lambda: self._assign_all('A'))
        assign_all_a_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF6B6B;
                color: white;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover { background-color: #FF5252; }
        """)
        quick_layout.addWidget(assign_all_a_btn)

        assign_all_b_btn = QPushButton("Assign All → Team B")
        assign_all_b_btn.clicked.connect(lambda: self._assign_all('B'))
        assign_all_b_btn.setStyleSheet("""
            QPushButton {
                background-color: #4ECDC4;
                color: white;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover { background-color: #3DBDB3; }
        """)
        quick_layout.addWidget(assign_all_b_btn)

        split_btn = QPushButton("Split 50-50")
        split_btn.clicked.connect(self._split_fifty_fifty)
        split_btn.setStyleSheet("""
            QPushButton {
                background-color: #9B59B6;
                color: white;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover { background-color: #8E44AD; }
        """)
        quick_layout.addWidget(split_btn)

        layout.addLayout(quick_layout)

        # Scrollable gift list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(400)

        scroll_widget = QWidget()
        self.gift_list_layout = QVBoxLayout(scroll_widget)
        self.gift_list_layout.setSpacing(5)

        # Create gift rows
        self.gift_widgets = []
        for gift in self.all_gifts:
            gift_widget = self._create_gift_row(gift)
            self.gift_widgets.append(gift_widget)
            self.gift_list_layout.addWidget(gift_widget)

        self.gift_list_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

        # Save button
        save_btn = QPushButton("💾 Save Gift Assignment")
        save_btn.clicked.connect(self._save_assignments)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        layout.addWidget(save_btn)

    def _create_gift_row(self, gift):
        """
        Create a single gift assignment row

        Args:
            gift: Gift dict with 'name' and 'coins'

        Returns:
            QWidget: Gift row widget
        """
        widget = QWidget()
        widget.gift_data = gift  # Store for filtering
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)

        # Gift name
        name_label = QLabel(gift['name'])
        name_label.setMinimumWidth(150)
        name_label.setStyleSheet("color: white; font-weight: bold;")
        layout.addWidget(name_label)

        # Coin value
        coins_label = QLabel(f"{gift['coins']:,} coins")
        coins_label.setMinimumWidth(100)
        coins_label.setStyleSheet("color: #FFD700;")
        layout.addWidget(coins_label)

        # Points (coins × 5)
        points = gift['coins'] * 5
        points_label = QLabel(f"= {points:,} pts")
        points_label.setMinimumWidth(100)
        points_label.setStyleSheet("color: #4CAF50;")
        layout.addWidget(points_label)

        layout.addStretch()

        # Team selection radio buttons
        button_group = QButtonGroup(widget)

        radio_a = QRadioButton("Team A")
        radio_a.setStyleSheet("color: #FF6B6B;")
        radio_a.toggled.connect(lambda checked: self._on_assignment_changed(gift['name'], 'A', checked))
        button_group.addButton(radio_a)
        layout.addWidget(radio_a)

        radio_b = QRadioButton("Team B")
        radio_b.setStyleSheet("color: #4ECDC4;")
        radio_b.toggled.connect(lambda checked: self._on_assignment_changed(gift['name'], 'B', checked))
        button_group.addButton(radio_b)
        layout.addWidget(radio_b)

        # Store references
        widget.radio_a = radio_a
        widget.radio_b = radio_b
        widget.button_group = button_group

        # Set default to Team A
        radio_a.setChecked(True)

        # Styling
        widget.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                border-radius: 5px;
            }
            QWidget:hover {
                background-color: #333333;
            }
        """)

        return widget

    def _on_assignment_changed(self, gift_name, team, checked):
        """Handle assignment change"""
        if checked:
            self.assignments[gift_name] = team

    def _filter_gifts(self, search_text):
        """Filter gift list by search text"""
        search_text = search_text.lower()

        for widget in self.gift_widgets:
            gift_name = widget.gift_data['name'].lower()
            if search_text in gift_name:
                widget.show()
            else:
                widget.hide()

    def _assign_all(self, team):
        """
        Assign all gifts to a team

        Args:
            team: 'A' or 'B'
        """
        for widget in self.gift_widgets:
            if team == 'A':
                widget.radio_a.setChecked(True)
            else:
                widget.radio_b.setChecked(True)

    def _split_fifty_fifty(self):
        """Split gifts 50-50 between teams"""
        for i, widget in enumerate(self.gift_widgets):
            if i % 2 == 0:
                widget.radio_a.setChecked(True)
            else:
                widget.radio_b.setChecked(True)

    def _save_assignments(self):
        """Save assignments to file"""
        try:
            filepath = 'gift_assignment.json'
            with open(filepath, 'w') as f:
                json.dump(self.assignments, f, indent=2)

            # Emit signal
            self.assignment_changed.emit(self.assignments)

            # Visual feedback (could add a message box here)
            print(f"✓ Gift assignments saved! ({len(self.assignments)} gifts)")

        except Exception as e:
            print(f"Error saving assignments: {e}")

    def _load_assignments(self):
        """Load assignments from file"""
        try:
            filepath = 'gift_assignment.json'
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    saved_assignments = json.load(f)

                # Apply saved assignments
                for widget in self.gift_widgets:
                    gift_name = widget.gift_data['name']
                    if gift_name in saved_assignments:
                        team = saved_assignments[gift_name]
                        if team == 'A':
                            widget.radio_a.setChecked(True)
                        else:
                            widget.radio_b.setChecked(True)

                self.assignments = saved_assignments
                print(f"✓ Loaded {len(saved_assignments)} gift assignments")

        except Exception as e:
            print(f"Error loading assignments: {e}")

    def get_team_for_gift(self, gift_name):
        """
        Get which team a gift is assigned to

        Args:
            gift_name: Name of the gift

        Returns:
            str: 'A' or 'B', defaults to 'A' if not found
        """
        return self.assignments.get(gift_name, 'A')
