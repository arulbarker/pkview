"""
PK Main Window - TikTok Style Battle Interface
Vertical layout for PK battle with bubble zones
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFrame, QSplitter, QGroupBox,
                             QTextEdit, QLineEdit, QSpinBox, QSlider, QCheckBox,
                             QTabWidget, QComboBox)
from PyQt6.QtCore import Qt, QTimer, pyqtSlot, QRect, QPoint
from PyQt6.QtGui import QPainter, QColor, QLinearGradient, QPen, QFont
import config
from bubble_widget import BubbleWidget
from pk_battle_system import PKBattleSystem
from photo_manager import DraggablePhoto, PhotoUploadWidget
from gift_assignment_widget import GiftAssignmentWidget
from interaction_assignment_widget import InteractionAssignmentWidget
from bubble_position_widget import BubblePositionWidget
from event_sound_widget import EventSoundWidget
from point_settings_widget import PointSettingsWidget
from draggable_label import DraggableLabel, DraggableMultiLineLabel
from sound_manager import SoundManager
from tiktok_handler import TikTokHandler, TikTokThread
import random
import math
import os
import json


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

        # Bubble positions (like/comment bubble placement) - OBSOLETE but kept for compatibility
        self.bubble_positions = {
            'like': 'top',
            'comment': 'top'
        }
        
        # Custom Bubble Settings (Duration & Size)
        self.bubble_settings = {
            'duration': 5000,  # Default 5 seconds
            'size': 100,       # Default 100px (Like/Comment)
            'gift_size': 150   # Default 150px (Gifts - Larger)
        }

        # Event sound settings
        self.event_sound_settings = {}

        # Point settings (custom points per like/comment)
        self.point_values = {
            'like': 1,      # Default: 1 point per like
            'comment': 1    # Default: 1 point per comment
        }

        # Win sound file paths (customizable by user)
        self.win_sound_files = {
            'team_a': 'sounds/team_a_win.mp3',
            'team_b': 'sounds/team_b_win.mp3'
        }

        self._setup_ui()
        self._connect_signals()

        # CRITICAL FIX: Manually trigger assignment updates after signals are connected
        # Widgets already loaded their data, but signals weren't connected yet
        self._initialize_assignments_from_widgets()

        self._show_welcome_message()

        # Create placeholder sounds
        self.sound_manager.create_placeholder_sounds()

    def _load_win_sound_settings(self):
        """Load win sound settings from config file"""
        # (Existing code for win sounds...)
        pass

    def save_settings(self):
        """Save current application settings to file"""
        settings = {
            'bubble_settings': self.bubble_settings,
            'point_values': self.point_values,
            'interaction_assignments': self.interaction_assignments,
            'gift_assignments': self.gift_assignments,
            'event_sound_settings': self.event_sound_settings,
            'win_sound_files': self.win_sound_files
        }
        
        try:
            with open('app_settings.json', 'w') as f:
                json.dump(settings, f, indent=4)
            self._add_log("💾 Settings saved successfully!")
        except Exception as e:
            self._add_log(f"❌ Error saving settings: {str(e)}")

    def load_settings(self):
        """Load application settings from file"""
        if not os.path.exists('app_settings.json'):
            return
            
        try:
            with open('app_settings.json', 'r') as f:
                settings = json.load(f)
                
            # Update settings if they exist
            if 'bubble_settings' in settings:
                self.bubble_settings.update(settings['bubble_settings'])
                
            if 'point_values' in settings:
                self.point_values.update(settings['point_values'])
                
            if 'interaction_assignments' in settings:
                self.interaction_assignments.update(settings['interaction_assignments'])
                
            # Note: Gift assignments are complex, might need special handling
            # For now, let's focus on bubble settings as requested
            
            self._add_log("📂 Settings loaded successfully")
        except Exception as e:
            self._add_log(f"❌ Error loading settings: {str(e)}")

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

        # FIXED: Make zones FULL SIZE to prevent clipping!
        # Zones are now full container size - no more element cutting!

        # TOP Bubble Zone (FULL SIZE - for bubbles only)
        self.top_bubble_zone = QWidget(container)
        self.top_bubble_zone.setGeometry(0, 0, 2000, 1200)  # Full size
        self.top_bubble_zone.setStyleSheet("background: transparent;")
        self.top_bubble_zone.lower()  # Behind draggable elements

        # CENTER PK Battle View (FULL SIZE - for all draggable elements)
        self.center_pk_view = QWidget(container)
        self.center_pk_view.setGeometry(0, 0, 2000, 1200)  # Full size
        self.center_pk_view.setStyleSheet("background: transparent;")
        # Don't lower this one - it should be above zones

        # Create PK view components
        self._create_pk_view_components()

        # BOTTOM Bubble Zone (FULL SIZE - for bubbles only)
        self.bottom_bubble_zone = QWidget(container)
        self.bottom_bubble_zone.setGeometry(0, 0, 2000, 1200)  # Full size
        self.bottom_bubble_zone.setStyleSheet("background: transparent;")
        self.bottom_bubble_zone.lower()  # Behind draggable elements
        
        # GIFT OVERLAY ZONE (FULL SIZE - ON TOP OF EVERYTHING)
        self.gift_overlay_zone = QWidget(container)
        self.gift_overlay_zone.setGeometry(0, 0, 2000, 1200)
        self.gift_overlay_zone.setStyleSheet("background: transparent;")
        self.gift_overlay_zone.raise_() # Ensure it's on top
        self.gift_overlay_zone.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents) # Let clicks pass through if needed

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

        # VS Label (center separator) - DRAGGABLE, ROTATABLE, RESIZABLE!
        self.vs_label = DraggableLabel(
            self.center_pk_view,
            "VS",
            font_size=36,
            text_color="#FFD700",  # Gold
            bg_color="rgba(255, 215, 0, 0.2)",  # Gold semi-transparent
            border_color="#FFD700"
        )
        self.vs_label.setGeometry(700, 610, 100, 50)
        self.vs_label.min_width = 60
        self.vs_label.max_width = 300
        self.vs_label.min_height = 40
        self.vs_label.max_height = 150
        self.vs_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

        # Tab 6: Bubble Settings (Custom Duration & Size)
        bubble_settings_tab = self._create_bubble_settings_tab()
        tabs.addTab(bubble_settings_tab, "🫧 Bubble Settings")

        # Tab 7: Event Sounds
        self.event_sound_widget = EventSoundWidget()
        self.event_sound_widget.sound_settings_changed.connect(self._on_sound_settings_changed)
        tabs.addTab(self.event_sound_widget, "🔊 Suara")

        # Tab 8: Point Settings
        self.point_settings_widget = PointSettingsWidget()
        self.point_settings_widget.point_settings_changed.connect(self._on_point_settings_changed)
        tabs.addTab(self.point_settings_widget, "🎯 Custom Points")

        # Tab 9: Developer Info
        developer_tab = self._create_developer_tab()
        tabs.addTab(developer_tab, "👨‍💻 Developer")

        # Tab 9: Simulation
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

        # Start button removed as requested - functionality moved to Connect button
        # self.start_btn = QPushButton("▶️ Start Battle")
        # ...

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

        # Win sound customization
        layout.addSpacing(15)
        layout.addWidget(QLabel("🎵 Custom Win Sounds:"))

        # Team A win sound
        team_a_sound_layout = QHBoxLayout()
        team_a_label = QLabel("Team A:")
        team_a_label.setStyleSheet("color: #FF6B6B; font-weight: bold;")
        team_a_sound_layout.addWidget(team_a_label)

        self.team_a_sound_file = QLabel("team_a_win.mp3")
        self.team_a_sound_file.setStyleSheet("color: #888; font-size: 11px;")
        team_a_sound_layout.addWidget(self.team_a_sound_file)
        team_a_sound_layout.addStretch()

        team_a_browse_btn = QPushButton("Browse...")
        team_a_browse_btn.clicked.connect(lambda: self._browse_win_sound('A'))
        team_a_browse_btn.setMaximumWidth(80)
        team_a_sound_layout.addWidget(team_a_browse_btn)
        layout.addLayout(team_a_sound_layout)

        # Team B win sound
        team_b_sound_layout = QHBoxLayout()
        team_b_label = QLabel("Team B:")
        team_b_label.setStyleSheet("color: #4ECDC4; font-weight: bold;")
        team_b_sound_layout.addWidget(team_b_label)

        self.team_b_sound_file = QLabel("team_b_win.mp3")
        self.team_b_sound_file.setStyleSheet("color: #888; font-size: 11px;")
        team_b_sound_layout.addWidget(self.team_b_sound_file)
        team_b_sound_layout.addStretch()
        team_b_browse_btn = QPushButton("Browse...")
        team_b_browse_btn.clicked.connect(lambda: self._browse_win_sound('B'))
        team_b_browse_btn.setMaximumWidth(80)
        team_b_sound_layout.addWidget(team_b_browse_btn)
        layout.addLayout(team_b_sound_layout)

        # Layout Mode
        layout_group = QGroupBox("Tampilan Layout")
        layout_layout = QVBoxLayout(layout_group)
        
        self.layout_combo = QComboBox()
        self.layout_combo.addItems([
            "Standard (Horizontal)", 
            "Vertical Stack (Top-Bottom)", 
            "Vertical Stream (Rotated -90°)"
        ])
        self.layout_combo.currentIndexChanged.connect(self._on_layout_mode_changed)
        layout_layout.addWidget(self.layout_combo)
        
        layout.addWidget(layout_group)

        # Add stretch
        layout.addStretch()
        return widget

    def _on_layout_mode_changed(self, index):
        """Handle layout mode change"""
        mode = self.layout_combo.currentText()
        self._apply_layout_mode(mode)

    def _apply_layout_mode(self, mode):
        """Apply the selected layout mode"""
        
        # Helper to restore standard dimensions
        def restore_label_dims(label, w, h):
            label.rotation_angle = 0
            # Restore standard constraints (hardcoded based on init)
            # Standard constraints:
            # Score: min_w 300, max_w 1000, min_h 60, max_h 150
            # Timer: min_w 200, max_w 500, min_h 40, max_h 100
            # Points: min_w 150, max_w 500
            # VS: min_w 60, max_w 300, min_h 40, max_h 150
            
            if label == self.score_label:
                label.min_width, label.max_width = 300, 1000
                label.min_height, label.max_height = 60, 150
            elif label == self.timer_label:
                label.min_width, label.max_width = 200, 500
                label.min_height, label.max_height = 40, 100
            elif label in [self.points_a_label, self.points_b_label]:
                label.min_width, label.max_width = 150, 500
                label.min_height, label.max_height = 40, 100 # Default
            elif label == self.vs_label:
                label.min_width, label.max_width = 60, 300
                label.min_height, label.max_height = 40, 150
                
            label.resize(w, h)

        # Reset rotations first
        self.photo_a.rotation_angle = 0
        self.photo_b.rotation_angle = 0
        self.progress_bar.rotation_angle = 0
        
        # Center X coordinate
        center_x = 1400 // 2
        
        if "Standard" in mode:
            # Standard Horizontal Layout
            restore_label_dims(self.score_label, 600, 80)
            restore_label_dims(self.timer_label, 300, 50)
            restore_label_dims(self.points_a_label, 300, 60)
            restore_label_dims(self.points_b_label, 300, 60)
            restore_label_dims(self.vs_label, 100, 50)
            
            self.score_label.move(500, 10)
            self.timer_label.move(650, 100)
            
            self.photo_a.move(300, 200)
            self.photo_b.move(800, 200)
            
            self.points_a_label.move(300, 560)
            self.points_b_label.move(800, 560)
            
            self.vs_label.move(675, 350)
            self.progress_bar.setGeometry(300, 650, 800, 40)
            
        elif "Vertical Stack" in mode:
            # Vertical Stack (Top-Bottom)
            restore_label_dims(self.score_label, 600, 80)
            restore_label_dims(self.timer_label, 300, 50)
            restore_label_dims(self.points_a_label, 300, 60)
            restore_label_dims(self.points_b_label, 300, 60)
            restore_label_dims(self.vs_label, 100, 50)
            
            self.score_label.move(center_x - 300, 20)
            self.timer_label.move(center_x - 150, 100)
            
            # Team A Top
            self.photo_a.move(center_x - 175, 180)
            self.points_a_label.move(center_x - 150, 540)
            
            # VS in middle
            self.vs_label.move(center_x - 50, 600)
            
            # Team B Bottom
            self.photo_b.move(center_x - 175, 680)
            self.points_b_label.move(center_x - 150, 1040)
            
            # Progress bar
            self.progress_bar.setGeometry(center_x - 400, 1120, 800, 40)

        elif "Rotated" in mode:
            # Rotated -90 degrees for vertical streaming
            rotation = -90
            
            # Helper to swap dimensions for a label
            def rotate_label_dims(label, w, h):
                label.rotation_angle = rotation
                # Swap min/max constraints
                label.min_width, label.min_height = label.min_height, label.min_width
                label.max_width, label.max_height = label.max_height, label.max_width
                # Resize to swapped dimensions
                label.resize(h, w)
            
            # Apply rotation and dimension swap
            rotate_label_dims(self.score_label, 600, 80)
            rotate_label_dims(self.timer_label, 300, 50)
            rotate_label_dims(self.points_a_label, 300, 60)
            rotate_label_dims(self.points_b_label, 300, 60)
            rotate_label_dims(self.vs_label, 100, 50)
            
            # Photos don't need swap (square)
            self.photo_a.rotation_angle = rotation
            self.photo_b.rotation_angle = rotation
            
            # Progress bar needs swap
            self.progress_bar.rotation_angle = rotation
            
            # Center Y line (middle of the screen height)
            mid_y = 500
            
            # Position elements (Left-to-Right visually -> Top-to-Bottom logically)
            
            # 1. Header (Timer & Score)
            self.timer_label.move(100, mid_y - 150)
            self.score_label.move(250, mid_y - 300)
            
            # 2. Team A
            self.photo_a.move(450, mid_y - 175)
            self.points_a_label.move(400, mid_y + 200)
            
            # 3. VS
            self.vs_label.move(800, mid_y - 50)
            
            # 4. Team B
            self.photo_b.move(950, mid_y - 175)
            self.points_b_label.move(900, mid_y + 200)
            
            # 5. Progress Bar
            # Swap width/height for geometry
            self.progress_bar.setGeometry(1300, mid_y - 400, 60, 800)

        # Force update
        self.score_label.update()
        self.timer_label.update()
        self.points_a_label.update()
        self.points_b_label.update()
        self.vs_label.update()
        self.photo_a.update()
        self.photo_b.update()
        self.progress_bar.update()

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

        # Simulate Comment
        sim_comment_btn = QPushButton("💬 Simulate Comment")
        sim_comment_btn.clicked.connect(lambda: self._simulate_event('comment'))
        layout.addWidget(sim_comment_btn)
        
        # Simulate Gift
        sim_gift_btn = QPushButton("🎁 Simulate Gift (Random)")
        sim_gift_btn.clicked.connect(lambda: self._simulate_gift('A'))
        layout.addWidget(sim_gift_btn)
        
        # Rapid Test
        rapid_test_btn = QPushButton("🚀 Rapid Test (10 events)")
        rapid_test_btn.clicked.connect(self._simulate_rapid_events)
        layout.addWidget(rapid_test_btn)

        layout.addStretch()
        return widget

    def _create_bubble_settings_tab(self):
        """Create tab for custom bubble settings"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title = QLabel("⚙️ Bubble Settings")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        layout.addWidget(title)
        
        layout.addWidget(QLabel("Customize appearance for ALL bubbles:"))
        layout.addSpacing(10)
        
        # 1. Duration Control
        duration_group = QGroupBox("Duration (Time on Screen)")
        duration_layout = QVBoxLayout()
        
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(1, 300) # 1s to 5 mins
        self.duration_spin.setValue(int(self.bubble_settings['duration'] / 1000))
        self.duration_spin.setSuffix(" seconds")
        self.duration_spin.valueChanged.connect(self._on_bubble_duration_changed)
        
        duration_layout.addWidget(QLabel("How long bubbles stay visible:"))
        duration_layout.addWidget(self.duration_spin)
        duration_group.setLayout(duration_layout)
        layout.addWidget(duration_group)
        
        # 2. Size Control
        size_group = QGroupBox("Bubble Size")
        size_layout = QVBoxLayout()
        
        self.size_spin = QSpinBox()
        self.size_spin.setRange(50, 500) # 50px to 500px
        self.size_spin.setValue(self.bubble_settings['size'])
        self.size_spin.setSuffix(" px")
        self.size_spin.setSingleStep(10)
        self.size_spin.valueChanged.connect(self._on_bubble_size_changed)
        
        size_layout.addWidget(QLabel("Size of the bubble:"))
        size_layout.addWidget(self.size_spin)
        size_group.setLayout(size_layout)
        layout.addWidget(size_group)
        
        # 3. Gift Size Control (Separate)
        gift_size_group = QGroupBox("Gift Bubble Size")
        gift_size_layout = QVBoxLayout()
        
        self.gift_size_spin = QSpinBox()
        self.gift_size_spin.setRange(50, 800) # 50px to 800px
        self.gift_size_spin.setValue(self.bubble_settings['gift_size'])
        self.gift_size_spin.setSuffix(" px")
        self.gift_size_spin.setSingleStep(10)
        self.gift_size_spin.valueChanged.connect(self._on_bubble_gift_size_changed)
        
        gift_size_layout.addWidget(QLabel("Size of GIFT bubbles (usually larger):"))
        gift_size_layout.addWidget(self.gift_size_spin)
        gift_size_group.setLayout(gift_size_layout)
        layout.addWidget(gift_size_group)
        
        layout.addSpacing(20)
        
        # Save Button
        save_btn = QPushButton("💾 Save All Settings")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                font-weight: bold; 
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
        
        layout.addStretch()
        return widget

    def _on_bubble_duration_changed(self, value):
        """Update bubble duration setting"""
        self.bubble_settings['duration'] = value * 1000 # Convert to ms
        self._add_log(f"⏱️ Bubble duration set to {value} seconds")

    def _on_bubble_size_changed(self, value):
        """Update bubble size setting"""
        self.bubble_settings['size'] = value
        self._add_log(f"📏 Bubble size set to {value} px")

    def _on_bubble_gift_size_changed(self, value):
        """Update gift bubble size setting"""
        self.bubble_settings['gift_size'] = value
        self._add_log(f"🎁 Gift bubble size set to {value} px")

    def _create_developer_tab(self):
        """Create developer info tab with social media links"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)

        # Title
        title = QLabel("👨‍💻 Developer Info")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: white; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Developer name
        dev_name = QLabel("Created by: Arul CG")
        dev_name.setStyleSheet("font-size: 14px; color: #FFD700; margin-bottom: 20px;")
        dev_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(dev_name)

        # Social media links container
        links_group = QGroupBox("Follow Me On Social Media")
        links_layout = QVBoxLayout()
        links_layout.setSpacing(10)

        # Social media data
        social_links = [
            ("YouTube", "https://www.youtube.com/@arulcg", "#FF0000"),
            ("Instagram", "https://www.instagram.com/arul.cg/", "#E4405F"),
            ("Facebook", "https://www.facebook.com/profile.php?id=61578938703730", "#1877F2"),
            ("Threads", "https://www.threads.com/@arul.cg", "#000000"),
            ("X (Twitter)", "https://x.com/ArulCg", "#1DA1F2"),
            ("LYNKID", "https://lynk.id/arullagi", "#00D9FF")
        ]

        # Create clickable link buttons
        for platform, url, color in social_links:
            link_btn = QPushButton(f"🔗 {platform}")
            link_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    padding: 12px;
                    border-radius: 6px;
                    font-size: 13px;
                    font-weight: bold;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background-color: #666666;
                }}
            """)
            link_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            link_btn.clicked.connect(lambda checked, u=url: self._open_link(u))
            links_layout.addWidget(link_btn)

        links_group.setLayout(links_layout)
        layout.addWidget(links_group)

        # Attribution
        attr_label = QLabel("Thank you for using TikTok Live PK Battle App!")
        attr_label.setStyleSheet("font-size: 11px; color: #888888; margin-top: 20px;")
        attr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(attr_label)

        layout.addStretch()
        return widget

    def _open_link(self, url):
        """Open URL in default browser"""
        try:
            import webbrowser
            webbrowser.open(url)
            self._add_log(f"Opening: {url}")
        except Exception as e:
            self._add_log(f"Error opening link: {str(e)}")

    def _connect_signals(self):
        """Connect PK system signals"""
        self.pk_system.points_updated.connect(self._on_points_updated)
        self.pk_system.score_updated.connect(self._on_score_updated)
        self.pk_system.timer_updated.connect(self._on_timer_updated)
        self.pk_system.round_won.connect(self._on_round_won)
        self.pk_system.round_reset.connect(self._on_round_reset)

        self.tiktok_handler.event_received.connect(self._on_tiktok_event)
        self.tiktok_handler.connection_status.connect(self._on_connection_status)
        self.tiktok_handler.error_occurred.connect(self._on_error)
        self.tiktok_handler.log_message.connect(self._add_log)  # Connect log messages

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
        self._add_log(f"")
        self._add_log(f"{'='*50}")
        self._add_log(f"[WINNER] TEAM {winner} WINS THE ROUND!")
        self._add_log(f"{'='*50}")
        self._add_log(f"[INFO] Auto-reset in 5 seconds...")
        self._add_log(f"[INFO] Score will accumulate, round will restart")
        self.sound_manager.play_team_win(winner)

        # TODO: Add visual win effect

    @pyqtSlot()
    def _on_round_reset(self):
        """Handle round reset"""
        self._add_log(f"")
        self._add_log(f"[NEW ROUND] Starting fresh round!")
        self._add_log(f"[RESET] Points: 0 - 0")
        self._add_log(f"[SCORE] Total Score: {self.pk_system.team_a_score} - {self.pk_system.team_b_score} (Accumulated)")
        self._add_log(f"{'='*50}")
        self._add_log(f"")

    def _on_start_battle(self):
        """Start PK battle"""
        self.pk_system.start_battle()
        # self.start_btn.setEnabled(False) # Button removed
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
        # self.start_btn.setEnabled(True) # Button removed
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

    def _browse_win_sound(self, team):
        """Browse for custom win sound file"""
        from PyQt6.QtWidgets import QFileDialog
        import os

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            f"Select Win Sound for Team {team}",
            "sounds",
            "Audio Files (*.mp3 *.wav *.ogg);;All Files (*.*)"
        )

        if file_path and os.path.exists(file_path):
            # Update the stored path
            team_key = f'team_{team.lower()}'
            self.win_sound_files[team_key] = file_path

            # Update the label
            file_name = os.path.basename(file_path)
            if team == 'A':
                self.team_a_sound_file.setText(file_name)
            else:
                self.team_b_sound_file.setText(file_name)

            # Update sound manager
            self.sound_manager.set_win_sound_file(team, file_path)

            # Save settings
            self._save_win_sound_settings()

            self._add_log(f"[OK] Team {team} win sound: {file_name}")

    def _load_win_sound_settings(self):
        """Load custom win sound file paths from JSON"""
        try:
            filepath = 'win_sounds.json'
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    saved_sounds = json.load(f)

                # Update paths
                self.win_sound_files.update(saved_sounds)

                # Update UI labels
                if 'team_a' in saved_sounds:
                    file_name = os.path.basename(saved_sounds['team_a'])
                    self.team_a_sound_file.setText(file_name)
                    self.sound_manager.set_win_sound_file('A', saved_sounds['team_a'])

                if 'team_b' in saved_sounds:
                    file_name = os.path.basename(saved_sounds['team_b'])
                    self.team_b_sound_file.setText(file_name)
                    self.sound_manager.set_win_sound_file('B', saved_sounds['team_b'])

                print("[OK] Loaded custom win sound settings")

        except Exception as e:
            print(f"Error loading win sound settings: {e}")

    def _save_win_sound_settings(self):
        """Save custom win sound file paths to JSON"""
        try:
            filepath = 'win_sounds.json'
            with open(filepath, 'w') as f:
                json.dump(self.win_sound_files, f, indent=2)

            print("[OK] Win sound settings saved")

        except Exception as e:
            print(f"Error saving win sound settings: {e}")

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

    def _on_point_settings_changed(self, settings):
        """Point settings changed"""
        self.point_values = settings
        self._add_log(f"🎯 Custom points updated")
        self._add_log(f"  1 Like = {settings['like']} poin")
        self._add_log(f"  1 Comment = {settings['comment']} poin")

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
            # Use like_count if available (handles spam/rapid likes from same user)
            like_count = event_data.get('like_count', 1)
            # Get custom points per like
            points_per_like = self.point_values.get('like', 1)
            total_points = like_count * points_per_like
            self.pk_system.add_interaction_points(team, like_count, points_per_like)
            self._add_log(f"[LIKE] Team {team} (+{total_points} poin) [{like_count} x {points_per_like}]")

            # Play sound if enabled
            if event_type in self.event_sound_settings and self.event_sound_settings[event_type]['enabled']:
                sound_file = self.event_sound_settings[event_type]['file']
                self.sound_manager.play_event_sound(event_type, sound_file)

        elif event_type == 'comment':
            team = self.interaction_assignments.get('comment', 'A')
            # Get custom points per comment
            points_per_comment = self.point_values.get('comment', 1)
            self.pk_system.add_interaction_points(team, 1, points_per_comment)
            comment_text = event_data.get('comment', '')[:20]
            self._add_log(f"[COMMENT] Team {team} (+{points_per_comment} poin): {comment_text}")

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

        # Get team assignment for like/comment to position bubble near team circle
        team = None
        if event_type == 'like':
            team = self.interaction_assignments.get('like', 'A')
        elif event_type == 'comment':
            team = self.interaction_assignments.get('comment', 'A')

        # Create bubble for visual effect based on position settings
        self._create_bubble_at_position(event_data, bubble_position, team)

    def _create_bubble_at_position(self, event_data, position='top', team=None):
        """Create bubble at specified position (left, right, top, bottom)
        If team is provided, position bubble near team's photo circle"""
        
        # Inject custom settings
        event_data['custom_duration'] = self.bubble_settings['duration']
        event_data['custom_size'] = self.bubble_settings['size']

        # If team is assigned (for like/comment), position near team photo in center view
        if team:
            parent = self.center_pk_view
            bubble = BubbleWidget(parent, event_data)

            # Team photo positions and sizes
            # Team A: (600, 170, 350x350)
            # Team B: (900, 170, 350x350)

            if team == 'A':
                # Position around Team A (Left side) - WIDE RANDOM AREA
                x = random.randint(50, 600)
                y = random.randint(100, 800)
            else:  # Team B
                # Position around Team B (Right side) - WIDE RANDOM AREA
                x = random.randint(900, 1450)
                y = random.randint(100, 800)

            # Clamp to valid screen bounds
            x = max(10, min(x, 1500))
            y = max(10, min(y, 850))

        # Otherwise use standard positioning based on bubble_position settings
        elif position in ['left', 'right']:
            # Use center zone for left/right
            parent = self.center_pk_view
            bubble = BubbleWidget(parent, event_data)
        else:
            # Default for top/bottom if no team assigned
            parent = self.center_pk_view
            bubble = BubbleWidget(parent, event_data)

        # Check layout mode
        is_rotated = "Rotated" in self.layout_combo.currentText()
        
        if is_rotated:
            bubble.rotation_angle = -90
            
            # Adjust positioning for rotated layout
            if position == 'left': # Visually Top
                x = random.randint(100, 1400)
                y = random.randint(10, 100)
            elif position == 'right': # Visually Bottom
                x = random.randint(100, 1400)
                y = random.randint(900, 1000)
            elif position == 'bottom': # Visually Right
                x = random.randint(1400, 1500)
                y = random.randint(100, 1000)
            else: # top (default) -> Visually Left
                x = random.randint(50, 150)
                y = random.randint(100, 1000)
        else:
            # Standard positioning
            if position == 'left':
                x = random.randint(10, 100)
                y = random.randint(100, 700)
            elif position == 'right':
                x = random.randint(1400, 1500)
                y = random.randint(100, 700)
            elif position == 'bottom':
                x = random.randint(50, 1400)
                y = random.randint(20, 150)
            else: # top
                x = random.randint(50, 1400)
                y = random.randint(20, 150)

        bubble.move(x, y)
        bubble.show()

        # Set z-order: Like/Comment bubbles should be behind everything
        bubble.lower()

        self.active_bubbles.append(bubble)

        # Auto cleanup
        # Prioritize custom_duration if set
        if 'custom_duration' in event_data:
            duration = event_data['custom_duration']
        else:
            duration = event_data.get('duration', 3000)
            
        QTimer.singleShot(duration + 1000, lambda: self._cleanup_bubble(bubble))

    def _create_bubble(self, event_data, zone='top', team=None):
        """Create bubble in specified zone (for gifts)"""
        # ALWAYS use overlay zone for gifts to ensure they are on top
        parent = self.gift_overlay_zone
            
        # Inject custom settings
        event_data['custom_duration'] = self.bubble_settings['duration']
        event_data['custom_size'] = self.bubble_settings['size']
        event_data['custom_gift_size'] = self.bubble_settings['gift_size']

        bubble = BubbleWidget(parent, event_data)
        
        # Check layout mode
        is_rotated = "Rotated" in self.layout_combo.currentText()
        
        if is_rotated:
            bubble.rotation_angle = -90
            
            # Position based on zone and team (Rotated logic)
            # Top Zone -> Left Side
            # Bottom Zone -> Right Side
            
            if zone == 'bottom' and team:
                if team == 'A':
                    # Top-Left (Visually Top) -> Logic: Left side, Top half
                    x = random.randint(50, 200)
                    y = random.randint(100, 500)
                else:
                    # Bottom-Left (Visually Bottom) -> Logic: Left side, Bottom half
                    # Wait, Team B is usually Right side in standard view.
                    # In Rotated: Team A is Left (Visually Top), Team B is Right (Visually Bottom).
                    # So Team A gifts should be Left side. Team B gifts should be Right side.
                    
                    # Let's simplify:
                    # Team A -> Left Side (Visually Top of Stream)
                    # Team B -> Right Side (Visually Bottom of Stream)
                    
                    if team == 'A':
                         x = random.randint(50, 250)
                         y = random.randint(100, 900)
                    else:
                         x = random.randint(1300, 1500)
                         y = random.randint(100, 900)
            else:
                # Random positioning in zone
                if zone == 'top': # Left Side
                    x = random.randint(50, 250)
                    y = random.randint(100, 900)
                else: # Right Side
                    x = random.randint(1300, 1500)
                    y = random.randint(100, 900)
        else:
            # Standard positioning
            if zone == 'bottom' and team:
                if team == 'A':
                    # Widen range for Team A (Left side)
                    x = random.randint(50, 600)
                else:
                    # Widen range for Team B (Right side)
                    x = random.randint(900, 1450)
                y = random.randint(50, 800) # Full height range
            else:
                x = random.randint(50, 1450)
                y = random.randint(50, 800)

        bubble.move(x, y)
        bubble.show()

        # Set z-order: Gift bubbles should be in front of everything
        bubble.raise_()

        self.active_bubbles.append(bubble)

        # Auto cleanup
        # Prioritize custom_duration if set
        if 'custom_duration' in event_data:
            duration = event_data['custom_duration']
        else:
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
        
        # Auto-start battle as requested
        self._on_start_battle()

    def _on_disconnect_tiktok(self):
        """Disconnect from TikTok"""
        self.tiktok_handler.disconnect_from_live()
        if self.tiktok_thread:
            self.tiktok_thread.quit()
            # Use timeout to prevent GUI freeze
            if not self.tiktok_thread.wait(2000):  # 2 second timeout
                # Force terminate if still running
                self.tiktok_thread.terminate()
                self.tiktok_thread.wait(1000)  # Wait up to 1 more second

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
        print(f"[LOG] {message}")  # Print to terminal for debugging
        self.log_text.append(message)
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )

    def _initialize_assignments_from_widgets(self):
        """
        Initialize assignments from widget data after signals are connected.
        This fixes the race condition where widgets load data before signals are connected.
        """
        # Get assignments from gift widget
        if hasattr(self, 'gift_assignment_widget') and self.gift_assignment_widget.assignments:
            self._on_gift_assignment_changed(self.gift_assignment_widget.assignments)
            print(f"[INIT] Loaded {len(self.gift_assignment_widget.assignments)} gift assignments from widget")

        # Get assignments from interaction widget
        if hasattr(self, 'interaction_assignment_widget') and self.interaction_assignment_widget.assignments:
            self._on_interaction_assignment_changed(self.interaction_assignment_widget.assignments)
            print(f"[INIT] Loaded interaction assignments from widget:")
            print(f"  Like -> Team {self.interaction_assignment_widget.assignments.get('like', 'A')}")
            print(f"  Comment -> Team {self.interaction_assignment_widget.assignments.get('comment', 'A')}")

        # Get positions from bubble position widget
        if hasattr(self, 'bubble_position_widget') and self.bubble_position_widget.positions:
            self._on_bubble_position_changed(self.bubble_position_widget.positions)
            print(f"[INIT] Loaded bubble positions from widget")

        # Get sound settings from event sound widget
        if hasattr(self, 'event_sound_widget') and self.event_sound_widget.sound_settings:
            self._on_sound_settings_changed(self.event_sound_widget.sound_settings)
            print(f"[INIT] Loaded event sound settings from widget")

        # Get point settings from point settings widget
        if hasattr(self, 'point_settings_widget') and self.point_settings_widget.point_values:
            self._on_point_settings_changed(self.point_settings_widget.point_values)
            print(f"[INIT] Loaded custom point settings from widget:")
            print(f"  1 Like = {self.point_settings_widget.point_values.get('like', 1)} poin")
            print(f"  1 Comment = {self.point_settings_widget.point_values.get('comment', 1)} poin")

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
    """Custom progress bar for PK battle - Shows REAL POINTS - DRAGGABLE, ROTATABLE, RESIZABLE!"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.team_a_points = 0
        self.team_b_points = 0

        # Drag state
        self.dragging = False
        self.resizing = False
        self.resize_corner = None
        self.drag_start_pos = QPoint()
        self.rotation_angle = 0  # Degrees

        # Size limits
        self.min_width = 300
        self.max_width = 1500
        self.min_height = 40
        self.max_height = 200

        # Enable mouse tracking
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def set_points(self, team_a_points, team_b_points):
        """Set real points for both teams"""
        self.team_a_points = team_a_points
        self.team_b_points = team_b_points
        self.update()

    def wheelEvent(self, event):
        """Rotate with mouse wheel"""
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            # Ctrl + Wheel = Rotate
            delta = event.angleDelta().y()
            self.rotation_angle += delta / 8  # 1 degree per wheel step
            self.rotation_angle = self.rotation_angle % 360  # Keep in 0-360 range
            self.update()
        else:
            super().wheelEvent(event)

    def mousePressEvent(self, event):
        """Handle mouse press for drag/resize"""
        if event.button() == Qt.MouseButton.LeftButton:
            corner = self._get_corner_at_pos(event.pos())

            if corner:
                # Start resizing
                self.resizing = True
                self.resize_corner = corner
                self.drag_start_pos = event.pos()
            else:
                # Start dragging
                self.dragging = True
                self.drag_start_pos = event.globalPosition().toPoint() - self.pos()

    def mouseMoveEvent(self, event):
        """Handle mouse move for drag/resize"""
        if self.resizing:
            self._handle_resize(event.pos())
        elif self.dragging:
            # Move widget
            new_pos = event.globalPosition().toPoint() - self.drag_start_pos
            self.move(new_pos)
        else:
            # Update cursor based on position
            corner = self._get_corner_at_pos(event.pos())
            if corner:
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            else:
                self.setCursor(Qt.CursorShape.SizeAllCursor)

    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            self.resizing = False
            self.resize_corner = None
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def _get_corner_at_pos(self, pos):
        """Check if position is near a corner for resizing"""
        corner_size = 20
        w = self.width()
        h = self.height()

        # Check corners
        corners = {
            'top_left': QRect(0, 0, corner_size, corner_size),
            'top_right': QRect(w - corner_size, 0, corner_size, corner_size),
            'bottom_left': QRect(0, h - corner_size, corner_size, corner_size),
            'bottom_right': QRect(w - corner_size, h - corner_size, corner_size, corner_size),
        }

        for corner_name, rect in corners.items():
            if rect.contains(pos):
                return corner_name

        return None

    def _handle_resize(self, pos):
        """Handle resizing from corner"""
        if not self.resize_corner:
            return

        delta = pos - self.drag_start_pos
        new_width = self.width()
        new_height = self.height()
        new_x = self.x()
        new_y = self.y()

        if 'right' in self.resize_corner:
            new_width = max(self.min_width, min(self.max_width, self.width() + delta.x()))
        elif 'left' in self.resize_corner:
            new_width = max(self.min_width, min(self.max_width, self.width() - delta.x()))
            new_x = self.x() + delta.x()

        if 'bottom' in self.resize_corner:
            new_height = max(self.min_height, min(self.max_height, self.height() + delta.y()))
        elif 'top' in self.resize_corner:
            new_height = max(self.min_height, min(self.max_height, self.height() - delta.y()))
            new_y = self.y() + delta.y()

        self.setGeometry(new_x, new_y, new_width, new_height)
        self.drag_start_pos = pos

    def paintEvent(self, event):
        """Custom paint with rotation support"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        rect = self.rect()
        w = rect.width()
        h = rect.height()
        
        is_vertical = abs(abs(self.rotation_angle) - 90) < 5

        if self.rotation_angle != 0:
            painter.save()
            center = rect.center()
            painter.translate(center.x(), center.y())
            painter.rotate(self.rotation_angle)
            
            if is_vertical:
                # Swapped dimensions
                target_rect = QRect(-h//2, -w//2, h, w)
            else:
                target_rect = QRect(-w//2, -h//2, w, h)
        else:
            target_rect = rect
            
        # Use target_rect for drawing
        tw = target_rect.width()
        th = target_rect.height()
        tx = target_rect.x()
        ty = target_rect.y()

        # Background
        painter.fillRect(target_rect, QColor(50, 50, 50))

        # Calculate percentage for bar visual
        total = self.team_a_points + self.team_b_points
        if total > 0:
            team_a_pct = (self.team_a_points / total) * 100
            team_b_pct = (self.team_b_points / total) * 100
        else:
            team_a_pct = 50
            team_b_pct = 50

        # Team A bar (from left of target_rect)
        a_width = int(tw * (team_a_pct / 100))
        gradient_a = QLinearGradient(tx, ty, tx + a_width, ty)
        gradient_a.setColorAt(0, QColor(255, 107, 107))
        gradient_a.setColorAt(1, QColor(255, 82, 82))
        painter.fillRect(tx, ty, a_width, th, gradient_a)

        # Team B bar (from right of target_rect)
        b_width = int(tw * (team_b_pct / 100))
        gradient_b = QLinearGradient(tx + tw - b_width, ty, tx + tw, ty)
        gradient_b.setColorAt(0, QColor(78, 205, 196))
        gradient_b.setColorAt(1, QColor(61, 189, 179))
        painter.fillRect(tx + tw - b_width, ty, b_width, th, gradient_b)

        # Border
        painter.setPen(QPen(QColor(255, 255, 255), 3))
        painter.drawRect(target_rect.adjusted(1, 1, -1, -1))

        # REAL POINTS text (not percentage!)
        font = painter.font()
        font.setPointSize(20)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))

        # Team A points (left)
        painter.drawText(QRect(tx + 10, ty, 250, th),
                        Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                        f"{self.team_a_points:,}")

        # Team B points (right)
        painter.drawText(QRect(tx + tw - 260, ty, 250, th),
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                        f"{self.team_b_points:,}")

        # Draw resize handles at corners (always)
        painter.setPen(QPen(QColor(255, 255, 255, 100), 1))
        painter.setBrush(QColor(255, 255, 255, 50))
        corner_size = 8

        # Draw small circles at corners of target_rect
        corners = [
            (tx, ty), (tx + tw - corner_size, ty),
            (tx, ty + th - corner_size), (tx + tw - corner_size, ty + th - corner_size)
        ]

        for x, y in corners:
            painter.drawEllipse(int(x), int(y), corner_size, corner_size)

        # Restore if rotated
        if self.rotation_angle != 0:
            painter.restore()
