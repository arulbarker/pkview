"""
Main Window for TikTok Live Bubble Application
Contains bubble display, controls, simulation panel, and logs
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QLineEdit, QTextEdit,
                             QGroupBox, QGridLayout, QSplitter, QFrame,
                             QScrollArea, QComboBox, QSpinBox)
from PyQt6.QtCore import Qt, QTimer, pyqtSlot
from PyQt6.QtGui import QFont, QPalette, QColor
import config
from bubble_widget import BubbleWidget
from tiktok_handler import TikTokHandler, TikTokThread
from persistent_bubbles import PersistentViewerManager
from gift_tiers import get_gift_tier, get_gift_value_from_name, TIKTOK_GIFT_VALUES
import random


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()

        self.tiktok_handler = TikTokHandler()
        self.tiktok_thread = None
        self.active_bubbles = []
        self.persistent_viewer_manager = None  # Initialize later
        self.current_effect_settings = {}  # Store user's effect choices

        self._setup_ui()
        self._connect_signals()
        self._show_welcome_message()
        self._load_saved_effects()

    def _setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle(config.WINDOW_TITLE)
        self.setGeometry(100, 100, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Main layout
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left side: Bubble display area (fullscreen)
        self.bubble_container = self._create_bubble_container()
        splitter.addWidget(self.bubble_container)

        # Right side: Control panel
        control_panel = self._create_control_panel()
        splitter.addWidget(control_panel)

        # Set initial sizes (80% bubbles, 20% controls)
        splitter.setSizes([int(config.WINDOW_WIDTH * 0.8),
                          int(config.WINDOW_WIDTH * 0.2)])

        main_layout.addWidget(splitter)

        # Apply dark theme
        self._apply_theme()

    def _create_bubble_container(self):
        """Create the bubble display area"""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2e, stop:0.5 #16213e, stop:1 #0f3460);
                border: none;
            }
        """)
        container.setMinimumSize(800, 600)

        return container

    def _create_control_panel(self):
        """Create the control panel"""
        panel = QWidget()
        panel.setMaximumWidth(400)
        panel.setMinimumWidth(300)

        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Connection controls
        connection_group = self._create_connection_controls()
        layout.addWidget(connection_group)

        # Simulation controls
        simulation_group = self._create_simulation_controls()
        layout.addWidget(simulation_group)

        # Event log
        log_group = self._create_log_panel()
        layout.addWidget(log_group)

        # Settings
        settings_group = self._create_settings_panel()
        layout.addWidget(settings_group)

        return panel

    def _create_connection_controls(self):
        """Create connection control group"""
        group = QGroupBox("TikTok Live Connection")
        layout = QVBoxLayout()

        # Username input
        username_layout = QHBoxLayout()
        username_layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter TikTok username")
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)

        # Connect/Disconnect buttons
        button_layout = QHBoxLayout()

        self.connect_btn = QPushButton("🔴 Start Live")
        self.connect_btn.clicked.connect(self._on_connect_clicked)
        self.connect_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        self.disconnect_btn = QPushButton("⏹️ Stop Live")
        self.disconnect_btn.clicked.connect(self._on_disconnect_clicked)
        self.disconnect_btn.setEnabled(False)
        self.disconnect_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 10px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)

        button_layout.addWidget(self.connect_btn)
        button_layout.addWidget(self.disconnect_btn)
        layout.addLayout(button_layout)

        # Status label
        self.status_label = QLabel("Status: Disconnected")
        self.status_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
        layout.addWidget(self.status_label)

        group.setLayout(layout)
        return group

    def _create_simulation_controls(self):
        """Create simulation control group"""
        group = QGroupBox("Event Simulation (for Testing)")
        layout = QGridLayout()

        # Simulation buttons
        sim_buttons = [
            ("👋 Join", "join"),
            ("🎁 Gift", "gift"),
            ("💬 Comment", "comment"),
            ("🔗 Share", "share"),
            ("❤️ Follow", "follow"),
            ("👍 Like", "like"),
        ]

        row, col = 0, 0
        for text, event_type in sim_buttons:
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, et=event_type: self._simulate_event(et))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    padding: 8px;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #0b7dda;
                }
            """)
            layout.addWidget(btn, row, col)

            col += 1
            if col > 1:
                col = 0
                row += 1

        # Rapid test button
        rapid_btn = QPushButton("🚀 Rapid Test (10 events)")
        rapid_btn.clicked.connect(self._simulate_rapid_events)
        rapid_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
        """)
        layout.addWidget(rapid_btn, row + 1, 0, 1, 2)

        group.setLayout(layout)
        return group

    def _create_log_panel(self):
        """Create event log panel"""
        group = QGroupBox("Event Log")
        layout = QVBoxLayout()

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #00ff00;
                font-family: 'Consolas', monospace;
                border: 1px solid #333;
            }
        """)

        clear_btn = QPushButton("Clear Log")
        clear_btn.clicked.connect(self.log_text.clear)

        layout.addWidget(self.log_text)
        layout.addWidget(clear_btn)

        group.setLayout(layout)
        return group

    def _create_settings_panel(self):
        """Create settings panel"""
        group = QGroupBox("Settings & Effect Selector")
        layout = QVBoxLayout()

        # Fullscreen toggle
        fullscreen_btn = QPushButton("Toggle Fullscreen (F11)")
        fullscreen_btn.clicked.connect(self._toggle_fullscreen)
        layout.addWidget(fullscreen_btn)

        # Persistent Viewers toggle
        persistent_layout = QHBoxLayout()
        from PyQt6.QtWidgets import QCheckBox
        self.persistent_viewers_check = QCheckBox("Show Persistent Viewers")
        self.persistent_viewers_check.setChecked(False)
        self.persistent_viewers_check.stateChanged.connect(self._toggle_persistent_viewers)
        persistent_layout.addWidget(self.persistent_viewers_check)
        layout.addLayout(persistent_layout)

        # Ratio selector
        ratio_layout = QHBoxLayout()
        ratio_label = QLabel("Aspect Ratio:")
        ratio_label.setMinimumWidth(100)
        ratio_layout.addWidget(ratio_label)

        self.ratio_selector = QComboBox()
        for ratio_key, ratio_info in config.RATIO_MODES.items():
            self.ratio_selector.addItem(ratio_info['name'], ratio_key)

        # Set default ratio
        default_index = list(config.RATIO_MODES.keys()).index(config.DEFAULT_RATIO)
        self.ratio_selector.setCurrentIndex(default_index)
        self.ratio_selector.currentIndexChanged.connect(self._on_ratio_changed)

        ratio_layout.addWidget(self.ratio_selector)
        layout.addLayout(ratio_layout)

        # Separator
        layout.addWidget(QLabel("─" * 30))

        # Effect selectors for each event type
        layout.addWidget(QLabel("Choose Effect per Event Type:"))

        # Available effects (18 total - including 5 NEW PREMIUM effects!)
        effects = [
            # Original 10 effects
            'fade_in_out', 'sparkle_zoom', 'slide_bounce',
            'float_away', 'heart_pulse', 'quick_pop',
            'firework', 'rainbow', 'shake', 'spiral',
            # v1.3 effects
            'bounce_in', 'rotate_zoom', 'wave_slide',
            # v1.4 PREMIUM effects (NEW!)
            'bounce_cascade', 'explosion_particles', 'screen_takeover',
            'neon_glow', 'matrix_rain'
        ]

        # Create selector for each event type
        self.effect_selectors = {}
        event_types = [
            ('join', '👋 Join'),
            ('gift', '🎁 Gift'),
            ('comment', '💬 Comment'),
            ('share', '🔗 Share'),
            ('follow', '❤️ Follow'),
            ('like', '👍 Like')
        ]

        for event_key, event_label in event_types:
            event_layout = QHBoxLayout()
            label = QLabel(f"{event_label}:")
            label.setMinimumWidth(80)
            event_layout.addWidget(label)

            combo = QComboBox()
            combo.addItems(effects)

            # Set default from config
            default_effect = config.EVENT_CONFIGS.get(event_key, {}).get('effect', 'fade_in_out')
            if default_effect in effects:
                combo.setCurrentText(default_effect)

            combo.currentTextChanged.connect(
                lambda effect, ek=event_key: self._on_effect_changed(ek, effect)
            )

            event_layout.addWidget(combo)
            layout.addLayout(event_layout)

            self.effect_selectors[event_key] = combo

        # Apply button
        apply_btn = QPushButton("💾 Save Effect Settings")
        apply_btn.clicked.connect(self._save_effect_settings)
        apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(apply_btn)

        # Reset button
        reset_btn = QPushButton("🔄 Reset to Defaults")
        reset_btn.clicked.connect(self._reset_effect_settings)
        layout.addWidget(reset_btn)

        group.setLayout(layout)
        return group

    def _apply_theme(self):
        """Apply dark theme to the application"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
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
                padding: 0 5px;
            }
            QLabel {
                color: #ffffff;
            }
            QLineEdit {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 5px;
            }
            QPushButton {
                min-height: 30px;
            }
        """)

    def _connect_signals(self):
        """Connect signals from TikTok handler"""
        self.tiktok_handler.event_received.connect(self._on_event_received)
        self.tiktok_handler.connection_status.connect(self._on_connection_status)
        self.tiktok_handler.error_occurred.connect(self._on_error)
        self.tiktok_handler.log_message.connect(self._add_log)

    # Slots for button actions

    @pyqtSlot()
    def _on_connect_clicked(self):
        """Handle connect button click"""
        username = self.username_input.text().strip()

        if not username:
            self._add_log("❌ Please enter a TikTok username")
            return

        # Remove @ if user added it
        username = username.lstrip('@')

        self._add_log(f"Connecting to @{username}...")

        # Start connection in separate thread
        self.tiktok_thread = TikTokThread(self.tiktok_handler, username)
        self.tiktok_thread.start()

        # Update UI
        self.connect_btn.setEnabled(False)
        self.disconnect_btn.setEnabled(True)
        self.username_input.setEnabled(False)

    @pyqtSlot()
    def _on_disconnect_clicked(self):
        """Handle disconnect button click"""
        self._add_log("Stopping TikTok Live connection...")

        # Disconnect TikTok handler
        self.tiktok_handler.disconnect_from_live()

        # Stop thread properly
        if self.tiktok_thread and self.tiktok_thread.isRunning():
            self._add_log("Stopping background thread...")
            self.tiktok_thread.quit()
            self.tiktok_thread.wait(2000)  # Wait max 2 seconds

            if self.tiktok_thread.isRunning():
                self._add_log("Force terminating thread...")
                self.tiktok_thread.terminate()
                self.tiktok_thread.wait()

            self.tiktok_thread = None
            self._add_log("Thread stopped successfully")

        # Update UI
        self.connect_btn.setEnabled(True)
        self.disconnect_btn.setEnabled(False)
        self.username_input.setEnabled(True)

    @pyqtSlot(dict)
    def _on_event_received(self, event_data):
        """Handle received TikTok event"""
        self._create_bubble(event_data)

    @pyqtSlot(str)
    def _on_connection_status(self, status):
        """Handle connection status update"""
        self.status_label.setText(f"Status: {status}")

        if "Connected" in status:
            self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        else:
            self.status_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")

    @pyqtSlot(str)
    def _on_error(self, error_msg):
        """Handle error"""
        self._add_log(f"❌ ERROR: {error_msg}")

        # Reset UI state on connection error
        if "Connection" in error_msg or "Timeout" in error_msg:
            self.connect_btn.setEnabled(True)
            self.disconnect_btn.setEnabled(False)
            self.username_input.setEnabled(True)

    @pyqtSlot(str)
    def _add_log(self, message):
        """Add message to log"""
        self.log_text.append(message)
        # Auto-scroll to bottom
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )

    def _create_bubble(self, event_data):
        """Create and display a bubble widget"""
        # Apply gift tier system for gifts
        if event_data.get('type') == 'gift':
            gift_name = event_data.get('gift_name', '')
            gift_value = get_gift_value_from_name(gift_name)
            tier = get_gift_tier(gift_value)

            # Apply tier settings to event_data (override defaults)
            event_data['tier_effect'] = tier['effect']
            event_data['tier_size'] = tier['size']
            event_data['tier_duration'] = tier['duration']
            event_data['tier_color'] = tier['color']
            event_data['tier_border_width'] = tier['border_width']
            event_data['tier_glow_intensity'] = tier['glow_intensity']
            event_data['tier_name'] = tier['name']
            event_data['gift_value'] = gift_value

            self._add_log(f"🎁 {tier['name']} ({gift_value} coins) - {tier['description']}")

        bubble = BubbleWidget(self.bubble_container, event_data)
        bubble.show()

        # Track active bubbles
        self.active_bubbles.append(bubble)

        # Clean up after animation (use tier duration if available)
        duration = event_data.get('tier_duration') or event_data.get('duration', 3000)
        QTimer.singleShot(duration + 1000,
                         lambda: self._cleanup_bubble(bubble))

    def _cleanup_bubble(self, bubble):
        """Clean up finished bubble"""
        if bubble in self.active_bubbles:
            self.active_bubbles.remove(bubble)

    def _simulate_event(self, event_type):
        """Simulate a TikTok event for testing"""
        # Get random dummy user
        user = random.choice(config.DUMMY_USERS)

        event_data = {
            'type': event_type,
            'username': user['nickname'],
            'user_id': user['username'],
            'avatar_url': user['avatar'],
        }

        # Add type-specific data
        if event_type == 'gift':
            gift = random.choice(config.DUMMY_GIFTS)
            event_data['gift_name'] = gift['name']
            event_data['gift_count'] = random.randint(1, 5)

        elif event_type == 'comment':
            event_data['comment'] = random.choice(config.DUMMY_COMMENTS)

        elif event_type == 'like':
            event_data['like_count'] = random.randint(1, 50)

        # Create bubble
        self._create_bubble(event_data)
        self._add_log(f"🧪 Simulated {event_type} from {user['nickname']}")

    def _simulate_rapid_events(self):
        """Simulate multiple events rapidly for testing"""
        event_types = ['join', 'gift', 'comment', 'share', 'follow', 'like']

        for i in range(10):
            event_type = random.choice(event_types)
            # Delay each event slightly
            QTimer.singleShot(i * 300, lambda et=event_type: self._simulate_event(et))

        self._add_log("🚀 Rapid test started: 10 events incoming!")

    def _toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def _toggle_persistent_viewers(self, state):
        """Toggle persistent viewer bubbles"""
        if state == Qt.CheckState.Checked.value:
            # Enable persistent viewers
            if not self.persistent_viewer_manager:
                self.persistent_viewer_manager = PersistentViewerManager(self.bubble_container)
            self._add_log("✅ Persistent viewers enabled")
            self._add_log("Viewers will stay on screen until they leave")
        else:
            # Disable and clear
            if self.persistent_viewer_manager:
                self.persistent_viewer_manager.clear_all()
                self.persistent_viewer_manager = None
            self._add_log("❌ Persistent viewers disabled")

    def _on_ratio_changed(self, index):
        """Handle ratio selection change"""
        ratio_key = self.ratio_selector.itemData(index)
        ratio_info = config.RATIO_MODES[ratio_key]

        # Update window size to match ratio
        new_width = ratio_info['width']
        new_height = ratio_info['height']

        # Resize window (maintaining position)
        current_geo = self.geometry()
        self.setGeometry(current_geo.x(), current_geo.y(), new_width, new_height)

        # Update bubble container size
        if self.bubble_container:
            self.bubble_container.setMinimumSize(int(new_width * 0.7), int(new_height * 0.7))

        self._add_log(f"📐 Ratio changed to: {ratio_info['name']}")
        self._add_log(f"   Size: {new_width}x{new_height}")
        self._add_log(f"   {ratio_info['description']}")

    def _on_effect_changed(self, event_key, effect_name):
        """Handle effect selection change"""
        self.current_effect_settings[event_key] = effect_name
        self._add_log(f"Effect for {event_key}: {effect_name}")

    def _save_effect_settings(self):
        """Save current effect settings"""
        import json
        import os

        # Save to file
        try:
            settings_file = 'effect_settings.json'
            with open(settings_file, 'w') as f:
                json.dump(self.current_effect_settings, f, indent=2)

            self._add_log("💾 Effect settings saved!")
            self._add_log(f"Saved to: {settings_file}")

            # Apply to config
            for event_key, effect_name in self.current_effect_settings.items():
                if event_key in config.EVENT_CONFIGS:
                    config.EVENT_CONFIGS[event_key]['effect'] = effect_name

            self._add_log("✅ Effects applied! Test with simulation buttons")
        except Exception as e:
            self._add_log(f"❌ Error saving settings: {e}")

    def _reset_effect_settings(self):
        """Reset effects to defaults"""
        defaults = {
            'join': 'fade_in_out',
            'gift': 'sparkle_zoom',
            'comment': 'slide_bounce',
            'share': 'float_away',
            'follow': 'heart_pulse',
            'like': 'quick_pop'
        }

        # Update UI
        for event_key, effect_name in defaults.items():
            if event_key in self.effect_selectors:
                self.effect_selectors[event_key].setCurrentText(effect_name)

        self.current_effect_settings = defaults.copy()

        # Apply to config
        for event_key, effect_name in defaults.items():
            if event_key in config.EVENT_CONFIGS:
                config.EVENT_CONFIGS[event_key]['effect'] = effect_name

        self._add_log("🔄 Effects reset to defaults")

    def _load_saved_effects(self):
        """Load saved effect settings on startup"""
        import json
        import os

        settings_file = 'effect_settings.json'
        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r') as f:
                    saved_settings = json.load(f)

                self.current_effect_settings = saved_settings

                # Apply to config
                for event_key, effect_name in saved_settings.items():
                    if event_key in config.EVENT_CONFIGS:
                        config.EVENT_CONFIGS[event_key]['effect'] = effect_name

                self._add_log(f"📂 Loaded saved effects from {settings_file}")
            except Exception as e:
                self._add_log(f"⚠️ Could not load saved effects: {e}")

    def _show_welcome_message(self):
        """Show welcome message with instructions"""
        welcome_msg = """
╔══════════════════════════════════════════════════════╗
║   TikTok Live Bubble Animation - Welcome!            ║
╚══════════════════════════════════════════════════════╝

🎮 Quick Start:
   1. Try simulation buttons to test animations
   2. Click "🚀 Rapid Test" to see 10 bubbles at once
   3. To connect to real TikTok Live:
      - Enter TikTok username (without @)
      - Click "🔴 Start Live"
      - Wait 10-30 seconds for connection

💡 Tips:
   - Use simulation panel for testing (no live needed!)
   - Check this log for all events
   - Press F11 or use "Toggle Fullscreen" button
   - All effects are configurable in config.py

Ready to start! Click any simulation button to test 🎉
        """
        self._add_log(welcome_msg.strip())

    def closeEvent(self, event):
        """Handle window close"""
        # Disconnect from live if connected
        if self.tiktok_handler.is_connected:
            self.tiktok_handler.disconnect_from_live()

        # Stop thread
        if self.tiktok_thread and self.tiktok_thread.isRunning():
            self.tiktok_thread.quit()
            self.tiktok_thread.wait()

        event.accept()
