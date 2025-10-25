"""
PK Main Window - TikTok Style Battle Interface
Vertical layout for PK battle with bubble zones
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFrame, QSplitter, QGroupBox,
                             QTextEdit, QLineEdit, QSpinBox, QSlider, QCheckBox,
                             QTabWidget)
from PyQt6.QtCore import Qt, QTimer, pyqtSlot, QRect
from PyQt6.QtGui import QPainter, QColor, QLinearGradient, QPen, QFont
import config
from bubble_widget import BubbleWidget
from pk_battle_system import PKBattleSystem
from photo_manager import DraggablePhoto, PhotoUploadWidget
from gift_assignment_widget import GiftAssignmentWidget
from interaction_assignment_widget import InteractionAssignmentWidget
from bubble_position_widget import BubblePositionWidget
from event_sound_widget import EventSoundWidget
from draggable_label import DraggableLabel, DraggableMultiLineLabel
from sound_manager import SoundManager
from tiktok_handler import TikTokHandler, TikTokThread
import random


class PKMainWindow(QMainWindow):
    """
    Main PK Battle Window
    Vertical layout: TOP bubbles | CENTER battle | BOTTOM bubbles
    """

    def __init__(self):
        super().__init__()

        # Initialize systems
        self.pk_system = PKBattleSystem(round_duration_minutes=60)
        self.sound_manager = SoundManager()
        self.tiktok_handler = TikTokHandler()
        self.tiktok_thread = None

        # Bubble tracking
        self.active_bubbles = []

        # Gift assignment
        self.gift_assignments = {}  # Will be loaded from GiftAssignmentWidget

        # Interaction assignment (like/comment)
        self.interaction_assignments = {
            'like': 'A',     # Default: Like goes to Team A
            'comment': 'A'   # Default: Comment goes to Team A
        }

        # Bubble positions (like/comment bubble placement)
        self.bubble_positions = {
            'like': 'top',      # Default: top
            'comment': 'top'    # Default: top
        }

        # Event sound settings
        self.event_sound_settings = {}

        self._setup_ui()
        self._connect_signals()
        self._show_welcome_message()

        # Create placeholder sounds
        self.sound_manager.create_placeholder_sounds()

    def _setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle("PK Battle Mode - TikTok Live")
        self.setGeometry(100, 100, 1920, 1080)

        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Main layout - horizontal split
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # LEFT: Battle Display (vertical layout)
        self.battle_container = self._create_battle_display()
        splitter.addWidget(self.battle_container)

        # RIGHT: Control Panel
        control_panel = self._create_control_panel()
        splitter.addWidget(control_panel)

        # Set sizes (80% battle, 20% controls)
        splitter.setSizes([int(1920 * 0.8), int(1920 * 0.2)])

        main_layout.addWidget(splitter)

        # Apply dark theme
        self._apply_theme()

    def _create_battle_display(self):
        """Create the main battle display area with vertical layout"""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2e, stop:0.5 #16213e, stop:1 #0f3460);
                border: none;
            }
        """)
        container.setMinimumSize(1400, 1000)

        # Use absolute positioning for zones
        # We'll create overlay widgets

        # TOP Bubble Zone
        self.top_bubble_zone = QWidget(container)
        self.top_bubble_zone.setGeometry(0, 0, 1536, 200)
        self.top_bubble_zone.setStyleSheet("background: transparent;")

        # CENTER PK Battle View
        self.center_pk_view = QWidget(container)
        self.center_pk_view.setGeometry(0, 200, 1536, 600)
        self.center_pk_view.setStyleSheet("background: transparent;")

        # Create PK view components
        self._create_pk_view_components()

        # BOTTOM Bubble Zone
        self.bottom_bubble_zone = QWidget(container)
        self.bottom_bubble_zone.setGeometry(0, 800, 1536, 200)
        self.bottom_bubble_zone.setStyleSheet("background: transparent;")

        return container

    def _create_pk_view_components(self):
        """Create PK battle view components in center zone - VERTICAL LAYOUT"""
        # Score display at top (DRAGGABLE, ROTATABLE, RESIZABLE!)
        self.score_label = DraggableLabel(self.center_pk_view, "TEAM A  [0] - [0]  TEAM B", font_size=42)
        self.score_label.setGeometry(500, 10, 600, 80)
        self.score_label.min_width = 300
        self.score_label.max_width = 1000
        self.score_label.min_height = 60
        self.score_label.max_height = 150
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Timer (DRAGGABLE, ROTATABLE, RESIZABLE!)
        self.timer_label = DraggableLabel(
            self.center_pk_view,
            "Waktu: 60:00",
            font_size=28,
            text_color="#FFD700",  # Gold
            bg_color="rgba(0, 0, 0, 180)",
            border_color="rgba(255, 215, 0, 150)"
        )
        self.timer_label.setGeometry(650, 100, 300, 50)
        self.timer_label.min_width = 200
        self.timer_label.max_width = 500
        self.timer_label.min_height = 40
        self.timer_label.max_height = 100
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # VERTICAL LAYOUT: Team A Photo (TOP)
        self.photo_a = DraggablePhoto(self.center_pk_view, team='A', default_size=350)
        self.photo_a.move(600, 170)

        # Team A Points (DRAGGABLE, ROTATABLE, RESIZABLE!)
        self.points_a_label = DraggableLabel(
            self.center_pk_view,
            "0 poin",
            font_size=32,
            text_color="#FF6B6B",  # Red
            bg_color="rgba(255, 107, 107, 0.3)",
            border_color="#FF6B6B"
        )
        self.points_a_label.setGeometry(500, 540, 300, 60)
        self.points_a_label.min_width = 150
        self.points_a_label.max_width = 500
        self.points_a_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # VS Label (center separator)
        vs_label = QLabel(self.center_pk_view)
        vs_label.setGeometry(700, 610, 100, 50)
        vs_label.setText("VS")
        vs_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vs_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 36px;
                font-weight: bold;
            }
        """)

        # Team B Points (DRAGGABLE, ROTATABLE, RESIZABLE!)
        self.points_b_label = DraggableLabel(
            self.center_pk_view,
            "0 poin",
            font_size=32,
            text_color="#4ECDC4",  # Teal
            bg_color="rgba(78, 205, 196, 0.3)",
            border_color="#4ECDC4"
        )
        self.points_b_label.setGeometry(900, 540, 300, 60)
        self.points_b_label.min_width = 150
        self.points_b_label.max_width = 500
        self.points_b_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # VERTICAL LAYOUT: Team B Photo (BOTTOM of points)
        # Actually let's put it side by side with A for horizontal window
        self.photo_b = DraggablePhoto(self.center_pk_view, team='B', default_size=350)
        self.photo_b.move(900, 170)

        # Progress Bar (show real points, not percentage!)
        self.progress_bar = PKProgressBar(self.center_pk_view)
        self.progress_bar.setGeometry(400, 680, 900, 80)

    def _create_control_panel(self):
        """Create the control panel with tabs"""
        panel = QWidget()
        panel.setMaximumWidth(450)
        panel.setMinimumWidth(350)

        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Tabs
        tabs = QTabWidget()

        # Tab 1: Battle Controls
        battle_tab = self._create_battle_controls()
        tabs.addTab(battle_tab, "⚔️ Battle")

        # Tab 2: TikTok Connection
        tiktok_tab = self._create_tiktok_controls()
        tabs.addTab(tiktok_tab, "📺 TikTok")

        # Tab 3: Photos
        photos_tab = PhotoUploadWidget()
        photos_tab.photo_loaded.connect(self._on_photo_loaded)
        tabs.addTab(photos_tab, "📸 Photos")

        # Tab 4: Gift Assignment
        self.gift_assignment_widget = GiftAssignmentWidget()
        self.gift_assignment_widget.assignment_changed.connect(self._on_gift_assignment_changed)
        tabs.addTab(self.gift_assignment_widget, "🎁 Gifts")

        # Tab 5: Like/Comment Assignment
        self.interaction_assignment_widget = InteractionAssignmentWidget()
        self.interaction_assignment_widget.assignment_changed.connect(self._on_interaction_assignment_changed)
        tabs.addTab(self.interaction_assignment_widget, "👍💬 Like/Comment")

        # Tab 6: Bubble Position
        self.bubble_position_widget = BubblePositionWidget()
        self.bubble_position_widget.position_changed.connect(self._on_bubble_position_changed)
        tabs.addTab(self.bubble_position_widget, "🫧 Posisi Bubble")

        # Tab 7: Event Sounds
        self.event_sound_widget = EventSoundWidget()
        self.event_sound_widget.sound_settings_changed.connect(self._on_sound_settings_changed)
        tabs.addTab(self.event_sound_widget, "🔊 Suara")

        # Tab 8: Simulation
        simulation_tab = self._create_simulation_controls()
        tabs.addTab(simulation_tab, "🧪 Test")

        layout.addWidget(tabs)

        # Log
        log_group = QGroupBox("Event Log")
        log_layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

        return panel

    def _create_battle_controls(self):
        """Create battle control widgets"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Title
        title = QLabel("⚔️ PK Battle Controls")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        layout.addWidget(title)

        # Round duration
        duration_layout = QHBoxLayout()
        duration_layout.addWidget(QLabel("Round Duration:"))
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(1, 180)
        self.duration_spin.setValue(60)
        self.duration_spin.setSuffix(" min")
        self.duration_spin.valueChanged.connect(self._on_duration_changed)
        duration_layout.addWidget(self.duration_spin)
        layout.addLayout(duration_layout)

        # Battle controls
        btn_layout = QVBoxLayout()

        self.start_btn = QPushButton("▶️ Start Battle")
        self.start_btn.clicked.connect(self._on_start_battle)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        btn_layout.addWidget(self.start_btn)

        self.pause_btn = QPushButton("⏸️ Pause")
        self.pause_btn.clicked.connect(self._on_pause_battle)
        self.pause_btn.setEnabled(False)
        btn_layout.addWidget(self.pause_btn)

        self.reset_btn = QPushButton("🔄 Reset All")
        self.reset_btn.clicked.connect(self._on_reset_battle)
        btn_layout.addWidget(self.reset_btn)

        layout.addLayout(btn_layout)

        # Sound settings
        layout.addWidget(QLabel("🔊 Sound Settings:"))

        self.sound_check = QCheckBox("Enable Win Sounds")
        self.sound_check.setChecked(True)
        self.sound_check.stateChanged.connect(self._on_sound_toggle)
        layout.addWidget(self.sound_check)

        volume_layout = QHBoxLayout()
        volume_layout.addWidget(QLabel("Volume:"))
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(80)
        self.volume_slider.valueChanged.connect(self._on_volume_changed)
        volume_layout.addWidget(self.volume_slider)
        layout.addLayout(volume_layout)

        layout.addStretch()
        return widget

    def _create_tiktok_controls(self):
        """Create TikTok connection controls"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Title
        title = QLabel("📺 TikTok Live Connection")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        layout.addWidget(title)

        # Username input
        layout.addWidget(QLabel("TikTok Username:"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter @username...")
        layout.addWidget(self.username_input)

        # Connect button
        self.connect_btn = QPushButton("🔌 Connect to Live")
        self.connect_btn.clicked.connect(self._on_connect_tiktok)
        self.connect_btn.setStyleSheet("""
            QPushButton {
                background-color: #E91E63;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #C2185B; }
        """)
        layout.addWidget(self.connect_btn)

        # Disconnect button
        self.disconnect_btn = QPushButton("⏹️ Disconnect")
        self.disconnect_btn.clicked.connect(self._on_disconnect_tiktok)
        self.disconnect_btn.setEnabled(False)
        layout.addWidget(self.disconnect_btn)

        # Status
        self.status_label = QLabel("Status: Not Connected")
        self.status_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
        layout.addWidget(self.status_label)

        layout.addStretch()
        return widget

    def _create_simulation_controls(self):
        """Create simulation test controls"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Title
        title = QLabel("🧪 Test Simulation")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        layout.addWidget(title)

        layout.addWidget(QLabel("Simulate events for testing:"))

        # Simulate buttons
        sim_like_btn = QPushButton("❤️ Simulate Like")
        sim_like_btn.clicked.connect(lambda: self._simulate_event('like'))
        layout.addWidget(sim_like_btn)

        sim_comment_btn = QPushButton("💬 Simulate Comment")
        sim_comment_btn.clicked.connect(lambda: self._simulate_event('comment'))
        layout.addWidget(sim_comment_btn)

        sim_gift_a_btn = QPushButton("🎁 Simulate Gift → Team A")
        sim_gift_a_btn.clicked.connect(lambda: self._simulate_gift('A'))
        sim_gift_a_btn.setStyleSheet("background-color: #FF6B6B; color: white;")
        layout.addWidget(sim_gift_a_btn)

        sim_gift_b_btn = QPushButton("🎁 Simulate Gift → Team B")
        sim_gift_b_btn.clicked.connect(lambda: self._simulate_gift('B'))
        sim_gift_b_btn.setStyleSheet("background-color: #4ECDC4; color: white;")
        layout.addWidget(sim_gift_b_btn)

        rapid_btn = QPushButton("🚀 Rapid Test (10 events)")
        rapid_btn.clicked.connect(self._simulate_rapid_events)
        layout.addWidget(rapid_btn)

        layout.addStretch()
        return widget

    def _connect_signals(self):
        """Connect PK system signals"""
        self.pk_system.points_updated.connect(self._on_points_updated)
        self.pk_system.score_updated.connect(self._on_score_updated)
        self.pk_system.timer_updated.connect(self._on_timer_updated)
        self.pk_system.round_won.connect(self._on_round_won)
        self.pk_system.round_reset.connect(self._on_round_reset)

        # TikTok signals
        self.tiktok_handler.event_received.connect(self._on_tiktok_event)
        self.tiktok_handler.connection_status.connect(self._on_connection_status)
        self.tiktok_handler.error_occurred.connect(self._on_error)

    def _apply_theme(self):
        """Apply dark theme"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QWidget {
                background-color: #2b2b2b;
                color: white;
            }
            QGroupBox {
                color: #ffffff;
                border: 2px solid #555555;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #555555;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QPushButton:disabled {
                background-color: #333333;
                color: #888888;
            }
            QLineEdit, QTextEdit, QSpinBox {
                background-color: #333333;
                color: white;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 5px;
            }
            QLabel {
                color: white;
            }
            QTabWidget::pane {
                border: 1px solid #555555;
                background: #2b2b2b;
            }
            QTabBar::tab {
                background: #333333;
                color: white;
                padding: 8px 15px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #4CAF50;
            }
        """)

    # Event Handlers
    @pyqtSlot(str, int)
    def _on_points_updated(self, team, points):
        """Update points display"""
        if team == 'A':
            self.points_a_label.setText(f"{points:,} poin")
        else:
            self.points_b_label.setText(f"{points:,} poin")

        # Update progress bar with REAL POINTS (not percentage!)
        self.progress_bar.set_points(self.pk_system.team_a_points, self.pk_system.team_b_points)

    @pyqtSlot(int, int)
    def _on_score_updated(self, score_a, score_b):
        """Update score display"""
        self.score_label.setText(f"TEAM A  [{score_a}] - [{score_b}]  TEAM B")

    @pyqtSlot(int)
    def _on_timer_updated(self, seconds):
        """Update timer display"""
        minutes = seconds // 60
        secs = seconds % 60
        self.timer_label.setText(f"Time: {minutes:02d}:{secs:02d}")

        # Warning at 10 seconds
        if seconds == 10:
            self.sound_manager.play_round_end_warning()

    @pyqtSlot(str)
    def _on_round_won(self, winner):
        """Handle round win"""
        self._add_log(f"🏆 TEAM {winner} WINS THE ROUND!")
        self.sound_manager.play_team_win(winner)

        # TODO: Add visual win effect

    @pyqtSlot()
    def _on_round_reset(self):
        """Handle round reset"""
        self._add_log("🔄 New round starting...")

    def _on_start_battle(self):
        """Start PK battle"""
        self.pk_system.start_battle()
        self.start_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self._add_log("▶️ PK Battle started!")

    def _on_pause_battle(self):
        """Pause/Resume battle"""
        if self.pk_system.is_running:
            self.pk_system.pause_battle()
            self.pause_btn.setText("▶️ Resume")
            self._add_log("⏸️ Battle paused")
        else:
            self.pk_system.resume_battle()
            self.pause_btn.setText("⏸️ Pause")
            self._add_log("▶️ Battle resumed")

    def _on_reset_battle(self):
        """Reset battle"""
        self.pk_system.reset_all()
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.pause_btn.setText("⏸️ Pause")
        self._add_log("🔄 Battle reset to 0-0")

    def _on_duration_changed(self, minutes):
        """Change round duration"""
        self.pk_system.set_round_duration(minutes)
        self._add_log(f"⏱️ Round duration set to {minutes} minutes")

    def _on_sound_toggle(self, state):
        """Toggle sound"""
        enabled = state == Qt.CheckState.Checked.value
        self.sound_manager.set_enabled(enabled)

    def _on_volume_changed(self, value):
        """Change volume"""
        volume = value / 100.0
        self.sound_manager.set_volume(volume)

    def _on_photo_loaded(self, team, file_path):
        """Load team photo"""
        if team == 'A':
            success = self.photo_a.load_photo(file_path)
        else:
            success = self.photo_b.load_photo(file_path)

        if success:
            self._add_log(f"📸 Team {team} photo loaded!")

    def _on_gift_assignment_changed(self, assignments):
        """Gift assignment changed"""
        self.gift_assignments = assignments
        self._add_log(f"🎁 Gift assignments updated ({len(assignments)} gifts)")

    def _on_interaction_assignment_changed(self, assignments):
        """Like/Comment assignment changed"""
        self.interaction_assignments = assignments
        self._add_log(f"👍💬 Like/Comment assignments updated")
        self._add_log(f"  Like → Team {assignments['like']}")
        self._add_log(f"  Comment → Team {assignments['comment']}")

    def _on_bubble_position_changed(self, positions):
        """Bubble position changed"""
        self.bubble_positions = positions
        self._add_log(f"🫧 Bubble positions updated")
        self._add_log(f"  Like → {positions['like']}")
        self._add_log(f"  Comment → {positions['comment']}")

    def _on_sound_settings_changed(self, settings):
        """Event sound settings changed"""
        self.event_sound_settings = settings
        enabled_count = sum(1 for s in settings.values() if s['enabled'])
        self._add_log(f"🔊 Sound settings updated ({enabled_count}/{len(settings)} enabled)")

    @pyqtSlot(dict)
    def _on_tiktok_event(self, event_data):
        """Handle TikTok event"""
        event_type = event_data.get('type')

        if event_type == 'gift':
            self._handle_gift_event(event_data)
        else:
            self._handle_bubble_event(event_data)

    def _handle_gift_event(self, event_data):
        """Handle gift event - add points and create bubble"""
        gift_name = event_data.get('gift_name', '')
        gift_count = event_data.get('gift_count', 1)

        # Get gift value
        from gift_tiers import get_gift_value_from_name
        gift_value = get_gift_value_from_name(gift_name)
        total_coins = gift_value * gift_count

        # Determine team
        team = self.gift_assignment_widget.get_team_for_gift(gift_name)

        # Add points
        self.pk_system.add_gift_points(team, total_coins)

        # Play gift sound if enabled
        if 'gift' in self.event_sound_settings and self.event_sound_settings['gift']['enabled']:
            sound_file = self.event_sound_settings['gift']['file']
            self.sound_manager.play_event_sound('gift', sound_file)

        # Create bubble in bottom zone (directional)
        self._create_bubble(event_data, zone='bottom', team=team)

        self._add_log(f"🎁 {gift_name} x{gift_count} → Team {team} (+{total_coins * 5} pts)")

    def _handle_bubble_event(self, event_data):
        """Handle non-gift events - create bubble and add points for like/comment"""
        event_type = event_data.get('type', '')

        # Check if it's a like or comment - add points to assigned team
        if event_type == 'like':
            team = self.interaction_assignments.get('like', 'A')
            self.pk_system.add_interaction_points(team, 1)
            self._add_log(f"👍 Like → Team {team} (+1 poin)")

            # Play sound if enabled
            if event_type in self.event_sound_settings and self.event_sound_settings[event_type]['enabled']:
                sound_file = self.event_sound_settings[event_type]['file']
                self.sound_manager.play_event_sound(event_type, sound_file)

        elif event_type == 'comment':
            team = self.interaction_assignments.get('comment', 'A')
            self.pk_system.add_interaction_points(team, 1)
            comment_text = event_data.get('comment', '')[:20]
            self._add_log(f"💬 Comment → Team {team} (+1 poin): {comment_text}")

            # Play sound if enabled
            if event_type in self.event_sound_settings and self.event_sound_settings[event_type]['enabled']:
                sound_file = self.event_sound_settings[event_type]['file']
                self.sound_manager.play_event_sound(event_type, sound_file)

        # Play sound for other events (join, follow, share)
        if event_type in ['join', 'follow', 'share']:
            if event_type in self.event_sound_settings and self.event_sound_settings[event_type]['enabled']:
                sound_file = self.event_sound_settings[event_type]['file']
                self.sound_manager.play_event_sound(event_type, sound_file)

        # Get bubble position for this event type
        bubble_position = self.bubble_positions.get(event_type, 'top')

        # Create bubble for visual effect based on position settings
        self._create_bubble_at_position(event_data, bubble_position)

    def _create_bubble_at_position(self, event_data, position='top'):
        """Create bubble at specified position (left, right, top, bottom)"""
        # Choose parent zone based on position
        if position in ['left', 'right']:
            # Use center zone for left/right
            parent = self.center_pk_view
            bubble = BubbleWidget(parent, event_data)

            if position == 'left':
                # Left edge, random vertical
                x = random.randint(10, 100)
                y = random.randint(100, 700)
            else:  # right
                # Right edge, random vertical
                x = random.randint(1400, 1500)
                y = random.randint(100, 700)

        elif position == 'bottom':
            # Bottom zone, random horizontal
            parent = self.bottom_bubble_zone
            bubble = BubbleWidget(parent, event_data)
            x = random.randint(50, 1400)
            y = random.randint(20, 150)

        else:  # top (default)
            # Top zone, random horizontal
            parent = self.top_bubble_zone
            bubble = BubbleWidget(parent, event_data)
            x = random.randint(50, 1400)
            y = random.randint(20, 150)

        bubble.move(x, y)
        bubble.show()

        self.active_bubbles.append(bubble)

        # Auto cleanup
        duration = event_data.get('duration', 3000)
        QTimer.singleShot(duration + 1000, lambda: self._cleanup_bubble(bubble))

    def _create_bubble(self, event_data, zone='top', team=None):
        """Create bubble in specified zone (for gifts)"""
        if zone == 'top':
            parent = self.top_bubble_zone
        else:
            parent = self.bottom_bubble_zone

        bubble = BubbleWidget(parent, event_data)

        # Position based on zone and team
        if zone == 'bottom' and team:
            # Directional positioning for gifts
            if team == 'A':
                # Left side
                x = random.randint(50, 600)
            else:
                # Right side
                x = random.randint(900, 1400)
            y = random.randint(20, 150)
        else:
            # Random positioning in zone
            x = random.randint(50, 1400)
            y = random.randint(20, 150)

        bubble.move(x, y)
        bubble.show()

        self.active_bubbles.append(bubble)

        # Auto cleanup
        duration = event_data.get('duration', 3000)
        QTimer.singleShot(duration + 1000, lambda: self._cleanup_bubble(bubble))

    def _cleanup_bubble(self, bubble):
        """Cleanup finished bubble"""
        try:
            if bubble in self.active_bubbles:
                self.active_bubbles.remove(bubble)
            # Check if bubble still exists before deleting
            if bubble and not bubble.isHidden():
                bubble.deleteLater()
        except RuntimeError:
            # Bubble already deleted, ignore
            pass

    def _simulate_event(self, event_type):
        """Simulate event for testing"""
        user = random.choice(config.DUMMY_USERS)
        event_data = {
            'type': event_type,
            'username': user['nickname'],
            'user_id': user['username'],
            'avatar_url': user['avatar'],
        }

        if event_type == 'comment':
            event_data['comment'] = random.choice(config.DUMMY_COMMENTS)

        self._handle_bubble_event(event_data)
        self._add_log(f"🧪 Simulated {event_type}")

    def _simulate_gift(self, team):
        """Simulate gift for a team"""
        # Get a gift assigned to this team
        team_gifts = [name for name, t in self.gift_assignments.items() if t == team]

        if not team_gifts:
            self._add_log(f"⚠️ No gifts assigned to Team {team} yet!")
            return

        gift_name = random.choice(team_gifts)
        user = random.choice(config.DUMMY_USERS)

        event_data = {
            'type': 'gift',
            'username': user['nickname'],
            'user_id': user['username'],
            'avatar_url': user['avatar'],
            'gift_name': gift_name,
            'gift_count': 1
        }

        self._handle_gift_event(event_data)

    def _simulate_rapid_events(self):
        """Simulate rapid events"""
        for i in range(10):
            if i % 3 == 0:
                team = random.choice(['A', 'B'])
                QTimer.singleShot(i * 300, lambda t=team: self._simulate_gift(t))
            else:
                event_type = random.choice(['like', 'comment'])
                QTimer.singleShot(i * 300, lambda et=event_type: self._simulate_event(et))

        self._add_log("🚀 Rapid test started!")

    def _on_connect_tiktok(self):
        """Connect to TikTok"""
        username = self.username_input.text().strip().lstrip('@')
        if not username:
            self._add_log("❌ Please enter a username")
            return

        self._add_log(f"Connecting to @{username}...")
        self.tiktok_thread = TikTokThread(self.tiktok_handler, username)
        self.tiktok_thread.start()

        self.connect_btn.setEnabled(False)
        self.disconnect_btn.setEnabled(True)

    def _on_disconnect_tiktok(self):
        """Disconnect from TikTok"""
        self.tiktok_handler.disconnect_from_live()
        if self.tiktok_thread:
            self.tiktok_thread.quit()
            self.tiktok_thread.wait()

        self.connect_btn.setEnabled(True)
        self.disconnect_btn.setEnabled(False)
        self._add_log("⏹️ Disconnected")

    @pyqtSlot(str)
    def _on_connection_status(self, status):
        """Update connection status"""
        self.status_label.setText(f"Status: {status}")
        if "Connected" in status:
            self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        else:
            self.status_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")

    @pyqtSlot(str)
    def _on_error(self, error_msg):
        """Handle error"""
        self._add_log(f"❌ ERROR: {error_msg}")

    def _add_log(self, message):
        """Add message to log"""
        self.log_text.append(message)
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )

    def _show_welcome_message(self):
        """Show welcome message"""
        self._add_log("="*50)
        self._add_log("🎮 PK BATTLE MODE - TikTok Live")
        self._add_log("="*50)
        self._add_log("1. Upload Team A & B photos (Photos tab)")
        self._add_log("2. Assign gifts to teams (Gifts tab)")
        self._add_log("3. Connect to TikTok Live (TikTok tab)")
        self._add_log("4. Start Battle! (Battle tab)")
        self._add_log("="*50)


class PKProgressBar(QWidget):
    """Custom progress bar for PK battle - Shows REAL POINTS"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.team_a_points = 0
        self.team_b_points = 0

    def set_points(self, team_a_points, team_b_points):
        """Set real points for both teams"""
        self.team_a_points = team_a_points
        self.team_b_points = team_b_points
        self.update()

    def paintEvent(self, event):
        """Custom paint"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()

        # Background
        painter.fillRect(0, 0, w, h, QColor(50, 50, 50))

        # Calculate percentage for bar visual
        total = self.team_a_points + self.team_b_points
        if total > 0:
            team_a_pct = (self.team_a_points / total) * 100
            team_b_pct = (self.team_b_points / total) * 100
        else:
            team_a_pct = 50
            team_b_pct = 50

        # Team A bar (from left)
        a_width = int(w * (team_a_pct / 100))
        gradient_a = QLinearGradient(0, 0, a_width, 0)
        gradient_a.setColorAt(0, QColor(255, 107, 107))
        gradient_a.setColorAt(1, QColor(255, 82, 82))
        painter.fillRect(0, 0, a_width, h, gradient_a)

        # Team B bar (from right)
        b_width = int(w * (team_b_pct / 100))
        gradient_b = QLinearGradient(w - b_width, 0, w, 0)
        gradient_b.setColorAt(0, QColor(78, 205, 196))
        gradient_b.setColorAt(1, QColor(61, 189, 179))
        painter.fillRect(w - b_width, 0, b_width, h, gradient_b)

        # Border
        painter.setPen(QPen(QColor(255, 255, 255), 3))
        painter.drawRect(1, 1, w - 2, h - 2)

        # REAL POINTS text (not percentage!)
        font = painter.font()
        font.setPointSize(20)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))

        # Team A points (left)
        painter.drawText(QRect(10, 0, 250, h),
                        Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                        f"{self.team_a_points:,}")

        # Team B points (right)
        painter.drawText(QRect(w - 260, 0, 250, h),
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                        f"{self.team_b_points:,}")
